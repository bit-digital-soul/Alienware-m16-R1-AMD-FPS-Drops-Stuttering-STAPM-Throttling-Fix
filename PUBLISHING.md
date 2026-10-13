# Publish this repository on GitHub

This folder is ready to publish. No GitHub repository has been created or uploaded as part of preparing these files.

## Suggested repository details

- **Name:** `alienware-m16-r1-amd-stapm-workaround`
- **Description:** `Alienware m16 R1 AMD FPS drops and STAPM throttling: documented BIOS 1.25.0 workaround using System Temperature Tracking settings and a Dell-specific SREP config.`
- **Visibility:** Public, if you want other owners to find the guide.
- **Topics:** `alienware`, `amd`, `ryzen`, `stapm`, `stt`, `fps-drops`, `stuttering`, `cpu-throttling`, `bios`, `uefi`, `srep`, `troubleshooting`

The guide identifies the tested hardware and firmware but contains no Service Tag, serial number, device UUID or recovery key. Review any additional screenshots or logs you add for those identifiers.

## Option A: Git and GitHub CLI

Install Git and GitHub CLI if needed, sign in with `gh auth login`, and open a terminal in **this folder**, where `README.md` is located. Run:

```sh
python tools/verify.py
python -m unittest discover -s tests -v
git init -b main
git add .
git commit -m "Document Alienware m16 R1 AMD STT/STAPM workaround"
gh repo create alienware-m16-r1-amd-stapm-workaround --public --source=. --remote=origin --push --description "Alienware m16 R1 AMD FPS drops and STAPM throttling: documented BIOS 1.25.0 workaround using System Temperature Tracking settings and a Dell-specific SREP config."
gh repo edit --add-topic alienware --add-topic amd --add-topic ryzen --add-topic stapm --add-topic stt --add-topic fps-drops --add-topic stuttering --add-topic cpu-throttling --add-topic bios --add-topic uefi --add-topic srep --add-topic troubleshooting
```

If Git asks for an author identity, configure the name and email you want shown on public commits. GitHub offers a no-reply email address in account settings. The commands above are for a new, empty repository; do not run `git init` in an unrelated project or overwrite an existing remote.

GitHub CLI documents the create-and-push options in [`gh repo create`](https://cli.github.com/manual/gh_repo_create).

## Option B: GitHub website

1. Create a public repository with the suggested name. Leave the automatic README, license and `.gitignore` options unchecked because these files are already supplied.
2. Extract the prepared ZIP locally. Upload the **contents** of its inner repository folder, so `README.md`, `docs/`, `configs/` and `assets/` appear at the repository root.
3. Include `.github/`, `.gitignore`, `.gitattributes` and `.editorconfig`; some file browsers hide dot-prefixed entries. The Git/CLI route is more reliable for preserving the complete tree.
4. Commit the upload, then add the description and topics in the repository's About panel.

See GitHub's [file upload instructions](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository).

## After publication

- Open the README and check that all four screenshots load across the linked pages.
- Check **Actions → Verify published configuration**. The workflow checks the public package without downloading or executing firmware. A workflow pass does not validate hardware safety or another BIOS version.
- Keep the compatibility scope and the unresolved final Auto-to-0 retest visible when sharing the guide.
- Use the included compatibility-report issue template for additional owners' observations.
- Optionally create a `v0.1.0` release using [CHANGELOG.md](CHANGELOG.md). GitHub automatically provides source archives; no BIOS image or EFI executable needs to be attached.

The package includes an MIT license for the original documentation, configuration and verification code. Third-party firmware material and interface images retain their respective rights; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
