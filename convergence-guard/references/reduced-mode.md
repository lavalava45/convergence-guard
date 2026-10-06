# Convergence Guard — Reduced Mode

Reduced Mode is a single-context fallback for hosts that cannot create genuinely isolated worker contexts.

It preserves the **shape** of the reasoning protocol but not its strongest anti-anchoring guarantees. It must never be presented as equivalent to Full Mode.

## When it is allowed

Use Reduced Mode only when:

- Full Mode isolation is unavailable; and
- the user explicitly accepts the limitation; and
- the task is not so consequential that pretending to compensate for missing independence would be irresponsible.

Label the result clearly as:

`Convergence Guard — Reduced Mode (no independent worker isolation)`

## What guarantees are lost

Reduced Mode cannot honestly provide:

- independent causal-search contexts;
- blind screening versus mapping in separate contexts;
- independent dossier authorship;
- independent second-opinion reconstruction.

Sequential sections in one context remain vulnerable to shared anchoring and memory effects.

## Reduced workflow

1. Build the evidence brief and decision contract, including the same finite run budget and corrective-cycle stopping rules as Full Mode (see [protocol details §13.1](protocol-details.md#131-run-budget-and-stopping)).
   Apply the same claim-level source-quality and provenance rules as Full Mode; Reduced Mode relaxes context-isolation guarantees, not evidence standards.
2. Perform the framing/outside-view check.
3. Generate at least three deliberately different search mandates **before** generating candidate models.
4. Complete each mandate in a separate labeled pass without editing earlier candidate outputs.
5. Create a causal map and contract screening, explicitly noting that blindness is not guaranteed.
6. Select 2–3 causally distinct finalists without aggregate scoring.
7. Build compact causal dossiers.
8. Stress load-bearing assumptions and audit shared blind spots.
9. Compare decision-conflicting finalist pairs.
10. Separate model judgment from action judgment.
11. Apply the evidence-sufficiency gate.
12. End with a feasible, worthwhile decision-changing observation or experiment. If none is identified, state `NO FEASIBLE DISCRIMINATOR IDENTIFIED` and the search limits; retain unresolved model judgment and apply the ordinary action-sufficiency gate. A known check deferred for budget reasons is not a no-discriminator result.

## Integrity rules

- Never call sequential passes “independent agents.”
- Never treat repeated agreement inside one context as corroboration.
- Preserve original candidate wording so later refinement cannot silently rewrite weak ideas.
- Be more willing than Full Mode to conclude `INSUFFICIENT DATA TO CHOOSE` when the missing isolation could matter.
- For very high-stakes decisions, recommend an external independent review or additional real-world evidence rather than adding more simulated internal critics.
