# Evidence index

| File | Contents and limits |
|---|---|
| [firmware-manifest.json](firmware-manifest.json) | Recovery-file and module identities, patch bytes, offsets and separate static/runtime validation status. |
| [case-observations.json](case-observations.json) | My hardware, troubleshooting history, settings, test sequence and unresolved questions. |
| [snapshot-readings.csv](snapshot-readings.csv) | Manual transcription of current and maximum readings from the two screenshots. **Not an exported HWiNFO sensor log.** |
| [STAPM_IFR_extract.txt](STAPM_IFR_extract.txt) | Focused decoded IFR records and supporting help text from CbsSetupDxeRPL. Not a full firmware/module dump. |

The four source screenshots are indexed in [assets](../assets/README.md). The narrative interpretation is in [results](../docs/results.md); the binary analysis is in [bios-analysis](../docs/bios-analysis.md).

## Integrity and reproducibility

The root [SHA256SUMS](../SHA256SUMS) covers the configuration, these four evidence files and the four screenshots. The [verifier](../tools/verify.py) checks them and pins the expected configuration hash. These checks detect accidental changes against the packaged references; they are **not a digital signature or proof of an installed BIOS version**.

With the exact original recovery image and extracted SetupUtilityApp payload supplied locally, the verifier additionally checks their hashes and simulates the unique 16-byte GUID replacement in memory. Firmware files are not included in this repository. Full extraction and reverse engineering are not performed by the public verifier.

## What remains unverified

- A final return from STT=Auto to STT=0 after the drops returned in my test.
- Synchronized frametime/sensor data, test duration and exact workload.
- Independent effects of the Boost Override and Boost fields.
- Long-term chassis and component thermal behavior with STT disabled.
- Other laptops, CPU variants and BIOS versions.

I changed the thermal-interface material, observed stutters associated with HWiNFO DELL EC monitoring and tried RyzenAdj/UXTU earlier in the troubleshooting process. My logs from those steps are incomplete. These are background observations, not independently reproduced causes or mandatory steps.
