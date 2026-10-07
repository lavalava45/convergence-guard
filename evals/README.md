# Convergence Guard comparative eval

This directory contains the public, reproducible part of the comparative evaluation harness for Convergence Guard.

The eval compares four complete workflows:

1. `single-context`
2. `shared-context-multi-agent`
3. `cg-reduced`
4. `cg-full`

The first stage is a technical pilot: two cases × four modes × one run each = eight runs. The main study is intentionally not created yet. Main-case authoring and the final freeze happen only after the pilot exposes procedural defects.

## Safety boundary

Ground-truth keys, answer keys, hidden provenance structures, calibration truth labels, and judge mappings must not live anywhere under this git repository. They belong in a separate private directory outside the repo and are read only by the judging stage.

Public case directories contain only participant-visible material:

```text
case.json
prompt.md
evidence/
```

The validator rejects common hidden-key filenames if they appear inside a public case.

## Current status

- Protocol draft: `protocol/EVAL-SPEC-v0.1.md`
- Output contract: `protocol/OUTPUT-SCHEMA.json`
- Run manifest contract: `protocol/RUN-MANIFEST-SCHEMA.json`
- Metric definitions: `protocol/METRICS-v0.1.yaml`
- Mode definitions: `protocol/modes/`
- Pilot cases: `cases/pilot/P01`, `cases/pilot/P02`
- Harness utilities: `harness/`

No main-run result should be interpreted from this draft. The v0.1 files are pilot infrastructure, not a frozen preregistration.

## Pilot workflow

```powershell
python evals/harness/validate_cases.py evals/cases/pilot
python evals/harness/make_run_plan.py --cases evals/cases/pilot --repeats 1 --seed 20261006 --output evals/run-plans/pilot-v0.1.json
```

After the eight technical pilot runs:

1. inspect isolation, logging, usage collection, rubric ambiguity, and output normalization;
2. revise the procedure if needed;
3. create the eight new main cases;
4. freeze protocol, cases, rubric, model/settings, budget, and run plan;
5. only then start the 64-run main study.
