# Testing, rollback and troubleshooting

## Compare behavior rather than trying to eliminate every limit

Reproduce the same workload with the same charger, power/fan profile and similar starting temperature. Record the time until a drop. If logging, keep the polling interval and enabled sensors consistent and reset HWiNFO statistics at the start of each run.

Useful observations include:

- FPS and frametime over time, especially during the original drop window.
- CPU effective clocks, utilization and CPU Package Power.
- APU STAPM Limit, PPT FAST/SLOW Limit and Thermal Limit.
- HTC / PROCHOT CPU / PROCHOT EXT flags.
- GPU load/power, fan behavior and chassis comfort where observable.

HWiNFO's percentage limit sensors show utilization of a limit, not the limit's value in watts. A reached PPT SLOW limit can coexist with stable FPS; raising it is not a required part of this workaround. Slow PPT concerns averaged power, as described in [RyzenAdj's documentation](https://github.com/FlyGoat/RyzenAdj/wiki/Renoir-Tuning-Guide); platform-specific behavior in that older guide should not be assumed to match this Dell in every detail.

I separately observed stutters associated with DELL EC monitoring, so I recommend keeping it disabled when reproducing my comparison. Use the same monitoring configuration in both runs.

## A useful comparison sequence

1. Record a baseline with the original settings.
2. Apply the [recorded workaround](../README.md#solution-change-the-stapm-settings-in-amd-cbs), then repeat the original workload long enough to cover its normal drop window.
3. If checking the contribution of STT, change only System Temperature Tracking to Auto and repeat. The drops returned on my laptop at this step.
4. Restore STT=0 and repeat again if continuing the experiment. I have not documented this final repeat in my results.

Stop the test if behavior becomes unstable or chassis/component temperatures become concerning. Because STT has been disabled, an acceptable CPU temperature alone is not sufficient evidence of acceptable system temperatures. This guide does not set a new temperature target or authorize unlimited power.

## Restore the recorded original settings

Use the same version-matched SREP USB to reopen **AMD CBS → SMU Common Options**. If currently on Auto, temporarily select STAPM Control → Manual to expose the fields, then restore the inner fields **before hiding them again**:

1. System Temperature Tracking → **Auto**.
2. STAPM Boost Override → **Auto**.
3. STAPM Boost → **Auto**.
4. Tskin Time Constant → **0**, the photographed original value. If your documented original value differed, use your own record.
5. STAPM Control → **Auto**.
6. Save Changes and Exit.

Reopen the menu later if you need to confirm persistence. This order restores the fields addressed by this guide; it is not a claim that every firmware setting has been reset.

Remove the USB from normal boot afterward. Restore the original Secure Boot setting if you changed it, and resume BitLocker protection if you suspended it. Keep the recovery key available while doing so. **Removing the USB alone does not reset saved CBS settings.**

If Windows fails to start but Setup remains accessible, restore the recorded settings through Setup. If Setup itself is inaccessible, consult Dell's model-specific recovery/service instructions or qualified support. This repository does not contain a tested no-POST recovery procedure. Do not flash a modified image or perform a blind NVRAM reset based on this guide.

## Troubleshooting

| Symptom | Next check |
|---|---|
| USB is not listed | Confirm UEFI boot, FAT32 and `EFI/BOOT/BOOTX64.EFI` on that USB. Confirm the file is the actual EFI application. |
| Secure Boot rejects the application | Review [Secure Boot and BitLocker](guide.md#secure-boot-and-bitlocker); do not clear security keys. |
| An old/wrong configuration runs | Keep only one lowercase `.cfg` in the USB volume root. |
| Missing RegularExpressionProtocol message | This CFG uses FastestPatch, which uses exact bytes. Inspect the actual load/patch result rather than switching to a random pattern. |
| SetupUtilityApp load fails or the patch fails | Exit without saving. Check installed BIOS, CFG hash, fork/version and log. Do not force an offset patch. |
| Patch succeeds but CBS does not appear | The live HII registration/browser state needs investigation. A matched table alone does not prove the CBS HII package is registered. |
| CBS appears but STAPM Control does not | Platform-dependent IFR conditions may suppress it. Do not force Combo CBS to 3 or remove all SUPPRESS_IF blocks. |
| STT=0 does not improve the drops | Restore the original settings and collect synchronized performance/limit data. Other bottlenecks can cause the same symptom. |
| STT=Auto brings the drops back | This matches what I observed, but document the readings rather than assuming every system has the same cause. |
| A firmware update changes the behavior | Verify the new firmware independently. The included patch is only validated against the recorded 1.25.0 image. |

For a report, use the repository's [compatibility report template](../.github/ISSUE_TEMPLATE/compatibility_report.md). Include the model, CPU, BIOS and exact settings, but redact private identifiers and recovery keys from logs/screenshots.
