#!/usr/bin/env python3
"""Exercise the intentional failures and fixes in an isolated temporary copy."""
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
ENV = {**os.environ, "ANSIBLE_NOCOLOR": "1", "ANSIBLE_FORCE_COLOR": "0"}


def main():
    if not shutil.which("ansible-playbook"):
        raise SystemExit("Activate the virtual environment from README.md first.")
    with tempfile.TemporaryDirectory(prefix="ansible-troubleshooting-") as temp:
        work = Path(temp)
        shutil.copytree(ROOT / "labs", work / "labs")
        shutil.copy2(ROOT / "inventory.yml", work / "inventory.yml")
        shutil.copy2(ROOT / "cleanup.yml", work / "cleanup.yml")

        def run(path, *extra, expect_failure=False):
            result = subprocess.run(
                ["ansible-playbook", "-i", "inventory.yml", path, *extra],
                cwd=work, env=ENV, text=True, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, timeout=90,
            )
            if (result.returncode != 0) != expect_failure:
                raise AssertionError(f"Unexpected exit {result.returncode}: {path}\n{result.stdout}")
            return result.stdout

        def no_changes(output):
            if not re.search(r"localhost\s+:.*changed=0\s", output):
                raise AssertionError(f"Expected an unchanged localhost recap:\n{output}")

        for path in sorted((work / "labs").glob("*/*.yml")):
            run(str(path.relative_to(work)), "--syntax-check")
        print("PASS: all nine playbooks pass syntax checks")

        result = run("labs/01-inventory/broken.yml")
        assert "no hosts matched" in result
        assert not (work / ".lab-output/01/result.txt").exists()
        run("labs/01-inventory/fixed.yml")
        assert (work / ".lab-output/01/result.txt").read_text() == "host reached\n"
        no_changes(run("labs/01-inventory/fixed.yml"))
        print("PASS: empty target set reproduced; corrected target runs and converges")

        result = run("labs/02-undefined-variable/broken.yml", expect_failure=True)
        assert "service_port" in result and "undefined" in result
        run("labs/02-undefined-variable/fixed.yml")
        assert (work / ".lab-output/02/app.conf").read_text() == "port=8080\nenvironment=development\n"
        no_changes(run("labs/02-undefined-variable/fixed.yml"))
        print("PASS: undefined input reproduced; valid configuration renders and converges")

        run("labs/03-idempotency/broken.yml")
        run("labs/03-idempotency/broken.yml")
        assert (work / ".lab-output/03/features.conf").read_text() == "feature=true\n" * 2
        run("labs/03-idempotency/fixed.yml")
        assert (work / ".lab-output/03/features.conf").read_text() == "feature=true\n"
        no_changes(run("labs/03-idempotency/fixed.yml"))
        print("PASS: duplicate writes reproduced; fixed file converges on desired content")

        run("labs/04-handlers/setup.yml")
        run("labs/04-handlers/broken.yml")
        active = work / ".lab-output/04/active.conf"
        assert active.read_text() == "version=1\n"
        assert (work / ".lab-output/04/app.conf").read_text() == "version=2\n"
        # The configuration already matches: fixing notification alone cannot recover it.
        no_changes(run("labs/04-handlers/fixed.yml"))
        assert active.read_text() == "version=1\n"
        run("labs/04-handlers/setup.yml")
        result = run("labs/04-handlers/fixed.yml")
        assert "RUNNING HANDLER" in result and active.read_text() == "version=2\n"
        result = run("labs/04-handlers/fixed.yml")
        no_changes(result)
        assert "RUNNING HANDLER" not in result
        print("PASS: missed notification and recovery caveat reproduced; fixed flow activates once")

        run("cleanup.yml")
        assert not (work / ".lab-output").exists()
        no_changes(run("cleanup.yml"))
        print("PASS: cleanup removes only generated lab output and is repeatable")


if __name__ == "__main__":
    main()
