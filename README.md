# POSIX shell portability

A small Python resolver selects a usable POSIX shell on Linux, macOS and native
Windows, excluding the System32 WSL launcher. On Windows, install Git for Windows.
Python 3.11 or later is required. No additional Python packages are needed.

Run `python ci/probe.py` to execute the five resolver tests and a real Bash
subprocess through a Unicode path containing spaces. The command prints structured
JSON and fails if a required check fails or skips. Host diagnostics are reported
separately from test results.

The published resolver matrix uses standard public Ubuntu, Windows and macOS
runners, with at most two concurrent jobs and ten minutes per matrix job. Pushes
to `ci-validation` run the matrix. Manual dispatch becomes available when the
workflow is present on the default branch. Results stay in logs and job summaries;
no artifacts or caches are uploaded.

The workflow includes an experimental fifteen-minute Ubuntu job after
the resolver matrix. It boots one disposable Ubuntu 24.04 x86_64 KVM guest with
at most two virtual CPUs and 2 GiB RAM. A synthetic systemd user heartbeat tests
launching SSH-parent exit, supervisor restart, recovery across a real reboot of
the same guest and disk, and explicit stop across a second guest reboot. The
unchanged public resolver tests and probe also run inside that guest. Nested
virtualization is experimental; runtime results, including unavailability, are
required before any environment predicate can be credited.

The lifecycle experiment is generic environment diagnostics. It does not prove
authenticated application workflows, trust acceptance, Windows
logon recovery, Metal execution, outer-host reboot, or persistence across CI jobs.
No private code, credentials or external persistent host is used.

## Licensing

The open-source license is **AGPL-3.0-only**; see [LICENSE](LICENSE).
Commercial use is permitted under the AGPL's conditions.

A **paid proprietary license** is available by separate written agreement with
the project maintainer. It can provide alternative permissions for uses that
need proprietary terms. See [LICENSING.md](LICENSING.md) for the licensing options.

The resolver is published at `FenLinger/posix-shell-portability` on
`ci-validation`. The lifecycle experiment remains unvalidated until actual job
results establish its declared checks.
