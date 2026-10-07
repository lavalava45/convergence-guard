# Main-study automation plan

Goal: execute the 64-run main study without manual participant copy/paste while preserving the information boundaries defined by the evaluation protocol.

## Architecture

### 1. Provider adapter

The runner talks to a stateless model API through a narrow adapter:

- create a call from an explicit message allowlist;
- no inherited chat/session state;
- no account/project memory;
- no retrieval unless explicitly enabled for the case;
- no participant access to the repository or private-key directory;
- expose exact model/version/settings and usage telemetry where the provider supports them.

The adapter must return both the raw provider response and the parsed content. The harness never reconstructs a participant answer from UI-rendered text.

### 2. Mode executors

`single-context`

- one fresh primary context;
- one post-freeze calibration call in the same logical context only if the primary validates.

`shared-context-multi-agent`

- one deliberately shared context;
- Analyst A → B → C → synthesizer;
- persist every journal entry;
- validate/freeze synthesizer primary;
- calibration only after valid freeze.

`cg-reduced`

- one effective context;
- inject frozen CG Reduced instructions and public case material;
- validate/freeze primary;
- calibration only afterward.

`cg-full`

- separate fresh requests/contexts for every isolation-dependent role;
- construct each role's input exclusively from the protocol allowlist;
- never attach prior conversation state implicitly;
- coordinator stores stage outputs but passes only authorized artifacts downstream;
- run only when automated isolation preflight is PASS.

### 3. Artifact pipeline

For every model call persist:

- request manifest without secrets;
- exact authorized input hashes;
- raw response;
- parsed output when applicable;
- parse/validation diagnostics;
- usage telemetry;
- timing;
- retry count and reason.

For every run persist:

- immutable raw primary artifact (`final.raw.json`);
- deterministic normalization audit plus normalized `final.json` under the frozen normalization policy;
- calibration artifact only when the normalized primary is structurally valid;
- integrity hashes;
- final manifest status.

### 4. Structured output policy

Use provider-supported JSON schema / structured output for final and calibration calls where available.

If the provider returns malformed JSON:

- retain raw output unchanged;
- apply the pre-frozen retry policy only;
- never silently repair the answer;
- if retries are exhausted, mark the run invalid/format-failure.

For parseable JSON, apply only the frozen deterministic normalization policy before structural validation. Preserve the raw answer unchanged and record every repair. Normalization must never infer or rewrite substantive reasoning.

### 5. Isolation preflight

Before any main participant run, automatically test and record:

- parent transcript inheritance;
- sibling-output inheritance;
- prior-worker/session history;
- account/project memory;
- retrieval scope;
- filesystem/tool scope;
- coordinator handoff allowlists.

A negative sentinel by itself remains `NO LEAK OBSERVED`, not PASS. PASS requires inspectable runtime/configuration evidence in addition to probes.

### 6. Budget model

Freeze a primary-analysis ceiling that every mode must respect. Recommended telemetry separates:

- primary analysis budget;
- standardized calibration add-on;
- optional judge budget.

Actual consumption may be lower than the ceiling. Full Mode conditional branches must remain inside the same frozen primary ceiling.

### 7. Blind judging

After all participant runs:

1. generate random neutral IDs;
2. write the run-ID ↔ neutral-ID mapping only to the private eval directory;
3. construct judge packets from public case + private key/rubric + neutralized primary answer;
4. run judges without mode names, worker counts, costs, or run IDs;
5. freeze semantic scores;
6. unblind only after scoring is complete.

## Implementation gate

The automation is ready for main-study execution only when a dry-run can:

1. execute P01/P02-equivalent throwaway cases end-to-end;
2. produce no manual copy/paste step;
3. detect malformed JSON cleanly;
4. demonstrate Full Mode isolation PASS;
5. persist reproducible hashes and telemetry;
6. generate blinded judge packets without exposing the mapping to participant or judge contexts.

## Current blocker

A provider-neutral/local runner now exists and LM Studio with `gemma-4-12b-it` has passed the Full Mode isolation preflight and the two-case local technical pilot. The remaining blocker is main-study freeze, not basic runtime feasibility: choose and freeze the actual main model/runtime, resource ceiling, normalization version, eight new cases/private keys, blind-judge pipeline, randomization seed/run plan, and exact harness/CG commits before the first main run.
