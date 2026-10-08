# Convergence Guard comparative eval

This directory contains the public, reproducible part of the comparative evaluation harness for Convergence Guard.

The original v0.1 eval compares four implemented workflows:

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
- Post-benchmark conformance matrix: `protocol/v0.2/CONFORMANCE-MATRIX.md`
- Main normalization diagnostics: `results/main-v0.1.7/diagnostics/`
- Targeted isolation-ablation: `results/isolation-ablation-v0.1.4/REPORT.md` / `INTERPRETATION.md` / `INTERPRETATION.ru.md`

The final `main-v0.1.7` result set contains 32/32 completed primary runs, 32/32 completed calibration runs, and 32 blind semantic judgments. A later conformance audit found that the executable `cg-full` and `cg-reduced` treatments were simplified implementations rather than complete executions of every current canonical rule. The study is therefore a descriptive **implemented-workflow benchmark**, not a validation of canonical Full Mode or a population effect estimate.

Post-benchmark correction artifacts live under `protocol/v0.2/`. They include a canonical-rule conformance matrix, a self-contained Reduced participant packet, a split causal/action/next-test/protocol-completion output schema, and fail-closed execution semantics for triggered but unsupported stages.

The targeted `isolation-ablation-v0.1.4` tested one mechanism only: exposure to prior conclusions during causal search. It completed 16/16 cells on the frozen standalone endpoint, passed isolated-pair integrity, and produced 0/8 false-anchor adoptions under two independent anchor judges. The result did **not** demonstrate an incremental answer-quality benefit from isolation under that manipulation.

## Reproducing the public eval structure

```powershell
python evals/harness/validate_cases.py evals/cases/pilot
python evals/harness/make_run_plan.py --cases evals/cases/pilot --repeats 1 --seed 20261006 --output evals/run-plans/pilot-v0.1.json
```

Historically, the pilot was used to inspect isolation, logging, usage collection, rubric ambiguity, and output normalization before the main cases were frozen. The final main run plan is `run-plans/main-v0.1.json`; the result aggregate can be regenerated with `harness/aggregate_main_results.py` when the private hidden keys, blind map, and judge-score files are available outside the public repository.

Private ground truth and judge mappings are intentionally not published here. The committed `summary.json`, metric report, and interpretation are the public result artifacts; raw participant run directories remain outside version control.

## Reproducibility boundary

The repository provides **public auditability, not a public-only full replay of the original experiment**. Available materials include participant-visible cases, frozen run plans and freeze manifests (with SHA-256 references), protocol/harness source, normalized aggregate `summary.json`, interpretations and generated reports. The published source and tests allow procedural checks, and the reports allow readers to inspect declared metrics and limitations.

Private hidden answer keys, case truth labels, blind mappings and individual judge-score files were stored outside the repository to preserve the experimental information boundary. The original model endpoint and environment, along with private adjudication materials, are also required for strict end-to-end regeneration. Consequently, **the original blind scoring and aggregates cannot be fully rederived from this public checkout alone**. Do not describe hash manifests or unit tests as independent validation of scientific ground truth.

The main benchmark must be read as a comparison of **implemented** workflows rather than a canonical-Full efficacy test; the targeted isolation experiment found no incremental quality advantage under its explicit anti-anchor warning. The v0.1.4 generated report carries a documented heading typo (`v0.1.2`); see the [isolation result index](results/isolation-ablation-v0.1.4/README.md), rather than modifying frozen outputs to correct its appearance.
