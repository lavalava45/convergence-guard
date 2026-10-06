# Why autonomous AI agents fail on long-running real-world tasks: a Convergence Guard Full Mode case study

[Русская версия](long-running-autonomous-agents-full-mode.ru.md)

> **Methodological case-study disclaimer.** This document is a worked example of Convergence Guard, run on 2026-10-06 against publicly available research and benchmark evidence. It is **not** a controlled laboratory study performed by the authors of this repository, a new agent benchmark, or an independent replication of the cited experiments. The run had no privileged access to unpublished benchmark traces, private deployment telemetry, model-provider internals, or proprietary production incidents. Its conclusions are therefore claims about what the cited public evidence supports under the protocol's rules, not a substitute for primary empirical work.

## Question

Why do modern autonomous AI agents still become unreliable on long-running real-world tasks that require sustained planning, tool use, changing-state understanding, verification, memory, recovery, and completion? Which causal mechanisms best explain the horizon-dependent drop in end-to-end reliability, and which intervention class should be prioritized?

The run was required to separate:

1. **local capability** — whether the model can choose a good next step in isolation;
2. **system reliability** — whether a sequence of steps remains correct and recoverable as state changes;
3. **task complexity** — dependency depth, branching, coordination, and verification burden;
4. **runtime architecture** — memory, state representation, tool semantics, checkpoints, rollback, retries, and handoffs.

The run was also forbidden from assuming that “longer task” is itself a sufficient causal explanation.

## Why this case is useful for Convergence Guard

The topic is unusually vulnerable to premature convergence because many plausible explanations can be true at the same time:

- small local errors can compound;
- planning becomes harder as dependency depth and branching increase;
- tools mutate external state, sometimes irreversibly;
- observations can be stale, partial, or ambiguous;
- failures can remain undetected for many steps;
- context, memory, and handoffs can lose task-relevant state;
- additional scaffolding can either help or create new failure surfaces;
- stronger base models can improve capability without proportionally improving reliability.

A conventional analysis can therefore produce a long list of “causes” without distinguishing root mechanisms, mediators, moderators, and downstream symptoms.

The decision problem is not merely:

> Why do agents fail?

It is:

> **Which causal structure predicts when a locally capable agent will become an unreliable long-horizon system, and which intervention remains useful across the surviving causal models?**

# Phase A — evidence brief and decision contract

## Decision contract

**Decision question:** Which causal families best explain the loss of end-to-end reliability as autonomous tool-using tasks become longer and more interdependent, and what intervention should be prioritized under current evidence?

**Scope:** The primary evidence base covers software, computer-use, web/API, and benchmarked digital-agent tasks. The run may reframe “long horizon” into policy complexity, state continuity, observability, and recovery, but it may not generalize benchmark results to robotics, social systems, or open-ended enterprise operations without qualification.

**Target phenomenon:** A system that can often perform short or local subtasks correctly nevertheless fails to complete a longer real-world task reliably.

**Required causal chain:** Where possible, explanations must distinguish:

```text
task demands
→ first material error or state divergence
→ detection / verification
→ recovery, rollback, retry, or replanning
→ continuation
→ terminal task outcome
```

**Forbidden substitutions:**

- human task duration → literal number of agent steps;
- long context → proof that memory is the root cause;
- high benchmark capability → high operational reliability;
- high single-run success → consistent reliability across repeated runs;
- agent self-critique → reliable failure detection;
- more inference or more agents → independent evidence;
- a late invalid action → the root cause of the trajectory;
- successful completion → proof that the trajectory was safe or internally correct;
- `p^n` intuition → established model of long-horizon failure;
- recovery on one benchmark → universal recovery mechanism.

**Model-discrimination criterion:** A surviving causal model must make discriminating predictions about at least one of the following:

- probability of the first consequential error;
- probability of detecting that error;
- probability of recovering after it;
- propagation of error into later steps;
- sensitivity to state mutability or observability;
- sensitivity to dependency depth or branching;
- sensitivity to memory/handoff architecture;
- effect of verification, rollback, retry, or replanning;
- final task success under controlled changes to those variables.

**Action success criterion:** An intervention is better when, under matched tasks and model capability, it reduces terminal failure and unsafe side effects while preserving acceptable task quality, latency, and cost. Improvements that merely move failures, hide them, or increase unrecoverable side effects do not count as success.

**Cost of error:** Misdiagnosing the bottleneck can produce expensive but weak interventions. Adding more planning compute does little if the dominant problem is stale state after side effects; adding memory does little if the first-error hazard is driven by policy complexity; adding verification does little if the verifier cannot localize failure or the action cannot be reversed.

**Reversibility:** Prefer early interventions that can be introduced, observed, and rolled back at the orchestration/runtime layer without committing to irreversible model retraining or platform-wide architecture changes. A production-wide persistent-state redesign is more locking than targeted verification at selected commit boundaries.

**Analysis budget:** This public case study is limited to the inspectable evidence available to the run on 2026-10-06 and does not perform new benchmark experiments. Material source/provenance gaps may trigger targeted evidence checks; empirical questions that require new controlled runs remain experiments rather than being filled with additional argument.

## Claim-level source policy

The run treated benchmark and paper reputation as metadata, not as truth labels.

For material claims it asked:

- What is actually measured?
- Is the benchmark task-level, step-level, or trajectory-level?
- Does “horizon” mean elapsed wall-clock time, human task duration, action count, token count, or compositional depth?
- Are task environments static or mutable?
- Are failures automatically verifiable?
- Does the intervention change the base model, the scaffold, or the environment?
- Is a reported gain from preventing first errors, detecting them, recovering from them, or merely selecting a better run?
- Do several sources reuse the same task families or evaluation assumptions?
- Is a result peer-reviewed, preprint-only, or a project report?
- Does the evidence support causation, correlation, or only feasibility?

Source roles are used in the sense of the protocol: `EVIDENCE`, `CORROBORATION`, `CONTEXT`, `LEAD ONLY`, or `UNSUPPORTED`.

### Source-role map for material uses

| Source group | Role in this run | Material use / dependency note |
|---|---|---|
| HCAST + METR | EVIDENCE / CORROBORATION | horizon-dependent success; overlapping software-task framing means they are not counted as fully independent evidence |
| HORIZON | EVIDENCE | controlled compositional-depth degradation and cross-domain failure patterns |
| Traverse | EVIDENCE | first-error, detection, recovery, cascade, and diffuse-failure measurements |
| ToolSandbox, τ-bench, τ²-bench | EVIDENCE / CORROBORATION | stateful tool use, repeated-run reliability, and shared-state coordination |
| Rabanser et al. | CORROBORATION | capability/reliability separation across multiple reliability dimensions |
| DeepVerifier, GUI-RobustEval/RoTS | EVIDENCE | specialized verification and recovery are measurable intervention surfaces |
| Atomix, AgentRewind | EVIDENCE | transactional/checkpoint runtime mechanisms can change recovery outcomes |
| AMA-Bench | EVIDENCE | persistent memory quality depends on causal/objective state representation, not only retrieval volume |
| MD5 state-tracking experiment | EVIDENCE (counterexample) | long dependent chains can succeed under controlled state/tool semantics; weakens “length alone” |
| UltraHorizon | CORROBORATION | extreme-horizon gap and evidence that simple scaling alone is insufficient in that benchmark |

