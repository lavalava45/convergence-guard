# Browser Pilot Packet 003

RUN_ID: P01-r1-single-context
CASE_ID: P01
MODE: single-context
EVAL_COMMIT: fda4395b37c782de3e6d79ab41d59b208d39e88f

## Participant wrapper

This is a controlled evaluation run.

Use only the material in this packet. Do not browse the web, use Connected Apps, retrieve other chats, or add facts from outside the packet.

Analyze the case carefully. Consider competing explanations, evidence quality, uncertainty, action under constraints, and a useful next test. Self-checking is allowed.

Do not ask the user questions. Do not request more files. At the end, return exactly one JSON object and nothing else. Do not wrap it in Markdown fences. The JSON must conform to the embedded OUTPUT-SCHEMA and use case_id = "P01".

---

# PARTICIPANT-VISIBLE CASE

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

## Evidence E01

2026-10-06T10:03:11Z checkout-7d9f startup INFO  configuration loaded
2026-10-06T10:03:12Z checkout-7d9f db      ERROR getaddrinfo ENOTFOUND db-proxy-old.internal
2026-10-06T10:03:12Z checkout-7d9f health  WARN  dependency database unavailable
2026-10-06T10:03:13Z checkout-7d9f http    WARN  GET /health -> 503
2026-10-06T10:03:18Z checkout-7d9f db      ERROR getaddrinfo ENOTFOUND db-proxy-old.internal
2026-10-06T10:03:19Z checkout-7d9f http    WARN  POST /checkout -> 503 dependency unavailable

## Evidence E02

Deployment configuration diff at 10:02:

- DATABASE_HOST=db-proxy.internal
+ DATABASE_HOST=db-proxy-old.internal

No application-code files changed in this deployment.

## Evidence E03

Probe executed from the same runtime network namespace at 10:06:

db-proxy.internal
  DNS: resolves to 10.20.4.17
  TCP 5432: success

db-proxy-old.internal
  DNS: NXDOMAIN

## Evidence E04

10:00-10:10 runtime summary:

CPU utilization: 18-27%
Memory utilization: 43-46%
Pod restarts: 0
Database dependency check: FAIL
Other dependency checks: PASS

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
