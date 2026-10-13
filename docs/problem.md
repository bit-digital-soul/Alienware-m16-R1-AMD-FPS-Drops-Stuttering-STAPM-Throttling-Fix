# Why STAPM can cause FPS drops below the CPU temperature limit

**STAPM** means **Skin Temperature Aware Power Management**. It manages power using the device's exterior-temperature budget; that temperature may be measured or estimated. STAPM can therefore constrain power even when the CPU die is below its own temperature threshold. AMD describes the general mechanism in [its STAPM patent](https://patents.google.com/patent/US9958921B2/en); that reference does not establish the exact implementation in this Dell.

Here, **STT** means the BIOS field **System Temperature Tracking**. On my Alienware m16 R1 AMD, the recurring FPS drops disappeared after I set STT to 0 alongside the recorded companion settings. When I changed only STT back to Auto, the drops returned, with HWiNFO showing APU STAPM Limit at 100%.

That comparison points to STT's involvement. It does not establish why Dell's default policy produced the behavior, identify a faulty sensor or prove that all STAPM limits were disabled. Other causes can produce similar FPS drops; the sensor reading and comparison matter.

## What the workaround changes

The Dell-specific SREP configuration exposes the hidden AMD CBS menu. I then changed the STAPM settings manually in Setup. The menu patch is temporary, while saved settings can remain across reboots.

I kept STAPM Boost Override at 1 and STAPM Boost at 0. I did not test their independent contributions; those values alone were insufficient when STT was returned to Auto. Tskin Time Constant stayed at its recorded default of 0, whose meaning beyond that default was not established. It should not be interpreted as unlimited.

Disabling system temperature tracking changes thermal policy. CPU temperature alone cannot establish that the chassis and every component remain within an acceptable range. I have not validated long-term chassis temperatures.

## Separate issues from the troubleshooting history

- I had replaced Element 31 with PTM7950 before the STT comparison. Repasting was not established as a prerequisite for this workaround.
- I separately linked periodic stutters to HWiNFO DELL EC monitoring. Keep the monitoring setup consistent when comparing settings.
- I tried RyzenAdj and UXTU without success; I do not have the exact versions and complete failure logs in this record.

Continue to the [step-by-step solution](guide.md), [my results](results.md) or [testing and rollback](testing-and-rollback.md).
