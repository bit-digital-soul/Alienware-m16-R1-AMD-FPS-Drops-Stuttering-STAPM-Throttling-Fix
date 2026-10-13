# Sources, attribution and third-party notices

## Original material

The repository's original explanatory text, Dell-specific configuration and read-only verification code are offered under the [MIT license](LICENSE). The laptop observations and screenshots are mine. I prepared the firmware analysis and documentation with AI assistance, using the recovery image and my test observations as references.

The MIT license does not relicense Dell, AMD, Insyde, HWiNFO or other third-party firmware, interfaces, trademarks or source code. Screenshots contain their respective interfaces; the short IFR extract contains firmware-derived text and records included to document the specific finding. Their underlying rights remain with the respective owners. This is an independent troubleshooting case, with no claimed vendor endorsement.

## SREP

- [SmokelessRuntimeEFIPatcher upstream project](https://github.com/barlowhaydnb/SmokelessRuntimeEFIPatcher), credited to SmokelessCPUv2 and upstream contributors.
- [Maxinator500's RUS fork](https://github.com/Maxinator500/SmokelessRuntimeEFIPatcher-RUS).
- [SREP 0.2.4 RUS release I used](https://github.com/Maxinator500/SmokelessRuntimeEFIPatcher-RUS/releases/tag/0.2.4).
- [Tagged source and configuration documentation](https://github.com/Maxinator500/SmokelessRuntimeEFIPatcher-RUS/tree/0.2.4).
- [Application source at 0.2.4](https://raw.githubusercontent.com/Maxinator500/SmokelessRuntimeEFIPatcher-RUS/0.2.4/SmokelessRuntimeEFIPatcher/SmokelessRuntimeEFIPatcher.c), used to verify configuration discovery, language/log filename switches and log replacement behavior.

SREP executables and source are not bundled. Obtain them from the linked project and consult its applicable terms. The CFG in this repository was constructed for the analyzed Dell image; the generic Lenovo GUID example does not match this case.

## Firmware and format references

- [AMD's STAPM patent, US9958921B2](https://patents.google.com/patent/US9958921B2/en), for the general distinction between exterior temperature management and CPU junction-temperature limits. It is background, not evidence of this Dell's exact algorithm.
- [Dell BIOS package reference, driver ID FYD7W](https://www.dell.com/support/home/en-us/drivers/driversdetails?driverid=FYD7W), for the m16 R1 AMD/m18 R1 AMD BIOS package family. Dell may localize or redirect this page. This repository's exact-file reference is the size and SHA-256 of the supplied `BIOS_IMG.rcv`, not a claim that every download from a product page is the same file.
- [Dell m16 R1 AMD boot sequence](https://www.dell.com/support/manuals/en-me/alienware-m16-r1-amd-laptop/alienware-m16r1-amd-service-manual/boot-sequence?guid=guid-c50bed7f-226b-4768-ab61-9725153df132&lang=en-us), for the F12 one-time boot menu.
- [TianoCore EDK II UEFI IFR definitions](https://github.com/tianocore/edk2/blob/master/MdePkg/Include/Uefi/UefiInternalFormRepresentation.h), used as a format reference for decoding IFR opcodes.

The original recovery image, full extracted modules and modified firmware images are not distributed here. The included [focused IFR extract](evidence/STAPM_IFR_extract.txt) supports the field meanings and conditions described in the guide. All firmware checksums identify analyzed files, not individual devices.

## Operational references

- [Microsoft BitLocker overview](https://support.microsoft.com/en-us/windows/security/encryption/bitlocker-overview), including recovery considerations when firmware settings change.
- [GitHub: adding a file to a repository](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository).
- [GitHub CLI: create a repository](https://cli.github.com/manual/gh_repo_create).
- [actions/checkout v4.2.2](https://github.com/actions/checkout/releases/tag/v4.2.2), referenced by a pinned commit in the verification workflow. The action is fetched by GitHub Actions when the workflow runs; its source is not included in this package.
