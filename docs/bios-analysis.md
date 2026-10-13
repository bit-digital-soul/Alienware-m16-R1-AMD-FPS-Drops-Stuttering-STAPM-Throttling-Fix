# BIOS 1.25.0: why this configuration targets SetupUtilityApp

This page records the offline BIOS analysis used to expose AMD CBS on my laptop. The analysis was prepared with AI assistance before I photographed the menu and compared STT settings. I confirmed menu access on my system; I have not validated long-term thermal behavior or other hardware.

## Image and method

| Item | Value |
|---|---|
| Image | `BIOS_IMG.rcv` |
| Size | 34,667,672 bytes |
| SHA-256 | `8be9a5771ae18fb0b649d5e9a57679ad1213c5abc9e09364c232c31a62a4e1f2` |
| Dell package reference | [FYD7W, Alienware m16 R1 AMD / m18 R1 AMD](https://www.dell.com/support/home/en-us/drivers/driversdetails?driverid=FYD7W) |
| Firmware volumes | 5 unique FV headers/contents encountered |
| FFS records / PE, TE and RAW payloads | 437 / 514 |
| Unique buffers scanned for the binary GUIDs | 573, including nested and decompressed buffers |

Local Python scripts recursively parsed FV/FFS/section structures, decompressed LZMA sections and decoded HII/IFR packages. FV header checksums, bounds, opcode lengths and scope balance were checked. There were no reported unsupported compression sections or extraction issues in this pass. The non-FFS NVRAM volume was not parsed as FFS.

`pefile` was used for PE mapping, and Microsoft's x64 `dumpbin` for disassembly. UEFITool/UEFIExtract was not used in the original analysis. Vendor GUID opcodes were retained as raw payloads rather than claiming complete semantic decoding. This is static analysis, not a cryptographic firmware audit. The original image was not modified or executed during that analysis.

Nested buffers overlap; their hit counts are not independent physical copies. The reference SHA-256 identifies the supplied file. Obtain firmware directly from Dell, not from this repository; its package page may vary by locale or availability.

## The generic CBS GUID did not match

The legacy example searched H2OFormBrowserDxe for:

```text
E33545B0043046499EB714942898305300000000
```

That is binary GUID `B04535E3-3004-4946-9EB7-149428983053` followed by four zero bytes. The GUID itself was not found in the original image or the recursively scanned decompressed buffers. The failed patch alone had not proven CBS was absent; subsequent extraction found it under a different FormSet GUID.

## Actual CBS identifiers

| Object | Identifier / location |
|---|---|
| CBS driver | `CbsSetupDxeRPL` |
| Driver FFS GUID | `2848A12F-3F86-47C7-81D8-D3FD47B205B2` |
| **AMD CBS FormSet GUID** | **`C03209ED-5F4B-4631-BD03-8ED627CD9DAF`** |
| HII PackageList GUID | `38A0FF25-EF7B-47E7-AB63-E56D9A67361B` |
| FormSet class GUID | `93039971-8545-4B04-B45E-32EB8326040E` |
| Root FormId | `0x7000` |
| PE size / SizeOfImage | `0x24820` |
| PE SHA-256 | `c0bb3840cdc394835e7fd0df5aedde9cfad6332ed637b7ac42955b864c1a3a43` |
| PackageList / forms package | `0xB1E0` / `0xB1F4` |
| Forms package length | `0x7341` |
| FormSet opcode / GUID field | `0xB1F8` / `0xB1FA` |

Binary FormSet GUID: `ED0932C04B5F3146BD038ED627CD9DAF`.

The CBS driver has CPU-family checks, HII ConfigAccess handling and HII registration code. A byte-identical HII resource also exists in `dGpuOnlyDxe`, FFS GUID `09AC30C4-0E82-4E97-97C1-68CC492E57E1`, starting at `0x4720`. This does not establish that both resources are registered simultaneously at runtime.

The CFG reuses the platform's existing HII registration through SetupUtilityApp. It does not start a second CBS driver or force-publish a detached HII resource.

## Dell's menu-selection table

Target: **SetupUtilityApp**, FFS GUID `3935B0A1-A182-4887-BC56-675528E78877`.

- PE size / SizeOfImage: `0x2720`.
- PE SHA-256: `350fad7419c53c862863617516c302eec146b6b240364c1ab78e1ea350b8969b`.
- FFS body length: `0x2756`, including its section layout. This matches the historical load log and is distinct from the PE size.

| PE offset = RVA | Slot | Original FormSet GUID |
|---|---|---|
| `0x22C0` | Main | `4DBD61FE-E487-4CED-80BD-7C2495A12BC6` |
| `0x22D0` | Advance | `0383EE8B-C386-4DC0-888B-DB90420A0942` |
| `0x22E0` | Security | `5204F764-DF25-48A2-B337-9EC122B85E0D` |
| `0x22F0` | Boot | `2D068309-12AC-45AB-9600-9187513CCDD8` |
| `0x2300` | Exit | `B6936426-FB04-4A7B-AA51-FD49397CDC01` |
| `0x2310` | Terminator | Zero GUID |

A separate matching-mode array at `0x2320` contains `00 00 00 00 00 FF`. The function at `0xC24` iterates the arrays and HII packages. Its helper at `0xB60`, called near `0xE17`, compares FormSet GUIDs for mode 0; mode 1 permits class GUIDs, and mode 2 permits either kind of match.

CBS is absent from the original list. This is a **menu filter/order table**, not the Lenovo example's interleaved GUID-plus-isShown layout. Simply appending a GUID over the terminator would collide with the nearby mode array and its count assumptions.

## Exact patch

The [CFG](../configs/Alienware_m16_R1_AMD_1.25.0_CBS_ENG_LOG.cfg) loads SetupUtilityApp, substitutes the Advance GUID, and then starts the application. The search includes Main and Security as surrounding context.

```text
Op LoadFromFV
SetupUtilityApp

Op FastestPatch
Pattern
FE61BD4D87E4ED4C80BD7C2495A12BC68BEE830386C3C04D888BDB90420A094264F7045225DFA248B3379EC122B85E0D
FE61BD4D87E4ED4C80BD7C2495A12BC6ED0932C04B5F3146BD038ED627CD9DAF64F7045225DFA248B3379EC122B85E0D

Op Exec

Op End
```

Offline checks found exactly one 48-byte match at `0x22C0`, both in the PE file and its mapped image. Search and replacement have equal length; only `0x22D0..0x22DF` changes, exactly 16 bytes. The terminator and mode array remain unchanged. This PE has no base-relocation directory.

The operation behavior is visible in [SREP 0.2.4's OpCode.c](https://raw.githubusercontent.com/Maxinator500/SmokelessRuntimeEFIPatcher-RUS/0.2.4/SmokelessRuntimeEFIPatcher/OpCode.c). This configuration has no runtime model/hash guard and does not establish compatibility with another firmware merely because a similar pattern exists there.

## STAPM in IFR

Navigation: **AMD CBS (FormId 0x7000) → SMU Common Options (0x7006)**. It is a direct root reference, not a submenu under NBIO in this image. The reference opcode is at `0xB2EB`; the SMU form starts at `0xDC0A`.

VarStore **AmdSetupRPL**:

- GUID: `3A997502-647A-4C82-998E-52EF9486A247`.
- VarStoreId: `0x5000`.
- Buffer size: `0x6D5`.
- Declaration: `0xB255`.

| Field | QuestionId | VarOffset | Width | IFR opcode offset | Values / compiled default |
|---|---|---|---:|---|---|
| STAPM Control | `0x0105` | `0x268` | 1 | `0xE942` | Auto=0 (default), Manual=1 |
| System Temperature Tracking | `0x0106` | `0x269` | 1 | `0xE97B` | Auto=15 (default), enabled=1, disabled=0 |
| STAPM Boost Override | `0x0107` | `0x26A` | 1 | `0xE9BB` | Auto=15 (default), use SMU default=0, use Boost field=1 |
| STAPM Boost | `0x0108` | `0x26B` | 1 | `0xE9FB` | Auto=15 (default), enabled=1, disabled=0 |
| Tskin Time Constant | `0x0109` | `0x26C` | 4 | `0xEA45` | Seconds, uint32; default=0 |

Question `0x0009`, **Combo CBS**, is a platform selector at VarOffset `0x20`. Its compiled default is not a live reading. Let `Q9` mean Combo CBS, `Q105` STAPM Control and `Q108` STAPM Boost. The following expressions **hide** their fields when true:

| SUPPRESS_IF offset | Field | Expression |
|---|---|---|
| `0xE936` | STAPM Control | `Q9 != 3` |
| `0xE965` | System Temperature Tracking | `Q105 != 1 OR Q9 != 3` |
| `0xE9A5` | STAPM Boost Override | `Q105 != 1 OR Q9 != 3` |
| `0xE9E5` | STAPM Boost | `Q105 != 1 OR Q9 != 3` |
| `0xEA25` | Tskin Time Constant | `Q9 != 3 OR (Q105 != 1 AND Q108 != 1)` |

These expressions were checked against 63 combinations. The menu patch does not alter them. Do not force Combo CBS=3 on another platform to make the fields appear.

Offsets above are within the extracted CBS PE; these sections have file offset equal to RVA. VarOffset is relative to AmdSetupRPL. **Neither coordinate is an offset into BIOS_IMG.rcv or a physical-memory write address.** The fields are documented for analysis, not as instructions for direct NVRAM editing.

The focused [IFR extract](../evidence/STAPM_IFR_extract.txt) retains the original opcode bytes and help strings. IFR structure definitions were checked against [EDK II](https://raw.githubusercontent.com/tianocore/edk2/master/MdePkg/Include/Uefi/UefiInternalFormRepresentation.h).

## Rechecking the target

The included [verifier](../tools/verify.py) is read-only and uses Python's standard library. It checks the bundled CFG and evidence; optional inputs check the exact recovery image and the exact extracted SetupUtilityApp PE:

```text
python tools/verify.py --bios /path/to/BIOS_IMG.rcv --setup-utility-app /path/to/SetupUtilityApp.efi
```

The optional PE must be the extracted PE payload, not the entire FFS file or an already-patched image. Its hash must match before the verifier inspects the pattern. The verifier does not extract the BIOS, boot an EFI application, identify installed firmware or write a patched file. Detailed identifiers and static checks are preserved in [firmware-manifest.json](../evidence/firmware-manifest.json).
