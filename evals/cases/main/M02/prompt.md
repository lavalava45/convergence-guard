# M02 — Export jobs failing during storage maintenance

Customer export jobs from worker pool B began failing during a maintenance window. A storage maintenance operation and a base-image rollout both occurred within minutes of the first failures. Pool A continues to export successfully.

Determine the justified causal conclusion and the best immediate action.

Constraints:

- the export SLA is at risk;
- storage maintenance is still in progress and should not be interrupted without evidence;
- replacing or rolling back one worker image is reversible;
- do not use the open web;
- do not assume facts outside the supplied evidence.

Return the required normalized final-answer object.
