# M04 — Duplicate order events

A stream-processing pipeline began emitting duplicate order events after two reliability changes were deployed together. Duplicates are causing downstream reconciliation work, but production traffic remains available.

Determine what causal conclusion is justified now and the minimum decision-changing next test.

Constraints:

- do not perform an indiscriminate production rollback while orders are flowing;
- isolated canaries and extra diagnostic logging are allowed;
- do not use the open web;
- do not assume facts outside the supplied evidence.

Return the required normalized final-answer object.
