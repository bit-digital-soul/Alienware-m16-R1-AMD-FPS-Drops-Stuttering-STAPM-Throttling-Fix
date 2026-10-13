#!/usr/bin/env python3
"""Read-only checks for this exact case. Never loads EFI code or writes firmware."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
CFG_SHA = 'ec9a9e2eb74d8581573ba4b53f8c8ea04a236f4f8946055b267b7700bdd5bed4'
BIOS_SHA = '8be9a5771ae18fb0b649d5e9a57679ad1213c5abc9e09364c232c31a62a4e1f2'
PE_SHA = '350fad7419c53c862863617516c302eec146b6b240364c1ab78e1ea350b8969b'
BIOS_SIZE = 34667672
PE_SIZE = 0x2720


class VerificationError(Exception):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def digest(path):
    result = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            result.update(block)
    return result.hexdigest()


def exact_file(path, size, expected_sha, label):
    require(path.is_file(), f'{label}: file not found')
    require(path.stat().st_size == size, f'{label}: unexpected file size; unsupported input')
    require(digest(path) == expected_sha, f'{label}: SHA-256 mismatch; unsupported input')


def within_root(root, relative):
    path = (root / relative).resolve()
    require(path.is_relative_to(root.resolve()), 'Manifest path escapes the repository')
    return path


def occurrences(data, needle):
    require(bool(needle), 'Empty search pattern')
    found, start = [], 0
    while True:
        start = data.find(needle, start)
        if start < 0:
            return found
        found.append(start)
        start += 1


def verify_config(data, patch):
    require(hashlib.sha256(data).hexdigest() == CFG_SHA, 'CFG checksum mismatch: use the exact supplied file')
    require(len(data) == 277, 'Unexpected CFG size')
    require(not data.startswith(b'\xef\xbb\xbf'), 'CFG must not contain a BOM')
    require(b'\n' not in data.replace(b'\r\n', b''), 'CFG must use CRLF endings')
    lines = [line for line in data.decode('ascii').splitlines() if line]
    require(len(lines) == 8, 'Unexpected CFG structure')
    require(lines[:4] == ['Op LoadFromFV', 'SetupUtilityApp', 'Op FastestPatch', 'Pattern'], 'Unexpected CFG target/operation')
    require(lines[-2:] == ['Op Exec', 'Op End'], 'Unexpected CFG execution order')
    require(all(re.fullmatch(r'[0-9A-F]{96}', s) for s in lines[4:6]), 'Invalid 48-byte hex lines')
    old, new = map(bytes.fromhex, lines[4:6])
    require(lines[4] == patch['search_bytes'] and lines[5] == patch['replacement_bytes'], 'CFG and manifest disagree')
    require(old[:16] == new[:16] and old[32:] == new[32:], 'Surrounding GUIDs changed')
    require(sum(a != b for a, b in zip(old, new)) == 16, 'Unexpected changed-byte count')
    return old, new


def verify_package(root=ROOT):
    manifest = json.loads((root / 'evidence/firmware-manifest.json').read_text(encoding='utf-8'))
    require(manifest['input']['sha256'] == BIOS_SHA, 'Unexpected reference BIOS hash')
    require(manifest['input']['bytes'] == BIOS_SIZE, 'Unexpected reference BIOS size')
    patch = manifest['patch']
    require(patch['config_sha256'] == CFG_SHA and patch['target_sha256'] == PE_SHA, 'Unexpected reference hashes')
    cfg = within_root(root, patch['config'])
    require(list((root / 'configs').glob('*.cfg')) == [cfg], 'Expected exactly the supplied CFG in configs/')
    old, new = verify_config(cfg.read_bytes(), patch)
    entries = (root / 'SHA256SUMS').read_text(encoding='ascii').splitlines()
    require(bool(entries), 'Checksum manifest is empty')
    seen = set()
    for line in entries:
        match = re.fullmatch(r'([0-9a-f]{64})  (.+)', line)
        require(match is not None, 'Invalid checksum entry')
        expected, relative = match.groups()
        require(relative not in seen, 'Duplicate checksum entry')
        seen.add(relative)
        path = within_root(root, relative)
        require(path.is_file(), f'Missing packaged file: {relative}')
        require(digest(path) == expected, f'Checksum mismatch: {relative}')
    required = {patch['config'], 'evidence/firmware-manifest.json', 'evidence/case-observations.json',
                'evidence/snapshot-readings.csv', 'evidence/STAPM_IFR_extract.txt',
                'assets/bios-stapm-auto.png', 'assets/bios-stapm-manual.png',
                'assets/hwinfo-stt-disabled.png', 'assets/hwinfo-stt-auto.png'}
    require(required <= seen, 'Checksum manifest does not cover all required evidence')
    return old, new


def mapped_pe(data):
    # The exact hash is checked by the caller before parsing this known small image.
    require(data[:2] == b'MZ', 'Missing DOS signature')
    pe = struct.unpack_from('<I', data, 0x3C)[0]
    require(data[pe:pe + 4] == b'PE\0\0', 'Missing PE signature')
    machine, sections = struct.unpack_from('<HH', data, pe + 4)
    require(machine == 0x8664, 'Expected x64 PE')
    optional_size = struct.unpack_from('<H', data, pe + 20)[0]
    optional = pe + 24
    require(struct.unpack_from('<H', data, optional)[0] == 0x20B, 'Expected PE32+')
    image_size, header_size = struct.unpack_from('<II', data, optional + 56)
    require(image_size == PE_SIZE, 'Unexpected mapped image size')
    require(header_size <= len(data) and header_size <= image_size, 'Invalid header size')
    require(struct.unpack_from('<I', data, optional + 112 + 5 * 8 + 4)[0] == 0, 'Unexpected base relocations')
    image = bytearray(image_size)
    image[:header_size] = data[:header_size]
    table = optional + optional_size
    require(table + sections * 40 <= len(data), 'Invalid section table')
    for i in range(sections):
        section = table + i * 40
        rva, raw_size, raw_offset = struct.unpack_from('<III', data, section + 12)
        require(raw_offset + raw_size <= len(data), 'Invalid raw section range')
        require(rva + raw_size <= image_size, 'Invalid mapped section range')
        image[rva:rva + raw_size] = data[raw_offset:raw_offset + raw_size]
    return bytes(image)


def verify_pe(path, old, new):
    exact_file(path, PE_SIZE, PE_SHA, 'SetupUtilityApp PE')
    data = path.read_bytes()
    mapped = mapped_pe(data)
    require(occurrences(data, old) == [0x22C0], 'Expected one raw match at 0x22C0')
    require(occurrences(mapped, old) == [0x22C0], 'Expected one mapped match at RVA 0x22C0')
    require(not occurrences(data, new), 'Input appears patched already')
    # Simulate in memory only. No output file is written.
    changed_image = data.replace(old, new, 1)
    changed = [i for i, (a, b) in enumerate(zip(data, changed_image)) if a != b]
    require(changed == list(range(0x22D0, 0x22E0)), 'Unexpected patch effect')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bios', type=Path, help='Optional original BIOS_IMG.rcv for exact size/hash verification')
    parser.add_argument('--setup-utility-app', type=Path, help='Optional extracted original SetupUtilityApp PE payload')
    args = parser.parse_args(argv)
    try:
        old, new = verify_package()
        print('PASS: exact CFG, structure and packaged evidence checksums')
        if args.bios:
            exact_file(args.bios, BIOS_SIZE, BIOS_SHA, 'BIOS_IMG.rcv')
            print('PASS: supplied recovery image matches the analyzed file')
        if args.setup_utility_app:
            verify_pe(args.setup_utility_app, old, new)
            print('PASS: original PE, unique raw/mapped match and exactly 16 changed bytes')
        print('No firmware was executed or written. Installed BIOS and thermal safety were not checked.')
        return 0
    except (VerificationError, OSError, ValueError, KeyError, UnicodeError, struct.error) as error:
        print(f'FAIL: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
