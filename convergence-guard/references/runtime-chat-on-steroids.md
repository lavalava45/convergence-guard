# Chat On Steroids Runtime Profile

This file describes the local Chat On Steroids integration used by the original Convergence Guard development environment. It is **not** part of the universal method.

Read it only when running Convergence Guard inside Chat On Steroids.

## Native execution path

Use Chat On Steroids Core for project facts: files, code, logs, Git, commands, and local state.

Use the native `agents` mechanism for Full Mode operations that require genuine isolation or blindness.

## v0.2.1 worker topology

A normal three-finalist Full Mode run uses approximately nine worker contexts:

```text
Phase B
3 isolated causal-search workers
(+1 or +2 only if the coverage gate fails)

Phase C
1 fresh contract screener
1 fresh blind causal mapper
(+1 boundary critic only if map ambiguity is decision-relevant)

Phase D
1 fresh dossier worker per finalist (2–3)
1 fresh slate-level adjudicator
(+1 independent second opinion only when triggered)

Optional before search
+1 independent reframe reviewer when framing risk is material
```

The screener and blind mapper should be spawned concurrently after candidate neutralization because each must remain blind to the other's output.

The default initial search cohort is three **fresh worker contexts**, not five. This is a requirement on the number of independent search contexts, not on simultaneous worker concurrency.

Chat On Steroids worker capacity is a runtime setting and may change. If the configured number of simultaneous worker slots is lower than the number of fresh contexts required by a stage, execute that stage in capacity-limited batches while preserving the same blindness and context-boundary rules. For example, with two slots the initial three-worker search cohort runs as `2 + 1`; with three or more slots, all three may launch together.

The current configured limit is **three simultaneous worker slots**, so the normal initial Phase B cohort of three fresh search workers can be launched concurrently.

Any later worker in a batched stage must still be fresh and must receive only the stage-authorized inputs. It must not receive outputs or conclusions from workers that completed earlier merely because those outputs now exist in the parent run.

Likewise, the approximately eight or nine worker contexts used by a typical Full Mode run are counted across the whole protocol. They do **not** imply that eight or nine workers must run concurrently.

Expand the search cohort to four or five fresh worker contexts only after the coverage gate identifies a genuine missing causal region.

## Fresh-context rules

Do not reuse a worker for a role whose value depends on blindness to material it has already seen.

In particular:

- search workers must not see other search outputs;
- the screener must not see the mapper's output;
- the mapper must not see screening results;
- dossier workers should see one finalist only;
- the slate adjudicator must be fresh relative to search, screening, mapping, and dossier authorship;
- a second-opinion reviewer must not see the adjudicator's winner or coordinator preference.

A worker may receive all relevant real-world evidence. Independence means removing prior conclusions and preference signals, not withholding facts required for judgment.

## Context-boundary integrity

A native `agents` worker conversation is necessary for Full Mode in this runtime, but it is not by itself sufficient evidence of context isolation.

A fresh worker may receive ambient context that was not explicitly included in its `context` or `task`, including parent-conversation, user-specific, memory, history, or project-level context supplied by the host.

Therefore distinguish:

**Worker separation** — sibling workers do not directly receive each other's task/output.

**Context isolation** — a worker also does not receive decision-relevant prior conclusions, framing, preferences, or candidate information through any other context channel.

Full Mode requires the second property wherever the protocol depends on isolation or blindness.

For isolation-dependent roles, the explicit stage payload is an allowlist. Decision-relevant information inherited through parent history, memory, project context, shared summaries, retrieval, or persisted worker history is contamination unless that information is explicitly authorized for the stage.

If a previously known real-world fact is needed, restate it in the factual brief with provenance. Do not rely on ambient project or conversation memory to supply it.

A sleeping worker revived through `agents message` retains its existing worker history and therefore is not fresh for any later role that requires blindness to material already present in that history.

### Isolation preflight

Before relying on Full Mode after a Chat On Steroids/runtime update, and before publishing benchmark results that depend on worker isolation, run a small non-sensitive context-boundary smoke test.

Use synthetic sentinel labels only; never use private user data.

Test three boundaries:

1. **Parent boundary**  
   Place a harmless sentinel declaration only in the prime conversation. Spawn a fresh worker without including that declaration in its explicit task/context. Ask only whether a sentinel with that label is present in its initial context; do not ask it to reveal hidden content.

2. **Sibling boundary**  
   Give a harmless sentinel declaration only to worker A. Spawn worker B independently. Ask B only whether sibling-task material with that sentinel label is present; do not ask for its value or content.

3. **Persistence boundary**  
   Verify that reviving a sleeping worker preserves its own prior history. Treat this as a positive control and never reuse such a worker for a role that requires blindness to that history.

Record each boundary as:

- `PASS` — forbidden ambient context was not visible;
- `FAIL` — forbidden ambient context was visible;
- `INCONCLUSIVE` — the runtime does not allow the boundary to be tested reliably.

A `FAIL` or material `INCONCLUSIVE` on a boundary required by the planned operation means that operation must not be labeled Full Mode.

Passing isolation preflight does **not** constitute Phase B and does not satisfy Full Mode by itself. After preflight, continue with the required fresh search cohort unless the activation gate determines that Full Mode is unnecessary for the case.

## Do not bypass the native agent binding

Do not launch Codex CLI, Claude Code, OpenCode, DevSpace, or another separate AI process solely to simulate Convergence Guard workers unless the user explicitly allows that runtime.

Do not invoke workers through `curl`, hidden local HTTP, direct IPC, terminal hacks, or another transport that bypasses Chat On Steroids' parent/worker binding.

Before a long Full Mode run, verify actual `agents` reachability once using the native status mechanism. Seeing `agents` in a published tool schema is necessary but not sufficient.

If multi-agent support is enabled but `agents` is not visible in the current conversation, treat that as a tool-publication or session-binding problem rather than evidence that Chat On Steroids lacks worker support.

If a real call fails before reaching local Core with a connector/session error such as `tool has been disabled` or `FORBIDDEN`, do not retry blindly in the same broken binding. Repair or recreate the relevant connection/session first.

Until isolated workers are both visible and callable, do not present sequential reasoning in the parent context as Full Mode. Use [Reduced Mode](reduced-mode.md) only with explicit user consent.

## User interface discipline

Do not take over the user's screen, active window, mouse, or focus for background analytical work.

If a task genuinely requires GUI interaction, follow the active project rules and obtain any required permission before taking focus.

## Recovery after a long run

Do not restart the whole protocol automatically after a delay, reload, or lost worker binding.

Recover in this order:

1. collect outputs from workers that already completed;
2. identify exactly which phase operations are missing;
3. rerun only the missing workers or checks;
4. preserve frozen screening/mapping artifacts when they remain valid;
5. continue from the nearest incomplete operation;
6. never replace a lost isolated result with an unmarked sequential reconstruction in the parent context.

Do not switch to another external agent runtime for recovery without explicit user permission.

## Local execution summary

```text
Chat On Steroids Core
→ evidence and project state
→ agents: isolated worker conversations
→ frozen blind-stage artifacts
→ fresh slate adjudication
→ convergence in the parent conversation
```
