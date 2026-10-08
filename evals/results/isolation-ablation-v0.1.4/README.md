# Isolation ablation v0.1.4 — result index

Start with [`INTERPRETATION.md`](INTERPRETATION.md) or the [Russian interpretation](INTERPRETATION.ru.md).

Files in this directory have different roles:

- `summary.json` — machine-readable aggregate;
- `REPORT.md` — frozen generated two-judge consensus table;
- `INTERPRETATION.md` / `INTERPRETATION.ru.md` — human-readable interpretation, execution provenance, limitations, and evidence boundary.

## Important report note

The frozen aggregator contains a presentation-only heading typo and therefore generates `REPORT.md` with `Isolation ablation v0.1.2` in its first line. The valid experiment is `isolation-ablation-v0.1.4`; that identity is recorded in `summary.json`, the run plan, freeze manifest, private blind map, and result directory.

The typo is intentionally **not** patched in the generated report because the current repository keeps the aggregator byte-identical to the SHA-256 frozen before v0.1.4 execution. This preserves exact result-generation provenance.

`REPORT.md` is a compact generated table, not the complete methodological interpretation. In particular, the shared-history treatment explicitly warned workers that inherited conclusions were **“NOT EVIDENCE”** and instructed them to re-check those conclusions. That anti-anchoring instruction is a material limitation of the isolation test and is discussed in full in `INTERPRETATION.md`.

No participant output, blind score, consensus mapping, or aggregate metric is changed by this presentation erratum.
