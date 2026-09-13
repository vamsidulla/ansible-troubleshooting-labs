# Ansible Troubleshooting Labs

Practice the failures behind developer environment automation: choose the right hosts, supply valid configuration, converge repeatedly, and activate changes reliably.

**Four local labs · Beginner → Intermediate · No cloud credentials · No sudo**

These are personal learning exercises. They use a supplied localhost inventory and write only beneath this checkout's `.lab-output/`. The handler lab models a service with files, so it does not restart your system services.

## Learning sequence

| Order | Lab | What you learn |
|---|---|---|
| 1 | [Inventory mismatch](labs/01-inventory/) | Host patterns, inventory inspection, and empty successful runs |
| 2 | [Undefined template variable](labs/02-undefined-variable/) | Variable contracts, validation, and runtime template errors |
| 3 | [Broken idempotency](labs/03-idempotency/) | Desired state, repeated-run checks, and appropriate modules |
| 4 | [Suppressed handler notification](labs/04-handlers/) | Change reporting, activation, handler timing, and recovery |

For each lab: reproduce → observe → explain → fix → run again → clean up. Open its README before the solution playbook. Each includes an analogy-based interview check.

## Install and start

Use Linux, macOS, or WSL with Python 3.11+ and Git. Execute these commands from the repository root in a Bash-compatible terminal:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
ansible-playbook --version
ansible-inventory -i inventory.yml --graph
ansible-playbook -i inventory.yml labs/01-inventory/broken.yml --list-hosts
```

The version pin makes these exercises reproducible; it is the tested version, not a claim about the latest release. Use the supplied inventory: it uses a local connection and the Python interpreter running Ansible.

## Verify the collection

```bash
python scripts/verify.py
```

The verification script copies the exercise sources into a temporary directory, checks the intended failures and results, and runs the fixes twice. It does not use your manually generated lab output. See [VALIDATION.md](VALIDATION.md).

## Cleanup

```bash
ansible-playbook -i inventory.yml cleanup.yml
```

This deletes only this checkout's `.lab-output/`, including output from all four labs. No credentials, external inventory, system packages, or privileged tasks are needed.

## Continue learning

After these labs, continue with [Terraform Troubleshooting Labs](https://github.com/vamsidulla/terraform-troubleshooting-labs). The earlier collection is [Kubernetes Troubleshooting Labs](https://github.com/vamsidulla/kubernetes-troubleshooting-labs).

## References

- [Ansible inventory guide](https://docs.ansible.com/projects/ansible/latest/inventory_guide/intro_inventory.html)
- [Ansible copy module](https://docs.ansible.com/projects/ansible/latest/collections/ansible/builtin/copy_module.html)
- [Ansible handlers](https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_handlers.html)

Created for [Vamsi Krishna's personal learning portfolio](https://github.com/vamsidulla). These exercises demonstrate local practice and do not claim production deployment experience.
