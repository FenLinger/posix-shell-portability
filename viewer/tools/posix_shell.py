# SPDX-License-Identifier: AGPL-3.0-only
"""Resolve a usable POSIX shell on Linux, macOS and native Windows. Prefer Git for Windows Bash over the System32 WSL launcher."""
from __future__ import annotations

import os
import shutil
from pathlib import Path


def posix_shell(which=shutil.which, exists=os.path.exists, os_name: str = os.name) -> str | None:
    """A usable Bash path, or None. Never the WSL stub."""
    if os_name != "nt" and exists("/bin/bash"):
        return "/bin/bash"
    git = which("git")
    if git:
        root = Path(git).resolve().parent.parent          # <Git>/cmd/git.exe -> <Git>
        for rel in ("bin/bash.exe", "usr/bin/bash.exe", "bin/bash"):
            cand = root / rel
            if exists(str(cand)):
                return str(cand)
    for name in ("bash", "sh"):
        p = which(name)
        if p and "system32" not in p.replace("\\", "/").lower():
            return p
    return None


def bash_argv(script, *args: str) -> list[str]:
    """`[<bash>, script, *args]` -- argv to run a shell script on any platform.
    Falls back to the bare name only when no shell was found, so the failure names `bash`."""
    # The script path is POSIX: it is an argument to bash, and on Windows `str(Path)` would hand
    # it `scripts\x.sh`, whose backslash bash eats.
    return [posix_shell() or "bash", Path(script).as_posix(), *args]
