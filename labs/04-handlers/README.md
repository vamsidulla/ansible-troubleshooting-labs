# 04 · Configuration changed, but activation did not run

Intermediate · 25 minutes

## Scenario

The configuration file shows version two, while a simulated application still uses version one. `active.conf` models the loaded configuration; this lab does not run a real service.

Run from the repository root after the [installation steps](../../README.md). Start with a clean exercise: `ansible-playbook -i inventory.yml cleanup.yml` removes this collection's generated files.

## Reproduce and investigate

```bash
ansible-playbook -i inventory.yml labs/04-handlers/setup.yml
ansible-playbook -i inventory.yml labs/04-handlers/broken.yml
cat .lab-output/04/app.conf .lab-output/04/active.conf
```

### Expected evidence

The files show `version=2` and `version=1`. The copy task wrote the file but `changed_when: false` suppressed notification, so no activation handler ran.

Before opening the solution, explain the observation, your hypothesis, and one check that could disprove it.

<details>
<summary>Reveal the fix and verification</summary>

Let the module report whether it changed the configuration and notify the handler on that change. Handlers normally run at the end of the tasks section. If a later task must inspect the newly active configuration, use `meta: flush_handlers` at the required point. Removing `changed_when: false` after the broken run alone will not recover the stale application: the file already matches and copy makes no new change. Reset this disposable simulation before exercising the fixed flow. For a real incident, validate the new configuration and explicitly perform the required reload/restart as a recovery action.

```bash
ansible-playbook -i inventory.yml labs/04-handlers/setup.yml
ansible-playbook -i inventory.yml labs/04-handlers/fixed.yml
ansible-playbook -i inventory.yml labs/04-handlers/fixed.yml
cat .lab-output/04/app.conf .lab-output/04/active.conf
```

Both files must show `version=2`; the second fixed run must report `changed=0` without running the handler.

</details>

## Interview check

A thermostat received a new setting but suppressed the signal to the heater. Which part corresponds to writing configuration, change detection, and a handler?

## Cleanup

```bash
ansible-playbook -i inventory.yml cleanup.yml
```

This removes only `.lab-output` in this checkout. See [validation results](../../VALIDATION.md) for the tested environment and scope.
