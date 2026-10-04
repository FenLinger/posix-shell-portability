# SPDX-License-Identifier: AGPL-3.0-only
"""Run public shell portability checks and emit bounded host diagnostics."""
from __future__ import annotations

import hashlib
import io
import json
import os
import platform
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "viewer" / "tools"))
from posix_shell import bash_argv, posix_shell  # noqa: E402


def command(argv):
    start = time.monotonic()
    try:
        result = subprocess.run(argv, capture_output=True, text=True,
                                encoding="utf-8", errors="replace", timeout=20)
        return {"argv": argv, "exit": result.returncode,
                "stdout": result.stdout[:8000], "stderr": result.stderr[:8000],
                "seconds": time.monotonic() - start}
    except (OSError, subprocess.TimeoutExpired) as error:
        return {"argv": argv, "exit": None, "error": str(error),
                "seconds": time.monotonic() - start}


def main():
    sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    output = io.StringIO()
    suite = unittest.defaultTestLoader.discover(
        str(ROOT / "viewer" / "tools" / "tests"), pattern="test_bash_resolver.py")
    start = time.monotonic()
    result = unittest.TextTestRunner(stream=output, verbosity=2).run(suite)
    tests = {"executed": result.testsRun, "failures": len(result.failures),
             "errors": len(result.errors), "skips": len(result.skipped),
             "seconds": time.monotonic() - start, "log": output.getvalue()}
    with tempfile.TemporaryDirectory(prefix="shell probe ") as tmp:
        script = Path(tmp) / "Unicode λ script.sh"
        script.write_text("printf '%s\\n' 'héllo λ'\n", encoding="utf-8")
        smoke = command(bash_argv(script))
    smoke["passed"] = smoke["exit"] == 0 and smoke.get("stdout") == "héllo λ\n"
    diagnostics = {"git": command(["git", "--version"])}
    if sys.platform == "linux":
        diagnostics["systemd_user"] = command(["systemctl", "--user", "is-system-running"])
    elif sys.platform == "win32":
        diagnostics["powershell"] = command([
            "powershell.exe", "-NoProfile", "-Command",
            "$PSVersionTable.PSVersion.ToString()"])
    elif sys.platform == "darwin":
        diagnostics["macos"] = command(["sw_vers"])
    passed = (result.wasSuccessful() and result.testsRun == 5
              and not result.skipped and smoke["passed"])
    record = {
        "schema": "public-shell-probe/1", "passed": passed,
        "profile": {"os": sys.platform, "architecture": platform.machine(),
                    "python": platform.python_version(), "bash": posix_shell()},
        "tests": tests, "unicode_subprocess": smoke, "diagnostics": diagnostics,
        "source_hashes": {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sorted(ROOT.rglob("*.py"))},
        "claims_excluded": ["Metal execution", "application authentication",
                            "persistent lifecycle", "reboot/logon recovery"],
    }
    rendered = json.dumps(record, ensure_ascii=False, indent=2)
    print(rendered)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8", newline="\n") as summary:
            summary.write("```json\n" + rendered + "\n```\n")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
