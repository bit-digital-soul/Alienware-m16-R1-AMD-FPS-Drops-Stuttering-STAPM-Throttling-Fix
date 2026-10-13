# Contributing

Reports from other owners are useful when they distinguish measured data from impressions. Start with the **Compatibility or test report** issue template.

## Useful evidence

Provide the model, CPU, installed BIOS version, SREP version and configuration checksum. Record the exact settings before and after, plus the workload, duration, charger, power/fan profile and monitoring setup. Report whether HWiNFO DELL EC monitoring was enabled.

If practical, capture synchronized frametime and sensor logs from the same repeatable workload. Screenshots are useful but do not establish the timing of a limit relative to an FPS drop. Say whether a setting was saved and verified after reboot. A final return to STT=0 after an Auto retest would extend the sequence documented here, but repeated thermal-policy changes are not required to file a report.

Do not include Service Tags, serial numbers, device UUIDs, BitLocker keys, account names or unrelated file paths. Inspect logs and images before uploading. Do not attach full BIOS dumps, extracted firmware executables or SREP binaries to this repository.

## Changes to the configuration

This CFG is pinned to the analyzed BIOS 1.25.0 image. Supporting another version requires a separate image analysis, module hash, unique search-pattern check, IFR review and clearly labeled hardware report. Do not infer compatibility from a model-family name or update a version string without checking the binary.

Keep firmware offsets tied to their specific module and file hash. Never present a PE offset as an address in the complete recovery image. Keep claims about menu access, setting persistence, performance and thermal behavior separate.

The verifier intentionally rejects changes to the published CFG. A new supported target needs reviewed reference values and its own configuration; do not remove checksum checks simply to make a modified file pass.

## Local checks

From the repository root, with Python 3.10 or newer:

```text
python tools/verify.py
python -m unittest discover -s tests -v
```

There are no external Python dependencies. The first command checks the exact CFG and the checksums of the packaged evidence. Tests cover altered configurations, incorrect firmware inputs and out-of-tree checksum paths. GitHub Actions runs these commands on the public package; it does not have the proprietary firmware input.

If you already have the original files, the optional checks are:

```text
python tools/verify.py --bios /path/to/BIOS_IMG.rcv --setup-utility-app /path/to/SetupUtilityApp.efi
```

Quote paths containing spaces. The tool reads files only and simulates the GUID replacement in memory; it does not extract, execute or flash firmware.

Preserve the CFG's CRLF endings and exact bytes. `SHA256SUMS` covers evidence and assets, not every prose file. Update evidence checksums only for an intentional, documented correction; keep the original case observations distinguishable from new reports.

Original contributions are accepted under the repository's [MIT license](LICENSE). Include attribution and applicable rights information for any third-party material.
