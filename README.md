# POSIX shell portability candidate

A small Python resolver selects a usable POSIX shell on Linux, macOS and native
Windows, excluding the System32 WSL launcher. On Windows, install Git for Windows.
Python 3.11 or later is required. No additional Python packages are needed.

Run `python ci/probe.py` to execute the five resolver tests and a real Bash
subprocess through a Unicode path containing spaces. The command prints structured
JSON and fails if a required check fails or skips. Host diagnostics are reported
separately from test results.

The CI candidate uses standard public Ubuntu, Windows and macOS runners, with at
most two concurrent jobs and ten minutes per job. It retains results in logs and
job summaries; it does not upload artifacts or caches. Pushes to `ci-validation`
run the matrix. Manual dispatch becomes available when the workflow is present
on the default branch.

These checks cover this resolver only. They do not prove Metal execution,
application authentication, persistent services, or recovery after reboot/logon.

## Licensing

The open-source license is **AGPL-3.0-only**; see [LICENSE](LICENSE).
Commercial use is permitted under the AGPL's conditions.

A **paid proprietary license** is available by separate written agreement with
the project maintainer. It can provide alternative permissions for uses that
need proprietary terms. See [LICENSING.md](LICENSING.md) for the licensing options.

This is an unpublished candidate. Publication destination and source ownership
clearance remain pending.
