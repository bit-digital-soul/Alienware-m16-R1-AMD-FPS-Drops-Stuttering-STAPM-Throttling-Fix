# Alienware m16 R1 AMD FPS Drops, Stuttering & STAPM Throttling Fix

**The problem:** recurring FPS drops while gaming, with HWiNFO showing **APU STAPM Limit at 100%**, even when the CPU temperature is below its thermal limit.

**The workaround:** disable **System Temperature Tracking (STT)** in the hidden AMD CBS BIOS menu using the settings below. On my laptop, the FPS drops disappeared with these settings. When I switched STT back to Auto, they returned.

**Tested on my laptop: Alienware m16 R1 AMD · Ryzen 9 7845HX · BIOS 1.25.0.** This configuration is specific to that BIOS; I have not tested other versions or models.

## Solution: change the STAPM settings in AMD CBS

The controls are hidden in the standard Dell BIOS interface. Use **SREP 0.2.4 RUS** with the included **Dell-specific configuration** to open them.

**[Start here: step-by-step guide →](docs/guide.md)** — tool download, USB preparation and BIOS menu access.

Open **AMD CBS → SMU Common Options**, then set:

| Setting | Value |
|---|---|
| STAPM Control | **Manual** |
| System Temperature Tracking | **0 — Disabled** |
| STAPM Boost Override | **1** |
| STAPM Boost | **0** |
| Tskin Time Constant | **0 — leave the existing value** |

Save changes and exit, then test the same game. **STT=0 is the key difference in my comparison.** Keep the other power and thermal controls at their original settings.

The [provided SREP CFG](configs/Alienware_m16_R1_AMD_1.25.0_CBS_ENG_LOG.cfg) opens the menu through a temporary memory patch. Saved BIOS settings persist after reboot.

> Disabling STT changes system thermal management. I have not validated long-term chassis temperatures. Record your original settings and use the [rollback instructions](docs/testing-and-rollback.md#restore-the-recorded-original-settings) to restore them.

## Details

- [Why STAPM can limit performance below the CPU temperature limit](docs/problem.md)
- [My before/after screenshots, results and limitations](docs/results.md)
- [Testing, troubleshooting and rollback](docs/testing-and-rollback.md)
- [Dell BIOS analysis, patch details and verification](docs/bios-analysis.md)
- [Report your results](CONTRIBUTING.md)

[MIT license](LICENSE) · [SREP credits and sources](THIRD_PARTY_NOTICES.md)
