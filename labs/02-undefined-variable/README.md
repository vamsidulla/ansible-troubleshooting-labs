# 02 · A template cannot resolve its input

Beginner · 20 minutes

## Scenario

A configuration file fails to render even though the playbook defines a port.

Run from the repository root after the [installation steps](../../README.md). Start with a clean exercise: `ansible-playbook -i inventory.yml cleanup.yml` removes this collection's generated files.

## Reproduce and investigate

```bash
ansible-playbook -i inventory.yml labs/02-undefined-variable/broken.yml --syntax-check
ansible-playbook -i inventory.yml labs/02-undefined-variable/broken.yml
cat labs/02-undefined-variable/templates/app.conf.j2
```

### Expected evidence

Syntax checking passes, but the real run fails because `service_port` is undefined. The playbook supplies `app_port`; these are different names. Syntax validation alone does not evaluate every runtime template.

Before opening the solution, explain the observation, your hypothesis, and one check that could disprove it.

<details>
<summary>Reveal the fix and verification</summary>

Use one variable contract: the fixed play supplies `service_port` and asserts its type and range before rendering. Do not add a silent default to hide a missing required value. A real role should document required variables and intentional defaults.

```bash
ansible-playbook -i inventory.yml labs/02-undefined-variable/fixed.yml
ansible-playbook -i inventory.yml labs/02-undefined-variable/fixed.yml
cat .lab-output/02/app.conf
```

Expect `port=8080`, `environment=development`, and a second run with `changed=0`.

</details>

## Interview check

A form asks for a delivery address, but the envelope contains a billing address. Why is the presence of some address insufficient? The producer and consumer must agree on the exact input contract.

## Cleanup

```bash
ansible-playbook -i inventory.yml cleanup.yml
```

This removes only `.lab-output` in this checkout. See [validation results](../../VALIDATION.md) for the tested environment and scope.
