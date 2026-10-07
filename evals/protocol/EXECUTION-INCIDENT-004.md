# Execution incident 004 — main-v0.1.3 aborted before scoring

`main-v0.1.3` completed the four M01 runs and then stopped on the first M02 run (`M02-r1-shared-context-multi-agent`). No judging or scoring was performed. Runs after ordinal 5 were never started. The completed v0.1.3 artifacts are excluded from the final main-study result set.

The failure was a Windows subprocess-transport encoding mismatch. The LM Studio adapter serialized its JSON envelope with literal non-ASCII characters using the process's active Windows stdout encoding, while the parent runner intentionally decoded adapter stdout as UTF-8. M02 produced a non-ASCII byte sequence, causing Python's subprocess reader thread to raise `UnicodeDecodeError` before the response envelope could be consumed.

The replacement execution version is `main-v0.1.4`. It changes only the adapter-to-runner serialization boundary: the adapter now emits its JSON envelope with non-ASCII characters escaped (`ensure_ascii=True`). Parsing the envelope reconstructs the same Unicode strings, so participant prompts, model responses, schemas, normalization, scoring, budgets, runtime profile, case order, and Convergence Guard treatment are unchanged.
