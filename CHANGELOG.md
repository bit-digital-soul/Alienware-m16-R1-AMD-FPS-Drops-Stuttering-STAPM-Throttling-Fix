# Changelog

## 0.1.0 — 2026-10-13

- Document the Alienware m16 R1 AMD / Ryzen 9 7845HX / BIOS 1.25.0 case and its STT/STAPM settings.
- Record how the FPS drops disappeared on my laptop with STT=0 and returned after I changed STT to Auto, with screenshots and a transcription of sensor readings.
- Include the Dell-specific SREP 0.2.4 configuration that exposes AMD CBS through SetupUtilityApp.
- Explain the actual CBS FormSet, menu-selection array, IFR fields and visibility conditions found in the supplied recovery image.
- Add preparation, testing, rollback and GitHub publishing instructions.
- Add checksums, a read-only verifier, rejection-path tests and a GitHub Actions workflow.

This release records my observations on one laptop. A final Auto-to-0 repeat, synchronized frametime logs, long-term chassis thermal validation and other hardware/BIOS versions remain unverified.
