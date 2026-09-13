# Validation results

Executed on 2026-09-13 using Linux x86_64, Python 3.12.14, and ansible-core 2.19.13.

Command: `python scripts/verify.py` with the Ansible virtual environment active.

```text
PASS: all nine playbooks pass syntax checks
PASS: empty target set reproduced; corrected target runs and converges
PASS: undefined input reproduced; valid configuration renders and converges
PASS: duplicate writes reproduced; fixed file converges on desired content
PASS: missed notification and recovery caveat reproduced; fixed flow activates once
PASS: cleanup removes only generated lab output and is repeatable
```

The verification ran the broken and fixed playbooks against localhost in a temporary copy. Each fixed playbook returned `changed=0` on a second run. It checked the actual generated file contents and confirmed cleanup removed the generated directory.

The handler check also verified that removing the notification suppression after the file has already changed does not automatically activate the stale version. After resetting the simulation, the fixed playbook activated version two and did not run the handler again on an unchanged run.

Scope: local file operations and a simulated application activation. SSH transport, privilege escalation, Windows targets, real services, external inventories, and other Ansible versions were not tested.
