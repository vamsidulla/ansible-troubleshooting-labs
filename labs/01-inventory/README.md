# 01 · A successful job targeted zero hosts

Beginner · 15 minutes

## Scenario

A developer setup job exits successfully, but its output file never appears.

Run from the repository root after the [installation steps](../../README.md). Start with a clean exercise: `ansible-playbook -i inventory.yml cleanup.yml` removes this collection's generated files.

## Reproduce and investigate

```bash
ansible-inventory -i inventory.yml --graph
ansible-playbook -i inventory.yml labs/01-inventory/broken.yml --list-hosts
ansible-playbook -i inventory.yml labs/01-inventory/broken.yml
test -f .lab-output/01/result.txt && cat .lab-output/01/result.txt
```

### Expected evidence

The play warns about an unmatched `application` group and reports no hosts matched. The file check fails. Ansible can return exit code 0 when a play matches no hosts; that does not prove configuration was applied.

Before opening the solution, explain the observation, your hypothesis, and one check that could disprove it.

<details>
<summary>Reveal the fix and verification</summary>

The inventory defines `lab`, but the play targets `application`. Correct the host pattern and use `--list-hosts` before a deployment. A useful CI gate checks the intended host count and the expected result, not only the command exit code.

```bash
ansible-playbook -i inventory.yml labs/01-inventory/fixed.yml
ansible-playbook -i inventory.yml labs/01-inventory/fixed.yml
cat .lab-output/01/result.txt
```

Expect `host reached` and `changed=0` on the second fixed run.

</details>

## Interview check

A bus driver completed the route with an empty passenger list. Did the intended people arrive? Map the passenger list to inventory and the route selection to the play host pattern.

## Cleanup

```bash
ansible-playbook -i inventory.yml cleanup.yml
```

This removes only `.lab-output` in this checkout. See [validation results](../../VALIDATION.md) for the tested environment and scope.
