# 03 · The playbook changes a file on every run

Intermediate · 20 minutes

## Scenario

A repeatedly executed setup job keeps appending the same feature flag.

Run from the repository root after the [installation steps](../../README.md). Start with a clean exercise: `ansible-playbook -i inventory.yml cleanup.yml` removes this collection's generated files.

## Reproduce and investigate

```bash
ansible-playbook -i inventory.yml labs/03-idempotency/broken.yml
ansible-playbook -i inventory.yml labs/03-idempotency/broken.yml
cat .lab-output/03/features.conf
```

### Expected evidence

Both runs report a change and the file contains duplicate lines. This is a real repeated mutation, not merely noisy reporting.

Before opening the solution, explain the observation, your hypothesis, and one check that could disprove it.

<details>
<summary>Reveal the fix and verification</summary>

The shell command describes an action to repeat. The copy module describes the complete desired file. It removes the accumulated duplicates and compares the result before writing again. This lab owns the entire file; use `lineinfile` or `blockinfile` when only a part is yours to manage. Setting `changed_when: false` on the append command would only hide the defect.

```bash
ansible-playbook -i inventory.yml labs/03-idempotency/fixed.yml
ansible-playbook -i inventory.yml labs/03-idempotency/fixed.yml
cat .lab-output/03/features.conf
```

Expect exactly one `feature=true` line and `changed=0` on the second fixed run.

</details>

## Interview check

Tell a robot to ensure the light is on. Why is blindly toggling the switch unsafe on the second run? Explain observed state, desired state, and convergence.

## Cleanup

```bash
ansible-playbook -i inventory.yml cleanup.yml
```

This removes only `.lab-output` in this checkout. See [validation results](../../VALIDATION.md) for the tested environment and scope.
