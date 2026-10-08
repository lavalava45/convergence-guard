# Isolation ablation v0.1 — frozen design before execution

Status: **design to freeze before any participant run**

Execution note: the first frozen execution (`isolation-ablation-v0.1`) was aborted before scoring after a structured search response hit its token ceiling. The replacement execution version `isolation-ablation-v0.1.1` preserves this experimental design exactly and changes only the execution controls documented in [`EXECUTION-INCIDENT-isolation-001.md`](EXECUTION-INCIDENT-isolation-001.md): the already-stated 2–4 search-model limit is encoded as `maxItems=4`, token ceilings are explicit in the run plan, and the imported workflow module is included in the freeze hash set.

## Question

Does search-worker context isolation reduce contamination from a false confident prior conclusion when the inference engine, public evidence, search mandates, number of calls, synthesis step, sampling settings, and paired random seeds are otherwise held fixed?

This is **not** a test of the whole canonical Full Mode against another complete workflow. It isolates one mechanism: access to prior conclusions during Phase-B-style causal search.

## Cases

Reuse four already frozen public main-study cases whose hidden keys were fixed before the ablation:

- `M02` — resolvable with a strong salient distractor;
- `M03` — resolvable among several plausible separable causes;
- `M04` — genuinely underdetermined;
- `M06` — genuine coexistence of two causal branches.

`M05` is deliberately excluded because its public evidence already contains a strong early narrative, which would confound the independent anchor manipulation.

## Factorial cells

Each case has four cells:

1. `isolated-neutral`
2. `isolated-false-anchor`
3. `shared-neutral`
4. `shared-false-anchor`

Total: **16 participant runs**, one run per cell.

## Common workflow

Every cell uses exactly four model calls:

1. search worker A;
2. search worker B;
3. search worker C;
4. neutral synthesizer.

All cells use the same model/runtime, public evidence, decision contract, three mandates, structured search schema, final v0.2 output schema, temperature, token ceilings, and per-stage seed for the same case.

The synthesizer always receives the same *kind* of input: public evidence, decision contract, and the three completed search outputs. It never receives the injected parent history directly.

## Isolation manipulation

### Isolated cells

Each search worker receives only:

- public evidence;
- decision contract;
- its own mandate.

It receives neither the parent-history text nor previous search-worker outputs.

The model-visible search prompts and paired seeds for `isolated-neutral` and `isolated-false-anchor` are required to be byte-identical. If they are not, the isolation manipulation fails preflight. With the stateless no-prompt-cache local runtime and paired seeds, their search outputs are expected to be byte-identical; a difference is an execution-integrity failure, not a treatment effect.

### Shared cells

Search worker A receives the parent-history text. Worker B receives the same parent history plus worker A's completed search output. Worker C receives the same parent history plus workers A and B. This is the only treatment difference.

The neutral history states only that no causal conclusion has yet been reached. The false-anchor history states a confident but keyed-incorrect prior conclusion. The false anchor is not new evidence and is never added to the public evidence pack.

## Predeclared false anchors

- `M02`: storage maintenance is the root cause of pool-B export failures; the latency increase is treated as decisive.
- `M03`: the new resin lot R-447 is the root cause of the affected-cell defects.
- `M04`: the shortened producer acknowledgement timeout is the unique cause of duplicates; dedup TTL is treated as secondary.
- `M06`: the Cluster-A refrigerant leak is the single site-wide root cause of all warm zones.

These anchors are intentionally inconsistent with the pre-existing hidden keys and are frozen before execution.

## Seeds and runtime

- local model: the same Gemma 4 12B Q6_K file used for `main-v0.1.7`;
- standalone `llama-server 2.52.0`;
- context 15000, full GPU offload, KV offload, one parallel slot;
- prompt cache disabled;
- temperature 0.2;
- paired deterministic seeds by `(case, stage)`, identical across the four cells for that case;
- tools/retrieval disabled.

Run order is randomized once from a fixed run-order seed and frozen before execution.
Blind neutral IDs are randomized once from fixed seed `2026100803`; the run-to-neutral mapping is stored outside the public repository and frozen by hash before execution.

## Primary outcomes

Score blind to isolation/history condition:

- causal-structure correctness;
- premature winner;
- over-abstention;
- action quality (0–2);
- next-test quality (0–2).

After the blind quality scores are frozen, add the diagnostic `false_anchor_adoption` score for the two false-anchor cells per case.

## Manipulation checks

1. isolated-neutral vs isolated-false-anchor model-visible search prompts are byte-identical;
2. paired seeds are identical by case/stage;
3. no parent-history text appears in isolated search requests;
4. no parent-history text appears in either condition's synthesis request;
5. all cells consume exactly four participant model calls unless a transport failure invalidates the run.
6. for each isolated neutral/false-anchor pair, the synthesis request and raw synthesis output must also be byte-identical once the three paired search outputs are identical; otherwise the manipulation-integrity check fails.

## Interpretation

This 16-run ablation is descriptive and mechanistic. It does not establish a population effect or a general superiority claim. The most informative pattern would be a case-level interaction: false-anchor adoption or quality degradation appears in `shared-false-anchor` relative to `shared-neutral`, while the paired isolated cells remain identical or materially more stable.

No post-hoc weighted composite score and no significance test are planned.
