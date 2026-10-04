# SPDX-License-Identifier: AGPL-3.0-only
"""Shared Bash resolver adapter for the public tests."""
from __future__ import annotations

import os
import shutil
from pathlib import Path


import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from posix_shell import posix_shell as _posix_shell  # noqa: E402


def bash_path(exists=os.path.exists, which=shutil.which, os_name: str = os.name) -> str | None:
    return _posix_shell(which=which, exists=exists, os_name=os_name)


BASH = bash_path()
