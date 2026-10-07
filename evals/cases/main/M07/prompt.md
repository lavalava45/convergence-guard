# M07 — Large upload corruption at a document gateway

A document gateway corrupts some large uploads. A client-library rollout and a proxy-firmware rollout occurred in the same week, and teams disagree over which change should be called the root cause.

Determine the justified causal assessment and a reversible mitigation.

Constraints:

- small uploads are unaffected;
- production data must not be intentionally corrupted for testing;
- isolated canaries using synthetic files are allowed;
- do not use the open web;
- do not assume facts outside the supplied evidence.

Return the required normalized final-answer object.
