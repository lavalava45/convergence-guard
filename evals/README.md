# Convergence Guard comparative eval

This directory contains the public, reproducible part of the comparative evaluation harness for Convergence Guard.

The eval compares four complete workflows:

1. `single-context`
2. `shared-context-multi-agent`
3. `cg-reduced`
4. `cg-full`

The first stage was a technical pilot: two cases × four modes × one run each = eight runs. The pilot was then followed by the frozen `main-v0.1.7` study: eight new cases × four modes × one repeat = 32 participant runs. The reduction from the earlier two-repeat/64-run draft was declared before the final study version began.

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
- Frozen main-study manifest: `FREEZE-MANIFEST-main-v0.1.7.json`
- Main-study metric report: `results/main-v0.1.7/REPORT.md`
- Main-study interpretation: `results/main-v0.1.7/INTERPRETATION.md` / `INTERPRETATION.ru.md`

The final `main-v0.1.7` result set contains 32/32 completed primary runs, 32/32 completed calibration runs, and 32 blind semantic judgments. The study is descriptive: one model, eight cases, and one repeat per cell do not support broad population claims or a universal mode ranking.

## Reproducing the public eval structure

```powershell
python evals/harness/validate_cases.py evals/cases/pilot
python evals/harness/make_run_plan.py --cases evals/cases/pilot --repeats 1 --seed 20261006 --output evals/run-plans/pilot-v0.1.json
```

Historically, the pilot was used to inspect isolation, logging, usage collection, rubric ambiguity, and output normalization before the main cases were frozen. The final main run plan is `run-plans/main-v0.1.json`; the result aggregate can be regenerated with `harness/aggregate_main_results.py` when the private hidden keys, blind map, and judge-score files are available outside the public repository.

Private ground truth and judge mappings are intentionally not published here. The committed `summary.json`, metric report, and interpretation are the public result artifacts; raw participant run directories remain outside version control.