## Main factual anchors

### 1. Success falls sharply as tasks move into longer human-equivalent durations

HCAST introduced 189 software-related tasks with 563 human baselines totaling more than 1,500 hours. In the reported evaluation, frontier agents succeeded on roughly **70–80%** of tasks taking skilled humans less than one hour, but on **less than 20%** of tasks taking humans more than four hours.

This is strong evidence for a horizon-dependent reliability gap in the tested task distribution.

It does **not** show that elapsed duration itself is the mechanism. Human completion time is a proxy for task difficulty and scope, not a direct count of agent actions or state transitions.

Sources:

- [Rein et al., *HCAST: Human-Calibrated Autonomy Software Tasks* (2025)](https://arxiv.org/abs/2503.17354)
- [METR, *Task-Completion Time Horizons of Frontier AI Models* — updated 2026-05-08](https://metr.org/time-horizons/)

METR's current methodology uses over one hundred diverse software tasks and explicitly notes that measurements above 16 human-hours are unreliable with the available suite. The run therefore treated the existence of horizon degradation as stronger evidence than any claim about an exact universal “hours of autonomy” limit.

### 2. Controlled compositional depth produces breaking regions rather than one smooth universal curve

HORIZON was designed to vary intrinsic task horizon more directly. It collected **3,100+ trajectories** across web navigation, operating systems, databases, and embodied tasks while increasing dependency and compositional depth.

The reported pattern is not merely “more steps, slightly worse.” Performance enters task-dependent breaking regions as compositional horizon grows, and the failure mix differs by domain.

This is evidence against a single universal “context length” explanation and supports a **policy-complexity / compositional breakpoint** family.

Source: [Wang et al., *The Long-Horizon Task Mirage? Diagnosing Where and Why Agentic Systems Break* (2026)](https://arxiv.org/abs/2604.11978).

### 3. After a first error, agents often fail to detect or recover from it

The 2026 Traverse study analyzed **2,518 agent trajectories** across software engineering, computer use, and science and classified **6,967 mistakes** into 78 failure types.

Its trajectory-level findings show a recurring failure signature:

- after a first localizable mistake, the agent recovered in only **30.5%** of applicable runs;
- in **38.5%**, its reasoning never flagged the error;
- in **72.6%**, it kept acting or declared completion without correcting it;
- in software engineering, a wrong step was followed by another wrong step **40.4%** of the time versus **3.0%** after a correct step — about **13.7×** higher;
- in computer use, the analogous rates were **58.1%** versus **5.3%** — about **10.9×** higher.

This is direct evidence that long-horizon failure is often **correlated and path-dependent**, not well modeled as a sequence of independent identical trials.

The same paper also reports an important boundary: **588 failed runs, 23% of all 2,518 trajectories, had no single decisive first mistake**. Long-horizon reliability therefore cannot be reduced to one universal “find the first mistake” theory.

Source: [Rahman et al., *Locating Hidden Failures Makes Long-Horizon Agents More Reliable* (2026)](https://arxiv.org/abs/2609.17930).

### 4. Environmental feedback can matter as much as agent self-awareness

Traverse reports a cross-domain contrast: software-engineering agents often fail to notice their own mistake but can still recover because tests, tracebacks, compiler errors, and other environmental signals expose the problem. Computer-use environments often provide weaker or more ambiguous correction signals, and recovery is much lower.

This supports a **closed-loop state integrity** model in which the important unit is not the reasoning step alone, but the loop:

```text
observe authoritative state
→ check assumptions
→ act
→ observe consequences
→ verify postconditions
→ repair / rollback / replan or continue
```

### 5. Stateful tool use is harder than stateless tool calling

ToolSandbox explicitly evaluates stateful execution, implicit dependencies between tool calls, on-policy conversation, and intermediate milestones. Its authors report that tasks involving **State Dependency**, **Canonicalization**, and **Insufficient Information** remain challenging even for strong models.

The result is mechanistically relevant to the causal hypothesis: a tool call can be locally valid while being globally invalid because it was made against the wrong state, in the wrong order, or without information that should have been obtained first.

Source: [Lu et al., *ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities*, Findings of NAACL 2025](https://aclanthology.org/2025.findings-naacl.65/).

### 6. Reliability across repeated runs can remain poor even when pass@1 looks respectable

In τ-bench, state-of-the-art function-calling agents in the original evaluation completed **less than 50%** of tasks, and repeated-run consistency was substantially worse: retail `pass^8` was reported below **25%**.

This separates “the agent can sometimes solve it” from “the system is dependable when the same task class is attempted repeatedly.”

Source: [Yao et al., *τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains*, ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/hash/1b126cc38b8638e07bef37e7b2bb72bf-Abstract-Conference.html).

### 7. Shared mutable state and coordination add a distinct failure surface

τ²-bench extends the setting so that both an agent and a user can act on a shared dynamic environment. In its telecom domain, moving from no-user control to **dual control** produces significant performance drops.

The benchmark separately analyzes reasoning errors and communication/coordination errors. A system can therefore fail even when participants are locally competent because they disagree about who changed what, which action has already happened, or which state now holds.

Source: [Barres et al., *τ²-Bench: Evaluating Conversational Agents in a Dual-Control Environment*, ICML 2026](https://proceedings.mlr.press/v306/barres26a.html).

### 8. Reliability does not automatically track headline capability gains

Rabanser et al. define twelve metrics across consistency, robustness, predictability, and safety and evaluate **15 models** on two agent benchmarks. Their central result is that recent capability gains yield only **small improvements in reliability** on those dimensions.

This weakens the hypothesis that the long-horizon problem can be solved simply by waiting for a stronger next-token policy.

Source: [Rabanser et al., *Towards a Science of AI Agent Reliability*, ICML 2026](https://proceedings.mlr.press/v306/rabanser26a.html).

### 9. Specialized verification can improve outcomes, but generic self-judgment is not enough

DeepVerifier uses rubric-guided verification for deep-research agents. The reported verifier outperforms vanilla agent-as-judge and LLM-judge baselines by **12–48%** in meta-evaluation F1 and yields **8–11% accuracy gains** on challenging subsets of GAIA and XBench-DeepResearch when used for iterative test-time refinement with capable closed-source models.

Traverse independently shows that general frontier judges can be poor at first-error localization: even the strongest evaluated judge correctly localized the first mistake in fewer than one third of organic-failure runs.

Together these findings support two claims:

1. verification is a real intervention surface;
2. “ask a strong model to check the trajectory” is not automatically a reliable verifier.

Sources:

- [Wan et al., *Inference-Time Scaling of Verification: Self-Evolving Deep Research Agents via Test-Time Rubric-Guided Verification*, Findings of ACL 2026](https://aclanthology.org/2026.findings-acl.1243/)
- [Rahman et al., Traverse (2026)](https://arxiv.org/abs/2609.17930)

### 10. Recovery can be trained and benchmarked directly

GUI-RobustEval contains **1,216 executable test cases** designed to measure recovery from policy-induced GUI errors. The associated robustness-driven trajectory synthesis method trains models on recovery behavior.

RoTS-32B reports **47.4% success on OSWorld** and **33.8% All-Pass@4**, with stronger recovery behavior than the compared open baseline.

The important causal point is not the absolute leaderboard score. It is that recovery can be treated as a distinct trainable and measurable capability instead of being hidden inside final success.

Source: [Bu et al., *Recovering Policy-Induced Errors: Benchmarking and Trajectory Synthesis for Robust GUI Agents*, ICML 2026](https://proceedings.mlr.press/v306/bu26b.html).

### 11. Transactional tool semantics can prevent external side effects from amplifying failure

Atomix treats multi-step tool effects more like transactions: calls are tracked, some effects can be delayed, commit can depend on progress conditions, and externalized effects can be compensated on abort.

Under fault injection, the authors report that transactional retry improves task success and that progress-aware commit strengthens isolation under speculation and contention.

This does not prove that every agent should use database-style transactions. It shows that some apparent “agent reasoning failures” can be converted into recoverable execution failures by changing the semantics around state mutation.

Source: [Mohammadi et al., *Atomix: Timely, Transactional Tool Use for Reliable Agentic Workflows* (2026)](https://arxiv.org/abs/2602.14849).

### 12. Checkpointing both agent context and environment state can improve recovery

AgentRewind records aligned checkpoints of agent context and controlled environment state, then allows the system to return to an earlier point and resume execution while preserving useful information from the failed attempt.

Across its long-horizon engineering benchmark and evaluated configurations, the authors report improved task success and checklist progress over compared baselines.

This is evidence for the hypothesis that recovery is architectural: rewinding text alone is insufficient when the external world has already changed.

Source: [Zhuang et al., *AgentRewind: Recoverable Execution for Long-Horizon LLM Agents* (2026)](https://arxiv.org/abs/2608.14380).

### 13. Long memory is not equivalent to good state representation

AMA-Bench evaluates agent memory over trajectories consisting of states, actions, observations, and tool outputs. The authors report that existing memory systems underperform partly because they lose **causal and objective information** and rely heavily on lossy similarity retrieval.

Their causality-graph and tool-augmented AMA-Agent reaches **57.22%** accuracy, **11.16 percentage points** above the strongest reported baseline.

This supports the persistent-state family while also narrowing it: the issue is not merely “remember more tokens,” but preserve the task-relevant structure needed to reconstruct current state and unresolved obligations.

Source: [Zhao et al., *AMA-Bench: Evaluating Long-Horizon Memory for Agentic Applications*, ICML 2026](https://proceedings.mlr.press/v306/zhao26bs.html).

### 14. A controlled 196-call task is a counterexample to “length alone causes inevitable collapse”

A 2026 preprint tests exact state tracking by making a model execute MD5 through **196 dependent tool calls across 64 rounds**, with every intermediate state checked against a ground-truth trace.

In the reported setup, gpt-oss-120b carried the state through the full chain and returned the correct digest on a majority of completed deterministic-tool runs.

This experiment is narrow and does not resemble an open-ended real-world task. That is exactly why it is useful here: it demonstrates that **a long dependent call chain is not sufficient by itself to cause failure** when interpretation is simple, state is exact, tools are controlled, and verification is strong.

Source: [Pai & Xian, *Long-Horizon State Tracking in LLMs: Executing MD5 through a Deep Sequence of Dependent Tool Calls* (2026)](https://arxiv.org/abs/2609.00012).

### 15. Ultra-long-horizon benchmarks preserve the gap even when simple scaling is tried

UltraHorizon evaluates long-horizon, partially observable exploration tasks. Standard trajectories exceed **35k tokens and 60 tool calls** on average; the heaviest settings exceed **200k tokens and 400 tool calls**.

The authors report that state-of-the-art agents remain substantially below human performance, that simple scaling does not solve the benchmark, and that observed failures cluster around in-context locking and fundamental capability gaps.

This supports keeping more than one causal family alive: some failures are architectural and recoverability-related, while others reflect genuine policy-capability limits.

Source: [Luo et al., *UltraHorizon: Benchmarking Agent Capabilities in Ultra Long-Horizon Scenarios*, ICML 2026](https://proceedings.mlr.press/v306/luo26ai.html).

# Phase A reframe — what exactly is “the horizon problem”?

The outside-view check changed the framing.

A naive formulation is:

> More steps mean more chances to be wrong; therefore long tasks fail because errors multiply.

That is directionally plausible but causally incomplete. If every step had independent correctness probability `p`, an `n`-step success rate might resemble `p^n`. But the evidence violates the assumptions of that toy model:

- errors are **correlated** after a first mistake;
- some mistakes are recoverable and others are not;
- some environments expose errors quickly and others hide them;
- some failures are diffuse rather than traceable to one first mistake;
- task complexity can rise non-linearly with dependency depth;
- shared state and side effects create path dependence;
- long deterministic chains can succeed when state and verification are tightly controlled.

The run therefore reframed terminal failure as the interaction of at least two broad hazards:

1. **entry into a bad trajectory** — the chance of a material planning, reasoning, coordination, perception, or execution error;
2. **failure to contain that error** — the chance that the system does not detect, reverse, compensate, or replan before the error contaminates later state.

A third factor governs persistence across time and actors:

3. **loss of task state** — the chance that the system no longer has a faithful representation of what is true, done, pending, verified, or owned.

This decomposition is conceptual, not a fitted probabilistic law.

# Phase B — isolated causal search

The completed run used four causally distinct search regions. The public write-up summarizes the mandates rather than reproducing worker-specific reasoning.

## Mandate 1 — error propagation, observability, and recovery

Search for mechanisms in which a locally survivable error becomes terminal because:

- the environment does not expose it;
- the agent fails to notice it;
- verification is delayed or weak;
- side effects mutate later preconditions;
- rollback or compensation is unavailable;
- replanning occurs from already-corrupted state.

This region produced models around post-first-error cascade, weak observability, transactionality, and recovery capacity.

## Mandate 2 — effective policy complexity

Search for failure that remains even in relatively static, observable, and reversible environments.

Focus on:

- dependency depth;
- branching and contingent planning;
- decomposition;
- search over action sequences;
- long-range constraints;
- plan adaptation;
- allocation of test-time reasoning compute.

This region produced a **policy-complexity breakpoint** model: beyond a task-dependent region, the policy fails to construct or maintain a sufficiently good action plan even before state corruption becomes the main issue.

## Mandate 3 — persistent state, memory, and coordination architecture

Search for mechanisms in which the problem is not one bad local action but loss of a coherent representation of:

- current world state;
- completed work;
- unresolved obligations;
- causal dependencies;
- ownership and handoff state;
- what has been verified;
- what must not be repeated.

This region included memory systems, externalized state, checkpointing, context compaction, shared-state coordination, and handoffs.

## Mandate 4 — capability/reliability separation and counterexamples

The coverage gate retained an additional region because the first three could otherwise treat horizon degradation as self-evident.

This region searched for:

- long chains that **do** work;
- cases where stronger models improve local capability but not reliability proportionally;
- benchmark confounds;
- differences between human duration and agent action horizon;
- interventions that change runtime semantics without changing model weights.

The MD5 state-tracking result, reliability work, and transactional/recovery studies were especially important because they prevent “long = doomed” from becoming an unfalsifiable explanation.

## Coverage gate

Coverage was judged sufficient after the fourth region because the surviving candidate space included:

- first-error generation;
- error propagation and containment;
- mutable-state / partial-observability effects;
- persistent-memory and coordination effects;
- policy-complexity limits;
- runtime/scaffold effects;
- counterexamples to length-only explanations.

No additional branch was needed to create a materially different causal region.

# Phase C — neutral candidates, screening, and blind causal mapping

Candidate wording was neutralized before reduction. Screening and causal mapping were performed as separate fresh operations in the original run.

## Screening result

Three distinct model families remained viable:

- **F1 — CLOSED-LOOP STATE INTEGRITY**
- **F2 — EFFECTIVE POLICY-COMPLEXITY BREAKPOINT**
- **F3 — PERSISTENT-STATE & COORDINATION ARCHITECTURE**

A pure independent-`p^n` accumulation model was retained only as a weak baseline intuition, not a finalist.

A pure “context window size” model did not survive as a standalone family because memory effects were better represented inside F3, and because long controlled sequences can succeed.

A pure “tool unreliability” model was also demoted: tool failures matter, but the stronger causal distinction is whether failures alter canonical state and whether the system can detect and recover from them.

## Blind causal map

### F1 — CLOSED-LOOP STATE INTEGRITY

**Claim:** The dominant long-horizon reliability loss in many state-changing tasks occurs because local errors or stale assumptions are allowed to persist into canonical state without sufficiently fast detection, verification, rollback, retry, or replanning.

**Core mechanism:**

```text
state estimate
→ action
→ external state mutation
→ incomplete / stale observation
→ undetected mismatch
→ later decisions conditioned on wrong state
→ correlated cascade
```

**Primary predictions:**

- wrong steps sharply raise downstream error risk;
- richer environment feedback improves recovery;
- stronger postcondition checks reduce terminal failure even without changing the base model;
- rollback/compensation matters most around state-changing actions;
- the same policy performs better in instrumented, reversible environments than in opaque, irreversible ones.

### F2 — EFFECTIVE POLICY-COMPLEXITY BREAKPOINT

**Claim:** Long-horizon degradation partly reflects a nonlinear increase in the difficulty of constructing and adapting a policy as dependency depth, branching, constraints, and subgoal interactions grow.

**Core mechanism:**

```text
more interdependent obligations
→ larger effective policy/search problem
→ decomposition or planning quality crosses a task-dependent threshold
→ first material error probability rises sharply
```

**Primary predictions:**

- a sharp break can remain in static, fully observable, reversible tasks;
- increasing dependency depth hurts more than adding equivalent independent work;
- extra state verification helps after errors but does not eliminate the rise in first-error hazard;
- better hierarchical planning or targeted test-time search shifts the breakpoint.

### F3 — PERSISTENT-STATE & COORDINATION ARCHITECTURE

**Claim:** Long tasks become unreliable when the system lacks a durable, causally meaningful representation of state, commitments, progress, ownership, and unresolved requirements across context growth, handoffs, retries, or multiple actors.

**Core mechanism:**

```text
history grows / actors change / context is compacted
→ task-relevant state is summarized, retrieved, or handed off imperfectly
→ current belief state diverges from canonical task/world state
→ duplicated, omitted, conflicting, or misordered work
→ terminal inconsistency
```

**Primary predictions:**

- failures increase around compaction, resume, handoff, or multi-actor boundaries;
- explicit persistent state helps even without increasing base-model reasoning;
- causally structured memory beats similarity-only retrieval for stateful tasks;
- coordination failures appear when multiple parties can mutate shared state.

## Relations between finalists

The mapper marked these families as primarily **INTERACTING**, not mutually exclusive.

A common causal composition is:

```text
F2 raises the hazard of the first consequential error
          ↓
F1 determines whether that error is detected and contained
          ↓
F3 determines whether a coherent state survives across time, retries, and handoffs
```

But the weighting is task-class dependent. A static theorem-search or code-design problem may be dominated by F2. A GUI or operational workflow with irreversible side effects may be dominated by F1. A multi-session or multi-actor workflow may expose F3 most strongly.

## Boundary audit

The main boundary question was whether F1 and F3 were duplicates.

They were kept separate because they make different predictions:

- F1 can fail in a single uninterrupted session with perfect memory if the system acts on stale state and does not verify consequences.
- F3 can fail even when each local action is verified if the system loses a durable representation of commitments or ownership across handoffs and context transitions.

Likewise, F2 was not collapsed into F3 because policy complexity can create a breakpoint in a static environment where memory and external state are controlled.

# Phase D — independent finalist dossiers

## Finalist A — closed-loop state integrity

### Mechanism

A long-running agent is a feedback controller embedded in a changing environment. It does not merely produce text; it repeatedly estimates state, chooses actions, observes consequences, and updates beliefs.

Reliability degrades when this loop is open or weakly closed:

1. the agent acts from an incomplete state estimate;
2. the tool, user, or environment changes the world;
3. the agent receives ambiguous, delayed, or partial evidence of the result;
4. it does not re-read authoritative state;
5. it fails to check a postcondition;
6. downstream decisions inherit the mismatch;
7. recovery becomes more expensive as side effects accumulate.

### Strongest support

- Traverse directly measures correlated post-error cascades and low recovery.
- ToolSandbox exposes difficulty with implicit state dependencies.
- τ²-bench shows degradation when another actor can mutate shared state.
- GUI-RobustEval makes recovery itself a measurable capability.
- Atomix and AgentRewind show that commit, rollback, compensation, and checkpoint semantics can change outcomes without changing the underlying model.

### Strongest contrary evidence / limitations

- Many failures begin as reasoning or planning errors before any consequential state mutation.
- A substantial subset of failed trajectories has no single localizable first mistake.
- HORIZON shows breaking regions where policy complexity is itself substantial.
- Stronger verification can be expensive and can itself be wrong.

### What this model explains better than the nearest competitors

It explains why an agent that is locally capable can still fail catastrophically after one wrong action, and why the same policy can behave differently in environments with strong versus weak feedback.

### What it does not uniquely explain

It does not explain why the **first** material error becomes more likely as compositional depth rises in static tasks. It also does not by itself explain state loss across long pauses or handoffs.

### What would materially strengthen it

A controlled experiment showing that, holding policy complexity constant, making state authoritative, observable, verifiable, and reversible sharply reduces terminal failure and the downstream error multiplier.

### What would materially weaken it

A finding that long-horizon failure remains nearly unchanged when state is fully observed, every consequential action is postcondition-checked, and failed actions are safely reversible.

## Finalist B — effective policy-complexity breakpoint

### Mechanism

The agent must compose a policy over interacting subgoals, constraints, branches, and future dependencies. As the effective search/composition problem grows, a previously adequate reasoning policy can cross a nonlinear threshold.

The relevant variable is not raw chain length. It is the complexity of maintaining a policy that remains globally coherent.

### Strongest support

- HORIZON deliberately increases task composition and reports horizon-dependent breaking behavior.
- UltraHorizon reports persistent gaps and capability-limited failure even under long-horizon-focused evaluation.
- The MD5 counterexample shows that long dependency chains can succeed when the policy is highly regular and state is exact, weakening “length alone” while remaining compatible with complexity as the real variable.
- Traverse finds reasoning/planning errors are disproportionately common as originating mistakes even though action errors dominate the later visible cascade.

### Strongest contrary evidence / limitations

- Benchmark extension levels remain proxies for real task complexity.
- Failure taxonomies often classify the visible failure rather than identify a fundamental bottleneck.
- Better runtime feedback can rescue trajectories that contain planning errors, so policy quality alone does not determine terminal outcome.
- Model and scaffold changes are often confounded.

### What this model explains better than the nearest competitors

It explains why performance can collapse before there is a major state-corruption event and why extra verification cannot fully rescue a policy that cannot construct a viable plan.

### What it does not uniquely explain

It does not explain large cross-environment differences in recovery after similar local errors, nor why checkpoint or transaction mechanisms can produce large gains under injected faults.

### What would materially strengthen it

A factorial benchmark showing that dependency depth or branching strongly increases **first-material-error probability** even when state is static, fully observable, reversible, and continuously verified.

### What would materially weaken it

A finding that the apparent breakpoint largely disappears once state observability and recovery are controlled, suggesting that “planning complexity” was mainly a proxy for accumulated state divergence.

## Finalist C — persistent-state & coordination architecture

### Mechanism

A long-running system needs a durable representation of what is true now, what has been done, what remains open, which constraints still apply, and which actor owns each obligation.

Raw transcript retention is not enough. Similarity-based retrieval is not necessarily enough. The architecture must preserve causally relevant state across:

- context growth;
- compaction;
- retries;
- restart/resume;
- worker handoff;
- user-agent coordination;
- multiple agents;
- external system updates.

### Strongest support

- AMA-Bench finds weaknesses in existing long-horizon memory systems and benefits from causality-structured memory.
- τ²-bench exposes shared-state coordination difficulty.
- AgentRewind improves outcomes by checkpointing both context and environment state.
- ToolSandbox shows the importance of implicit state dependencies.
- Long-horizon multi-actor settings create failure modes that cannot be reduced to one model's local next-step competence.

### Strongest contrary evidence / limitations

- Some single-session failures occur with no obvious memory or handoff problem.
- The MD5 result shows that exact state can be carried through a long chain in a narrow controlled setting.
- More persistent memory can preserve incorrect beliefs as well as correct ones.
- External state stores can create stale or contradictory sources of truth if commit semantics are weak.

### What this model explains better than the nearest competitors

It explains omissions, duplicated work, stale commitments, inconsistent handoffs, and coordination failures that can survive local verification.

### What it does not uniquely explain

It does not explain why a single agent with perfect persistent state may still hit a planning breakpoint, nor why one wrong external action can cascade even when memory is excellent.

### What would materially strengthen it

A controlled experiment showing that externalized causal state and explicit handoff/ownership records substantially reduce failures while holding model, task complexity, and verification policy fixed.

### What would materially weaken it

A finding that persistent-state architecture has little effect once policy complexity and closed-loop recovery are controlled.

# Shared-bias and source-dependency audit

## Software and computer-use concentration

HCAST, METR time-horizon work, SWE-style trajectories, OS tasks, and several recovery studies are heavily weighted toward software or computer-use environments.

That makes the evidence especially relevant to coding and digital operations, but weaker for robotics, long-running social interaction, multi-user enterprise work, or scientific field operations.

## Benchmark-definition dependence

“Horizon” is not one variable across sources:

- HCAST / METR: human task duration;
- HORIZON: intrinsic/compositional task horizon;
- Traverse: trajectory structure and first-error localization;
- MD5: exact dependent tool-call depth;
- τ / τ²: multi-turn stateful interaction;
- UltraHorizon: very large token/tool-call trajectories under partial observability.

Agreement across these measures is useful, but they must not be treated as interchangeable measurements of one latent quantity.

## Failure-taxonomy dependence

Several studies use human or LLM-assisted labels such as planning, memory, environment, action, or reasoning failure. Those labels are useful descriptions but do not automatically establish causal identification.

A late “invalid action” can be a symptom of an earlier wrong state estimate. A “planning error” can be downstream of missing information. The run therefore used taxonomies as evidence about **where failures appear**, not as direct proof of a fundamental cause.

## Scaffold confounding

Model, prompting, tools, memory, retry policy, and orchestrator are often changed together.

A benchmark score therefore measures an **agent system**, not a pure foundation-model property. This is one reason the final judgment separates policy capability from system reliability.

## Intervention-study selection

DeepVerifier, RoTS, AgentRewind, and Atomix each intervene on a specific failure surface. Their positive results show that the surface is actionable; they do not prove that it is the dominant bottleneck in every task class.

## Preprint versus peer-reviewed evidence

Some of the most directly relevant 2026 work — Traverse, HORIZON, Atomix, AgentRewind, and the MD5 state-tracking experiment — was available as public preprints at the time of this run. Peer-reviewed ICML/ACL/NAACL/ICLR papers received stronger provenance status where claims overlapped, but preprint status alone was not treated as disqualifying.

## Survivorship and terminal-score bias

Pass/fail metrics can hide unsafe or incorrect intermediate behavior. Conversely, focusing only on failed trajectories can hide recoverable mistakes.

Traverse is especially useful because it separates mistakes, recovery, and final outcome, but even its first-mistake analysis deliberately excludes diffuse failures with no unique turning point.

# Assumption sensitivity

## Assumption 1 — “The problem is basically independent per-step error multiplication”

**Result: THREATENED.**

The `p^n` intuition explains why long chains can be fragile, but Traverse shows strong conditional dependence after errors, while the MD5 experiment provides a narrow counterexample where a 196-call dependent sequence can often succeed under tightly controlled state and tool semantics.

The relevant errors are neither identical nor independent.

## Assumption 2 — “Every failed run has one decisive first mistake”

**Result: FAIL as a universal assumption.**

Traverse reports hundreds of failed trajectories without one localizable decisive first mistake. A useful reliability architecture must therefore handle both discrete faults and gradual drift.

## Assumption 3 — “A stronger base model will mostly solve reliability”

**Result: THREATENED.**

Capability improves, but the ICML reliability study finds only small reliability gains on several operational dimensions, while UltraHorizon reports persistent failure under simple scaling.

This does not imply scaling is useless. It implies that model scaling and reliability engineering are distinct intervention levers.

## Assumption 4 — “Verification is cheap and reliable”

**Result: THREATENED.**

Generic frontier judges can fail to localize trajectory errors. Specialized verification can improve results, but it consumes inference and can introduce false positives, false negatives, and latency.

Verification should therefore be **risk-adaptive**, not blindly inserted after every trivial action.

## Assumption 5 — “Rollback solves recovery”

**Result: CONDITIONAL.**

Rollback is powerful only when the relevant state can actually be restored or compensated. External writes, messages, payments, user actions, and irreversible operations require transaction boundaries or compensating semantics, not merely restoring an LLM transcript.

# Pairwise collisions

## F1 closed-loop state integrity vs F2 policy-complexity breakpoint

**Decision-conflicting prediction:** What happens when task complexity increases while the environment remains static, fully observable, continuously verified, and reversible?

- **F1** predicts that much of the terminal-failure increase should be suppressed because mistakes cannot silently corrupt later canonical state.
- **F2** predicts that a substantial first-error breakpoint should remain because the policy itself becomes harder to construct as dependency depth and branching rise.

The current evidence supports both effects. HORIZON and UltraHorizon keep F2 alive; Traverse, ToolSandbox, RoTS, Atomix, and AgentRewind show that containment strongly changes terminal outcomes.

**Collision result:** Neither model dominates universally. F2 better explains **entry into error** under controlled state; F1 better explains **conversion of an error into terminal failure** in mutable environments.

## F1 closed-loop state integrity vs F3 persistent-state architecture

**Decision-conflicting prediction:** In a single uninterrupted session with no handoff or compaction, but with consequential side effects and weak postcondition checks, should reliability still degrade?

- **F1:** yes — stale or unverified external state is enough.
- **F3:** the strongest effect should appear around persistence boundaries such as compaction, resume, handoff, or multi-actor coordination.

Conversely, if every local action is strongly verified but the task repeatedly crosses handoff/compaction boundaries, F3 predicts failures that F1 alone does not.

**Collision result:** F1 and F3 are distinct but complementary. F1 is about **control-loop integrity around actions**; F3 is about **continuity of canonical task state across time and actors**.

## F2 policy-complexity breakpoint vs F3 persistent-state architecture

**Decision-conflicting prediction:** If the same highly compositional task is given an external causal state ledger with perfect persistence but no stronger planning policy, does the breakpoint disappear?

- **F3:** a large share of long-horizon failures should fall if lost obligations, stale summaries, and handoff inconsistency were dominant.
- **F2:** a substantial breakpoint should remain if the policy still cannot synthesize or adapt a coherent plan over the dependency structure.

**Collision result:** Existing evidence is insufficient to quantify the split. AMA-Bench supports F3; HORIZON and UltraHorizon support F2. No reviewed source in this run orthogonally manipulates both variables at sufficient scale.

# Slate-level adjudication

The adjudication rejected the premise that the evidence supports one universal root cause.

The three finalists describe different parts of the failure process:

| Family | Best interpretation | Main causal locus |
|---|---|---|
| F1 — Closed-loop state integrity | errors become dangerous because state divergence is not detected and contained | error propagation / recovery |
| F2 — Policy-complexity breakpoint | first material errors become more likely as effective planning complexity rises | error generation |
| F3 — Persistent-state & coordination architecture | the system loses a faithful representation of commitments and state across time/actors | state continuity |

The adjudicator therefore treated the families as **interacting and task-class dependent**.

The strongest general causal statement supported by the evidence is:

> Long-horizon agent failure is not well explained by task length alone. Reliability degrades when increasing policy complexity raises the chance of entering a bad trajectory, while imperfect observability, verification, recoverability, and persistent-state architecture determine whether that error is contained or amplified.

This is narrower than claiming that any one mechanism is “the” cause.

## Second-opinion trigger

The original run triggered an independent blind second opinion because pairwise adjudication left the global dominance relation between the two strongest broad explanations unresolved: evidence for a universal winner remained weak, and a plausible counterfactual could shift relative weight between upstream policy-complexity failure and downstream closed-loop state/recovery failure. Under the current protocol, this corresponds to the weak-winner / unresolved-comparison trigger.

The second opinion did **not** establish a universal winner. It independently preserved the task-class-dependent reading and judged the public evidence insufficient to choose one of those mechanisms as globally dominant.

It also preserved the same practical asymmetry:

- there was no direct head-to-head evidence showing that closed-loop verification/recovery is a universally stronger causal fix than better planning;
- nevertheless, targeted closed-loop control at state-changing or commit boundaries remained the more robust **near-term engineering action**, because it limits propagation under multiple surviving causal models.

This confirmation was treated as a robustness check on the inference, not as additional real-world evidence.

# Phase E — model judgment, action judgment, and evidence sufficiency

## Model judgment

There is **insufficient evidence to choose one universal causal family** as the dominant explanation across long-running real-world agent tasks.

The best-supported structure is an interaction:

```text
effective policy complexity
        ↓
first-error / drift hazard
        ↓
closed-loop detection and containment
        ↓
persistent-state continuity across time and actors
        ↓
terminal reliability
```

The relative weight of each stage changes by task.

For a static but combinatorially difficult task, F2 can dominate. For an operational workflow with external side effects, F1 can dominate. For multi-session or multi-actor work, F3 can become load-bearing.

## Action judgment

Even though no universal causal winner is justified, the evidence is sufficient to prioritize one **cross-model engineering intervention**:

> **Add risk-adaptive closed-loop control around state-changing actions.**

In practical terms:

1. **Read authoritative state before consequential action.**
2. **Represent the intended postcondition explicitly.**
3. **Execute through idempotent, transactional, or compensatable semantics where possible.**
4. **Re-read authoritative state after the action.**
5. **Verify the postcondition with a check that is independent of the action-generation path when stakes justify it.**
6. **On mismatch, stop propagation and choose retry, rollback, compensation, or replanning.**
7. **Checkpoint durable task state at meaningful commit boundaries.**

This is not “verify everything after every step.” Verification cost should scale with:

- irreversibility;
- blast radius;
- observability;
- downstream dependency;
- cost of rollback;
- uncertainty in the current state estimate.

### Feasible action comparison

The run compared four near-term action classes qualitatively across the surviving models:

| Action | Expected downside / regret if wrong | Reversibility / lock-in | Option & information value | Cross-model fit |
|---|---|---|---|---|
| **A1. Risk-adaptive closed-loop verification/recovery at consequential boundaries** | extra tool calls, latency, verifier mistakes; may not reduce first-error generation | high reversibility when added at orchestration boundaries; can be scoped gradually | high: produces trajectory evidence about detection/recovery while limiting propagation | useful under F1 directly; protective under F2; supplies commit/checkpoint structure for F3 |
| **A2. Prioritize stronger planning / more test-time reasoning first** | can spend substantial compute while leaving stale-state and recovery failures untouched | moderately reversible, but cost can scale with every run | medium: may reveal whether first-error hazard shifts, but gives weaker protection after errors | strongest under F2; weaker protection under F1/F3 |
| **A3. Redesign persistent memory / coordination state first** | architecture complexity; risk of persisting wrong beliefs or creating competing sources of truth | lower reversibility and greater integration lock-in than A1 | high for handoff/memory questions, but slower and more system-specific | strongest under F3; incomplete for F1/F2 |
| **A4. Verify every step / add blanket redundancy** | high latency and cost; false alarms; may multiply correlated judgments without improving state integrity | technically reversible but operationally expensive | low-to-medium: poor targeting can obscure where value comes from | broad but inefficient; not justified by current evidence |

No quantitative utility scores were assigned because the evidence does not support them.

**Qualitative dominance:** A1 has the lowest regret across the three plausible causal families while remaining relatively reversible and informative. A2 and A3 remain important targeted follow-ons if the discriminating measurements show that first-error generation or persistence boundaries dominate. A4 is not justified as the default because the evidence supports selective, risk-adaptive verification rather than blanket checking.

### Why prioritize this before generic “more agents” or “more reasoning”

This intervention survives the widest set of plausible models:

- If **F1** is dominant, it directly attacks the core propagation mechanism.
- If **F2** is dominant, it does not prevent every planning error, but it can keep one planning error from contaminating the remainder of the task.
- If **F3** is dominant, commit checkpoints and authoritative state updates create the durable substrate that memory/handoff systems need.

It is therefore a **robust action under causal uncertainty**, not proof that F1 is the universal winner.

## Evidence-sufficiency judgment

For the causal question:

> **Which single mechanism is the universal primary cause of long-horizon agent failure?**

the run returns:

> **INSUFFICIENT DATA TO CHOOSE**

For the engineering decision:

> **Which intervention class deserves priority before broad deployment of long-running state-changing agents?**

the evidence is sufficient to recommend:

> **risk-adaptive closed-loop state verification and recovery at consequential state transitions.**

This distinction is central to Convergence Guard: **model uncertainty does not imply action paralysis when one intervention is robust across the plausible model set.**

# Popular explanations weakened by the evidence

### “Long tasks fail because per-step accuracy compounds as p^n.”

Useful intuition, but too simple. Errors are correlated, recovery varies by environment, and long controlled chains can succeed.

### “The context window is the bottleneck.”

Sometimes relevant, but not sufficient. Memory architecture, causal state representation, state mutability, planning complexity, and recovery all matter independently.

### “Just use a stronger model.”

Stronger models can help, but reliability metrics do not rise in lockstep with headline capability, and simple scaling does not eliminate long-horizon failure in the cited evidence.

### “Just let the agent reflect after every step.”

Generic self-judgment is not a dependable failure detector. Specialized verification helps, but verification has cost and error modes of its own.

### “Just run five agents and vote.”

Agreement does not establish evidential independence, and voting does not repair corrupted external state.

### “Checkpointing solves it.”

Checkpointing helps only if the right state is captured and the external effects are reversible or compensatable. A checkpoint can faithfully preserve an already-wrong belief.

### “The first mistake explains every failed trajectory.”

False as a universal statement. Traverse contains a substantial set of diffuse failures with no single decisive first mistake.

# Highest-value decision-changing experiment

The run's most important missing evidence is a controlled **factorial reliability benchmark** that independently manipulates the three finalists instead of changing whole agent stacks at once.

## Proposed benchmark

Use matched tasks with the same semantic goal and roughly matched local action difficulty. Independently vary:

### Factor A — policy complexity

- shallow independent subtasks;
- deeper dependency chains;
- branching/contingent plans;
- interacting constraints.

### Factor B — state architecture

- transcript-only;
- external flat state ledger;
- causally structured persistent state with explicit obligations, ownership, and verified facts.

### Factor C — closed-loop recovery

- no mandatory verification;
- postcondition verification;
- verification + retry;
- verification + rollback/compensation + replan.

### Factor D — environment properties

Where practical, cross:

- static vs mutable state;
- fully observable vs partially observable;
- reversible vs irreversible/compensatable actions;
- single actor vs dual/multi-actor control.

## Measure more than final pass/fail

For every run, record:

- first material error position;
- whether a unique first error exists;
- `P(first material error)` by experimental cell;
- `P(terminal failure | first material error)` by experimental cell;
- error type;
- detection latency;
- whether the detector was internal or environmental;
- recovery attempt;
- recovery success;
- number of state divergences;
- number of unverified consequential actions;
- stale-state reads;
- duplicated or omitted obligations;
- rollback/compensation success;
- terminal success;
- repeated-run consistency;
- unsafe side effects even on nominally successful runs.

## Discriminating predictions

**F2 gains support** if increasing dependency depth strongly raises first-error hazard even when state is fully observable, persistent, verified, and reversible.

**F1 gains support** if strong postcondition checks and rollback sharply reduce `P(terminal failure | first material error)` and downstream error correlation while leaving `P(first material error)` comparatively unchanged.

**F3 gains support** if causally structured persistent state sharply reduces failures concentrated around context growth, handoff, resume, or multi-actor boundaries while model and verification policy remain fixed.

The interaction terms matter as much as the main effects. A likely result is not one winner but a map showing **which mechanism dominates in which task regime**.

## Minimum practical discriminating pilot

The full factorial benchmark above is the research-grade design. The **cheapest practical next step that could change the near-term engineering decision** is smaller:

- preselect **8 stateful tool-use tasks** from at least two task types before running the experiment;
- hold the base model, prompts, tool set, planning budget, and task definitions fixed;
- run a **2×2 architecture ablation**:
  1. baseline — no added closed-loop guard, no structured persistent ledger;
  2. closed-loop guard only — authoritative pre-read, explicit postcondition, post-read, targeted retry/rollback/replan;
  3. persistent ledger only — explicit durable facts, obligations, ownership, and verified completion state;
  4. guard + persistent ledger;
- repeat each task **three independent times per cell**, producing 96 trajectories.

The pilot should record `P(first material error)`, `P(terminal failure | first material error)`, detection latency, recovery success, unsafe/irreversible side effects, extra tool calls, latency, and final task success.

### Decision-changing patterns

- **Keep A1 as the near-term priority** if the guard conditions consistently lower conditional terminal failure across both task types while first-error frequency remains broadly similar and the added cost/latency stays operationally acceptable.
- **Shift priority toward A2 / policy capability** if most of the performance loss comes from a rising first-error rate and the guard produces little reduction in conditional terminal failure.
- **Shift priority toward A3 / persistent-state architecture** if the ledger conditions produce the clearer gain, especially on resume/handoff/long-context boundaries, while the guard alone adds little.
- **Adopt a staged hybrid** if guard and ledger effects are complementary or the combined cell produces a material interaction.

### Guardrails and stopping rule

- Score the first material error and terminal outcome using frozen criteria defined before seeing condition labels where practical.
- Do not change prompts, tools, or planning budget mid-pilot.
- Count added verification cost and verifier-caused failures, not only recovered runs.
- Stop after the preregistered 96 trajectories; do not extend the pilot until a preferred conclusion appears.
- If results are mixed across the two task types, retain `INSUFFICIENT DATA TO CHOOSE` for a universal causal winner and use the task-specific pattern rather than averaging it away.

This pilot is not large enough to establish a universal theory. Its purpose is narrower: determine whether the current **A1 engineering priority** survives a controlled ablation before investing in the larger factorial benchmark.

# Runtime integrity note

The original Full Mode run used fresh isolated worker contexts for stages whose value depended on blindness or independence, including causal search, reduction, finalist dossiers, and slate-level adjudication.

This public case study does not treat agreement between workers as independent real-world evidence. Claims are grounded in the cited external evidence, and the worker outputs are used only to structure competing causal models and their comparisons.

# What this example demonstrates about the method

This case is useful precisely because the final result is not “we found the one true reason agents fail.”

The protocol forced several distinctions that a conventional discussion can easily collapse:

> **Longer tasks correlate with lower success**
> is not the same proposition as
> **task length itself is the cause.**

> **Planning errors often begin failures**
> is not the same proposition as
> **better planning alone will make the system reliable.**

> **Memory matters**
> is not the same proposition as
> **a larger context window is the solution.**

> **No universal causal winner is identified**
> is not the same proposition as
> **no engineering action can be justified.**

The strongest output of the run is therefore a two-part judgment:

1. **Causal attribution:** the present evidence supports an interacting, task-dependent model and is insufficient to choose one universal primary cause.
2. **Decision under uncertainty:** closed-loop verification and recovery around consequential state changes is a robust priority across the surviving model set.

That separation between **what is true about the cause** and **what is rational to do next** is one of the central design goals of Convergence Guard.

# Sources

Primary or nearest-available sources used in the public evidence brief:

1. Rein, D. et al. (2025). **HCAST: Human-Calibrated Autonomy Software Tasks.**
   https://arxiv.org/abs/2503.17354

2. METR (updated 2026-05-08). **Task-Completion Time Horizons of Frontier AI Models.**
   https://metr.org/time-horizons/

3. Wang, X. J. et al. (2026). **The Long-Horizon Task Mirage? Diagnosing Where and Why Agentic Systems Break.**
   https://arxiv.org/abs/2604.11978

4. Rahman, S. et al. (2026). **Locating Hidden Failures Makes Long-Horizon Agents More Reliable.**
   https://arxiv.org/abs/2609.17930

5. Lu, J. et al. (2025). **ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities.** Findings of NAACL 2025.
   https://aclanthology.org/2025.findings-naacl.65/

6. Yao, S. et al. (2025). **τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains.** ICLR 2025.
   https://proceedings.iclr.cc/paper_files/paper/2025/hash/1b126cc38b8638e07bef37e7b2bb72bf-Abstract-Conference.html

7. Barres, V. et al. (2026). **τ²-Bench: Evaluating Conversational Agents in a Dual-Control Environment.** ICML 2026.
   https://proceedings.mlr.press/v306/barres26a.html

8. Rabanser, S. et al. (2026). **Towards a Science of AI Agent Reliability.** ICML 2026.
   https://proceedings.mlr.press/v306/rabanser26a.html

9. Wan, Y. et al. (2026). **Inference-Time Scaling of Verification: Self-Evolving Deep Research Agents via Test-Time Rubric-Guided Verification.** Findings of ACL 2026.
   https://aclanthology.org/2026.findings-acl.1243/

10. Bu, T. et al. (2026). **Recovering Policy-Induced Errors: Benchmarking and Trajectory Synthesis for Robust GUI Agents.** ICML 2026.
    https://proceedings.mlr.press/v306/bu26b.html

11. Mohammadi, B. et al. (2026). **Atomix: Timely, Transactional Tool Use for Reliable Agentic Workflows.**
    https://arxiv.org/abs/2602.14849

12. Zhuang, Y. et al. (2026). **AgentRewind: Recoverable Execution for Long-Horizon LLM Agents.**
    https://arxiv.org/abs/2608.14380

13. Zhao, Y. et al. (2026). **AMA-Bench: Evaluating Long-Horizon Memory for Agentic Applications.** ICML 2026.
    https://proceedings.mlr.press/v306/zhao26bs.html

14. Pai, D. M. & Xian, L. (2026). **Long-Horizon State Tracking in LLMs: Executing MD5 through a Deep Sequence of Dependent Tool Calls.**
    https://arxiv.org/abs/2609.00012

15. Luo, H. et al. (2026). **UltraHorizon: Benchmarking Agent Capabilities in Ultra Long-Horizon Scenarios.** ICML 2026.
    https://proceedings.mlr.press/v306/luo26ai.html

The source list is deliberately heterogeneous because the decision question spans planning, reliability, stateful tool use, recovery, memory, coordination, and benchmark methodology. The run did not count multiple papers as independent corroboration merely because they reached similar conclusions; source ancestry, task overlap, and intervention scope were considered separately.
