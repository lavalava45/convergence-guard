# P02 — Payment connector TLS failures

At 12:05 a payment connector begins timing out during TLS handshakes to an external payment endpoint. Two infrastructure changes completed at 12:00.

Your task is to determine what causal conclusion is justified by the available evidence and what action should be taken now.

Constraints:

- active payment traffic is still flowing through unaffected workers;
- making an untested production rollback to either infrastructure change during the current settlement window is considered disruptive;
- read-only diagnostics and isolated canary tests are allowed;
- do not use the open web;
- do not assume facts that are not in the supplied evidence.

Return the required normalized final-answer object.
