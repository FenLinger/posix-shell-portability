# POSIX shell portability

A small Python module for selecting Bash and building portable shell-script
arguments on Linux, macOS and native Windows. On Windows it prefers Bash from
Git for Windows and excludes a launcher found under System32.

## Install

Use Python 3.11 or later and an installed Bash. Native Windows needs Git for
Windows. There are no third-party Python dependencies, package downloads or
build steps. Copy or unpack this source directory into your chosen location;
the module lives at `viewer/tools/posix_shell.py`.

Run commands below from the unpacked directory. Copy the module into your Python
application, or add `viewer/tools` to your application's import path.

## Quick start

Find the shell:

```bash
python -c "import sys; sys.path.insert(0, 'viewer/tools'); from posix_shell import posix_shell; print(posix_shell())"
```

Run an existing script without shell-string interpolation:

```python
import subprocess
import sys

sys.path.insert(0, "viewer/tools")
from posix_shell import bash_argv

subprocess.run(bash_argv("my script.sh", "an argument with spaces"), check=True)
```

## API

`posix_shell(which=shutil.which, exists=os.path.exists, os_name=os.name)` returns
a shell path as `str`, or `None` when no candidate is found. The injectable
`which`, `exists` and `os_name` parameters support deterministic resolver tests.

The search order is `/bin/bash` on a non-Windows host, Bash adjacent to a
resolved Git executable, then `bash` or `sh` on PATH outside System32. Git's
candidate locations are `bin/bash.exe`, `usr/bin/bash.exe` and `bin/bash`.

`bash_argv(script, *args)` returns a `list[str]` containing the shell, the script
path rendered with POSIX separators, and the supplied argument strings. Pass it
directly to `subprocess.run`. If resolution fails, it uses the bare name `bash`;
execution may then raise an error. It neither executes nor validates the script.

## Tests and diagnostics

```bash
python ci/probe.py
```

The probe executes five resolver unit tests and one real Bash subprocess through
a path containing spaces and Unicode. It fails if a required test fails, errors
or skips, or if the subprocess's Unicode output differs from the expected bytes.
It prints a JSON record with counts, exits, timings, runtime details and Python
source hashes. Git and platform diagnostics are separate from the pass decision.

The optional GitHub Actions workflow tests the same probe on standard Ubuntu,
macOS and native Windows runners, using Python 3.11.9, at most two concurrent
jobs, and a ten-minute limit per job. It writes results to logs and job summaries
without uploading artifacts or caches. Pushes to `ci-validation` trigger the
matrix; manual dispatch requires the workflow on the repository's default branch.

## Scope and limitations

This package selects a shell; it does not install Bash, translate shell syntax
or convert paths between different filesystems. Resolution checks locations,
not executable versions or permissions. The PATH fallback can select `sh`;
scripts needing Bash features should use a host with Bash installed. Unit tests
with injected Windows paths are distinct from actual execution on Windows.

There are no hardware, persistent-service, authentication, reboot or logon
guarantees. The package contains no private datasets, research corpus or agent
configuration.

## Licensing

The open-source license is **AGPL-3.0-only**; see [LICENSE](LICENSE).
Commercial use is permitted under its conditions.

A **paid proprietary license** is available by separate executed agreement for
rights controlled by the licensor. No proprietary grant or automatic assignment
of contribution rights is made here. See [LICENSING.md](LICENSING.md).
