# issue-pilot-benchmark

A small FastAPI application used as the target repository for the IssuePilot
coding-agent harness.

This repository is **intentionally broken at HEAD**. Visible tests under
`tests/` reproduce symptoms. Hidden gold tests live in the harness repo and
are not part of this tree.

## Layout

```
app/          FastAPI app, auth, users, orders, inventory, pricing, payments
tests/        Symptom-level reproductions (one issue per file)
```

## Run tests

```bash
pip install -r requirements.txt
pytest -q
```

Do not fix the bugs by hand in the committed baseline — the harness runs
`git reset --hard <base_commit> && git clean -fd` before every task.
