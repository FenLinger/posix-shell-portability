# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for POSIX shell selection and exclusion of the Windows WSL launcher."""
from __future__ import annotations

import unittest
from pathlib import Path

from _bash import bash_path


class TheResolverPrefersTheShebangsShellThenGitsBash(unittest.TestCase):

    def test_bin_bash_wins_where_it_exists(self):
        self.assertEqual(bash_path(exists=lambda p: p == "/bin/bash", which=lambda n: None, os_name="posix"), "/bin/bash")

    def test_without_bin_bash_the_bash_beside_git_is_chosen(self):
        which = {"git": "C:/Program Files/Git/cmd/git.exe", "bash": "C:/Windows/System32/bash.exe"}.get
        exists = lambda p: str(p).replace("\\", "/").endswith("Git/bin/bash.exe")
        got = bash_path(exists=exists, which=which)
        self.assertTrue(got and got.replace("\\", "/").endswith("Git/bin/bash.exe"), got)

    def test_the_wsl_stub_is_never_chosen(self):
        which = {"bash": "C:/Windows/System32/bash.exe"}.get
        self.assertIsNone(bash_path(exists=lambda p: False, which=which))

    def test_a_plain_bash_on_path_is_the_last_resort(self):
        which = {"bash": "/usr/local/bin/bash"}.get
        self.assertEqual(bash_path(exists=lambda p: False, which=which), "/usr/local/bin/bash")

    def test_the_live_resolution_is_usable_here(self):
        b = bash_path()
        if b is None:
            self.skipTest("no bash on this machine")
        self.assertTrue(Path(b).exists(), b)


if __name__ == "__main__":
    unittest.main()
