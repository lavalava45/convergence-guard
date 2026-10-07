# P01 — Checkout service failure after deployment

You are on call for a checkout service. At 10:02 a deployment completed. Within two minutes, most checkout requests began returning HTTP 503.

Your task is to determine what causal conclusion is justified by the available evidence and what action should be taken now.

Constraints:

- restore checkout quickly;
- avoid data-destructive actions;
- a deployment rollback or configuration correction is reversible;
- do not use the open web;
- do not assume facts that are not in the supplied evidence.

Return the required normalized final-answer object.
