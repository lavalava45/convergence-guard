# Browser Pilot Packet 006

RUN_ID: P02-r1-single-context
CASE_ID: P02
MODE: single-context
EVAL_COMMIT: fda4395b37c782de3e6d79ab41d59b208d39e88f

## Participant wrapper

This is a controlled evaluation run.

Use only the material in this packet. Do not browse the web, use Connected Apps, retrieve other chats, or add facts from outside the packet.

Analyze the case carefully. Consider competing explanations, evidence quality, uncertainty, action under constraints, and a useful next test. Self-checking is allowed.

Do not ask the user questions. Do not request more files. At the end, return exactly one JSON object and nothing else. Do not wrap it in Markdown fences. The JSON must conform to the embedded OUTPUT-SCHEMA and use case_id = "P02".

---

# PARTICIPANT-VISIBLE CASE

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

## Evidence E01

2026-10-06T12:04:58Z worker-12 payment INFO  connection attempt api.payments.example:443
2026-10-06T12:05:03Z worker-12 payment ERROR TLS handshake timeout after 5000ms
2026-10-06T12:05:08Z worker-12 payment ERROR TLS handshake timeout after 5000ms
2026-10-06T12:05:13Z worker-12 payment ERROR TLS handshake timeout after 5000ms

No certificate-validation error, protocol-version error, or explicit connection-refused error is recorded.

## Evidence E02

Changes completed at 12:00:

Change A:
  payment-connector base image updated;
  TLS client library changed from version family 4.x to 5.x.

Change B:
  outbound firewall policy for the connector subnet migrated to a new policy set.

Both changes reached the affected worker pool before the first recorded timeout.

## Evidence E03

Read-only probe from an affected worker at 12:09:

DNS lookup api.payments.example: success
TCP connect api.payments.example:443: success

The probe did not capture or inspect the TLS handshake payload.

## Evidence E04

Available observability at 12:10:

- client logs contain only the handshake timeout shown in E01;
- there is no packet capture;
- the new firewall policy has no per-rule drop telemetry enabled;
- no isolated worker is currently running the previous TLS client library;
- the external payment provider exposes no participant-visible server-side handshake log for this incident.

---

# MODE SPECIFICATION

# Mode: single-context

## Purpose

Provide a strong ordinary-analysis baseline without Convergence Guard-specific procedural scaffolding.

## Context

- exactly one fresh effective context for the run;
- no prior eval-run conclusions;
- no private key or judge material;
- same participant-visible case files and tools as the other modes.

## Analytical instruction

Analyze the case carefully. Consider competing explanations, evidence quality, uncertainty, action under constraints, and a useful next test. Self-checking is allowed.

The prompt must not require a single winner, suppress uncertainty, artificially limit alternatives, or teach Convergence Guard labels or hidden rubric wording.

## Output

Return the common final-answer schema.

## Accounting

All model calls made to obtain the final answer count against the mode budget.


---

# COMMON OUTPUT CONTRACT

{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Convergence Guard comparative eval final answer",
  "type": "object",
  "additionalProperties": false,
  "required": ["case_id", "causal_assessment", "action", "evidence", "uncertainty", "next_test"],
  "properties": {
    "case_id": {"type": "string", "minLength": 1},
    "causal_assessment": {
      "type": "object",
      "additionalProperties": false,
      "required": ["status", "candidate_causes", "preferred_cause"],
      "properties": {
        "status": {"enum": ["CHOOSE", "COEXIST", "INSUFFICIENT"]},
        "candidate_causes": {
          "type": "array",
          "minItems": 1,
          "items": {
            "type": "object",
            "additionalProperties": false,
            "required": ["id", "claim"],
            "properties": {
              "id": {"type": "string", "minLength": 1},
              "claim": {"type": "string", "minLength": 1}
            }
          }
        },
        "preferred_cause": {
          "type": ["string", "null"],
          "description": "Candidate ID when status=CHOOSE; null for COEXIST or INSUFFICIENT."
        }
      },
      "allOf": [
        {
          "if": {"properties": {"status": {"const": "CHOOSE"}}},
          "then": {"properties": {"preferred_cause": {"type": "string", "minLength": 1}}}
        },
        {
          "if": {"properties": {"status": {"enum": ["COEXIST", "INSUFFICIENT"]}}},
          "then": {"properties": {"preferred_cause": {"type": "null"}}}
        }
      ]
    },
    "action": {
      "type": "object",
      "additionalProperties": false,
      "required": ["recommended_action", "reason"],
      "properties": {
        "recommended_action": {"type": "string", "minLength": 1},
        "reason": {"type": "string", "minLength": 1}
      }
    },
    "evidence": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["evidence_ids", "claim"],
        "properties": {
          "evidence_ids": {
            "type": "array",
            "minItems": 1,
            "items": {"type": "string", "pattern": "^E[0-9]{2}$"}
          },
          "claim": {"type": "string", "minLength": 1}
        }
      }
    },
    "uncertainty": {
      "type": "array",
      "items": {"type": "string", "minLength": 1}
    },
    "next_test": {
      "type": "object",
      "additionalProperties": false,
      "required": ["test", "outcome_a_implication", "outcome_b_implication"],
      "properties": {
        "test": {"type": "string", "minLength": 1},
        "outcome_a_implication": {"type": "string", "minLength": 1},
        "outcome_b_implication": {"type": "string", "minLength": 1}
      }
    }
  }
}


---

# FINAL EXECUTION INSTRUCTION

Perform the analysis now. Return exactly one JSON object and nothing else.
