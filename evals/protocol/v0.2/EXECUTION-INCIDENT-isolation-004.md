# Isolation execution incident 004 — v0.1.3 used the wrong endpoint

`isolation-ablation-v0.1.3` was aborted after endpoint forensics showed that all 40 saved response artifacts had `metadata.base_url = http://127.0.0.1:1234/v1` rather than the frozen standalone endpoint `http://127.0.0.1:55991/v1`.

The cause was runner plumbing: unlike the main-v0.1.7 batch launcher, `isolation_ablation_runner.py` did not explicitly pass `LMSTUDIO_BASE_URL` to the adapter subprocess, so the adapter fell back to its default endpoint.

All v0.1.3 participant outputs are excluded. No v0.1.3 judging or aggregate result is valid for the frozen isolation design.

Replacement `isolation-ablation-v0.1.4` preserves the experiment design and transport retry policy from v0.1.3 and changes endpoint enforcement only:

- every adapter subprocess is launched with `LMSTUDIO_BASE_URL=http://127.0.0.1:55991/v1`;
- `LMSTUDIO_API_KEY` is removed from that subprocess environment;
- every returned envelope must report the exact frozen endpoint in `metadata.base_url`, otherwise the cell fails closed.

All 16 cells are rerun from scratch under v0.1.4.
