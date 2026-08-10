# issue-pilot-benchmark

A small FastAPI application intentionally seeded with 8 bugs (3 easy / 3 medium
/ 2 hard). Used as the target repository for the IssuePilot coding-agent
harness.

This repository is **intentionally broken at HEAD**: `pytest` is expected to
report multiple failures. Each failing "gold test" corresponds to a task in
`issue-pilot/eval/dataset.json`.

## Layout

```
app/
  auth.py          issues 001 (expired JWT), 006 (missing claim), 007 (role in token)
  users.py         issues 004 (missing user), 007 (role passthrough)
  calculator.py    issue  002 (sum_inclusive off-by-one)
  validators.py    issue  003 (empty email accepted)
  orders.py        issues 005 (qty ignored), 008 (idempotency)
  main.py          FastAPI wiring
tests/
  test_auth.py, test_users.py, test_calculator.py, test_validators.py, test_orders.py
```

## Run tests

```bash
pip install -r requirements.txt
pytest -q
```

Do **not** fix the bugs by hand in the committed baseline — the harness runs
`git reset --hard <base_commit> && git clean -fd` before every task to
guarantee reproducibility.
