from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "harness"
PROTOCOL = ROOT / "protocol" / "v0.2"
if str(HARNESS) not in sys.path:
    sys.path.insert(0, str(HARNESS))


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


cg = load_module("cg_v02_workflow_test", HARNESS / "cg_v02_workflow.py")
ablation = load_module("isolation_ablation_test", HARNESS / "isolation_ablation_runner.py")


def search_model(label: str) -> dict:
    return {
        "claim": f"claim {label}",
        "mechanism": f"mechanism {label}",
        "necessary_conditions": [f"condition {label}"],
        "predictions": [f"prediction {label}"],
        "implied_action": f"action {label}",
        "disconfirming_evidence": [f"disconfirm {label}"],
        "identification_threats": [],
        "conflicts_with_evidence": [],
    }


def final_v02(case_id: str, *, causal_status: str = "INSUFFICIENT") -> dict:
    relation = "UNRESOLVED" if causal_status == "INSUFFICIENT" else "NOT_APPLICABLE"
    return {
        "case_id": case_id,
        "causal_structure": {
            "status": causal_status,
            "supported_models": [],
            "preferred_cause": None,
            "relation": relation,
            "residual_uncertainty": "test uncertainty",
        },
        "action_decision": {
            "status": "DEFER_ACTION",
            "chosen_action": None,
            "rationale": "insufficient for commitment",
            "conditions": [],
            "cost_of_delay_considered": "bounded",
            "default_if_no_new_information": None,
        },
        "next_test": {
            "status": "NO_FEASIBLE_DISCRIMINATOR",
            "description": None,
            "decision_rule": [],
            "why_decision_changing": "no feasible discriminator identified",
        },
        "protocol_completion": {
            "status": "COMPLETE",
            "completed_stages": [],
            "skipped_stages": [],
            "triggered_but_unexecuted": [],
            "pending_hypotheses": [],
            "material_omissions": [],
        },
    }


def candidate_ids_from_prompt(prompt: str) -> list[str]:
    return sorted(set(re.findall(r'"id"\s*:\s*"(H\d+)"', prompt)))


class ScriptedFullCall:
    """Force the conditional branches that were missing in main-v0.1.7."""

    def __init__(self):
        self.calls: list[str] = []
        self.counts: dict[str, int] = {}

    def __call__(self, stage: str, prompt: str, schema: dict) -> dict:
        self.calls.append(stage)
        self.counts[stage] = self.counts.get(stage, 0) + 1
        n = self.counts[stage]

        if stage.startswith(("B1-search-", "B2-search-", "C4-checkpoint-search-", "D2-reroute-search-")):
            return {"models": [search_model(stage)]}

        if stage == "B2-coverage":
            return {"expand": True, "reasons": ["missing region"], "new_mandates": ["target missing region"]}

        if stage == "C1-screen":
            ids = candidate_ids_from_prompt(prompt)
            return {
                "evaluations": [
                    {
                        "candidate_id": cid,
                        "contract_fit": "PASS",
                        "evidence_support": "MIXED",
                        "causal_completeness": "CHAIN PRESENT",
                        "causal_identification": "THREATENED",
                        "identification_threat": "test",
                        "discriminability": "MEDIUM",
                        "decision_exposure": "MEDIUM",
                        "danger_flags": [],
                        "evidence_ids": ["E01"],
                    }
                    for cid in ids
                ]
            }

        if stage == "C2-map":
            ids = candidate_ids_from_prompt(prompt)
            return {
                "families": [
                    {"family_id": f"F{i+1}", "candidate_ids": [cid], "summary": cid}
                    for i, cid in enumerate(ids)
                ],
                "relations": [],
                "boundary_critic_needed": n == 1,
                "boundary_issue": "test boundary" if n == 1 else "",
            }

        if stage == "C3-boundary":
            ids = candidate_ids_from_prompt(prompt)
            return {
                "resolved": True,
                "rationale": "boundary resolved",
                "revised_mapping": {
                    "families": [
                        {"family_id": f"F{i+1}", "candidate_ids": [cid], "summary": cid}
                        for i, cid in enumerate(ids)
                    ],
                    "relations": [],
                    "boundary_critic_needed": False,
                    "boundary_issue": "",
                },
            }

        if stage == "C4-slate":
            ids = candidate_ids_from_prompt(prompt)
            # First C4 forces the targeted checkpoint. Third C4 is after the D1
            # revision and should select the newest revised ID (H06 here).
            if n == 1:
                return {
                    "finalist_ids": [ids[0]],
                    "information_probe_id": None,
                    "excluded_strong_models": [],
                    "checkpoint_needed": True,
                    "checkpoint_reason": "missing family",
                    "targeted_search_mandate": "search missing family",
                }
            chosen = ids[-1] if n >= 3 else ids[0]
            return {
                "finalist_ids": [chosen],
                "information_probe_id": None,
                "excluded_strong_models": [],
                "checkpoint_needed": False,
                "checkpoint_reason": "",
                "targeted_search_mandate": None,
            }

        if stage == "D1-dossier-1":
            cid = candidate_ids_from_prompt(prompt)[0]
            if n == 1:
                return {
                    "candidate_id": cid,
                    "mechanism": "old mechanism",
                    "assumptions": [],
                    "predictions": [],
                    "disconfirming_observations": [],
                    "decision_consequence": "old action",
                    "identification_weaknesses": [],
                    "error_cost_reversibility": "bounded",
                    "revision_required": True,
                    "revised_claim": "revised claim",
                    "revised_mechanism": "revised mechanism",
                    "new_load_bearing_premises": ["new premise"],
                }
            return self._dossier(cid)

        if stage.startswith("D1-reroute-dossier-"):
            cid = candidate_ids_from_prompt(prompt)[0]
            return self._dossier(cid)

        if stage == "D2-adjudication":
            return self._adjudication(reroute=True, second=False)

        if stage == "D2-adjudication-rerun":
            return self._adjudication(reroute=False, second=True)

        if stage == "D3-second-opinion":
            return {
                "disposition": "CHALLENGE",
                "decisive_inference": "conflict remains",
                "unsupported_premises": [],
                "missing_family_or_evidence": ["missing evidence"],
                "action_conflict": True,
                "conditions_or_limits": [],
            }

        if stage == "E-final":
            return final_v02("T01")

        raise AssertionError(f"unexpected stage {stage}")

    @staticmethod
    def _dossier(cid: str) -> dict:
        return {
            "candidate_id": cid,
            "mechanism": "mechanism",
            "assumptions": [],
            "predictions": [],
            "disconfirming_observations": [],
            "decision_consequence": "action",
            "identification_weaknesses": [],
            "error_cost_reversibility": "bounded",
            "revision_required": False,
            "revised_claim": None,
            "revised_mechanism": None,
            "new_load_bearing_premises": [],
        }

    @staticmethod
    def _adjudication(*, reroute: bool, second: bool) -> dict:
        return {
            "model_judgment": {
                "status": "INSUFFICIENT",
                "supported_candidate_ids": [],
                "relation": "UNRESOLVED",
                "residual_uncertainty": "test",
            },
            "action_judgment": {
                "status": "DEFER_ACTION",
                "preferred_action": None,
                "rationale": "test",
                "conditions": [],
            },
            "sensitivity_summary": "test",
            "shared_bias_summary": "test",
            "collision_summary": "test",
            "reroute_needed": reroute,
            "reroute_reason": "missing family" if reroute else "",
            "reroute_mandate": "search missing family" if reroute else None,
            "second_opinion_needed": second,
            "second_opinion_reason": "sharp conflict" if second else "",
            "next_test": {
                "status": "NO_FEASIBLE_DISCRIMINATOR",
                "description": None,
                "decision_rule": [],
            },
        }


class ZeroFinalistCall(ScriptedFullCall):
    def __call__(self, stage: str, prompt: str, schema: dict) -> dict:
        if stage == "B2-coverage":
            self.calls.append(stage)
            return {"expand": False, "reasons": [], "new_mandates": []}
        if stage == "C2-map":
            self.calls.append(stage)
            ids = candidate_ids_from_prompt(prompt)
            return {
                "families": [
                    {"family_id": f"F{i+1}", "candidate_ids": [cid], "summary": cid}
                    for i, cid in enumerate(ids)
                ],
                "relations": [],
                "boundary_critic_needed": False,
                "boundary_issue": "",
            }
        if stage == "C4-slate":
            self.calls.append(stage)
            return {
                "finalist_ids": [],
                "information_probe_id": None,
                "excluded_strong_models": [],
                "checkpoint_needed": False,
                "checkpoint_reason": "no supported model",
                "targeted_search_mandate": None,
            }
        if stage == "D2-adjudication":
            self.calls.append(stage)
            return self._adjudication(reroute=False, second=False)
        if stage == "E-final":
            self.calls.append(stage)
            return final_v02("T00", causal_status="NO_SUPPORTED_MODEL")
        return super().__call__(stage, prompt, schema)


class V02SchemaTests(unittest.TestCase):
    def setUp(self):
        self.schema = json.loads((PROTOCOL / "OUTPUT-SCHEMA-v0.2.json").read_text(encoding="utf-8"))

    def test_schema_accepts_zero_models_and_no_discriminator(self):
        payload = final_v02("T00", causal_status="NO_SUPPORTED_MODEL")
        payload["causal_structure"]["relation"] = "NOT_APPLICABLE"
        jsonschema.validate(payload, self.schema)

    def test_reduced_packet_is_self_contained_not_external_reference_dependent(self):
        text = (PROTOCOL / "REDUCED-SELF-CONTAINED-PACKET.md").read_text(encoding="utf-8")
        self.assertNotIn("protocol-details.md", text)
        self.assertNotIn("see §", text.lower())
        self.assertIn("Evidence and provenance", text)
        self.assertIn("Coverage gate", text)


class V02ConformanceExecutionTests(unittest.TestCase):
    def test_forced_conditional_branches_leave_artifacts_and_fail_closed(self):
        scripted = ScriptedFullCall()
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            final = cg.execute_full_v02(
                case_id="T01",
                material="E01 test evidence",
                contract="test contract",
                mandates=["m1", "m2", "m3"],
                call_json=scripted,
                final_schema=json.loads((PROTOCOL / "OUTPUT-SCHEMA-v0.2.json").read_text(encoding="utf-8")),
                run_dir=run_dir,
                max_corrective_cycles=4,
            )
            completion = final["protocol_completion"]
            self.assertEqual(completion["status"], "PARTIAL_PROTOCOL")
            self.assertIn("B2-search-4", scripted.calls)
            self.assertIn("C3-boundary", scripted.calls)
            self.assertTrue(any(s.startswith("C4-checkpoint-search-") for s in scripted.calls))
            self.assertTrue((run_dir / "working" / "D1-revision-cycle-2.json").exists())
            self.assertTrue(any(s.startswith("D2-reroute-search-") for s in scripted.calls))
            self.assertIn("D2-adjudication-rerun", scripted.calls)
            self.assertIn("D3-second-opinion", scripted.calls)
            self.assertTrue(any("D2/D3 conflict" in x for x in completion["material_omissions"]))
            self.assertTrue((run_dir / "working" / "protocol-ledger.json").exists())

    def test_zero_finalist_path_does_not_pad(self):
        scripted = ZeroFinalistCall()
        with tempfile.TemporaryDirectory() as tmp:
            final = cg.execute_full_v02(
                case_id="T00",
                material="E01 test evidence",
                contract="test contract",
                mandates=["m1", "m2", "m3"],
                call_json=scripted,
                final_schema=json.loads((PROTOCOL / "OUTPUT-SCHEMA-v0.2.json").read_text(encoding="utf-8")),
                run_dir=Path(tmp),
            )
            self.assertEqual(final["causal_structure"]["status"], "NO_SUPPORTED_MODEL")
            self.assertFalse(any(stage.startswith("D1-dossier-") for stage in scripted.calls))


class IsolationAblationIntegrityTests(unittest.TestCase):
    def test_isolated_history_manipulation_cannot_change_search_prompt(self):
        material = "evidence"
        contract = "contract"
        mandate = "mandate"
        a = ablation.search_prompt(
            material=material,
            contract=contract,
            mandate=mandate,
            shared_history=None,
            prior_outputs=[],
        )
        b = ablation.search_prompt(
            material=material,
            contract=contract,
            mandate=mandate,
            shared_history=None,
            prior_outputs=[],
        )
        self.assertEqual(a.encode("utf-8"), b.encode("utf-8"))
        self.assertNotIn("PARENT CONTEXT HISTORY", a)

    def test_shared_prompt_contains_history_but_synthesis_does_not(self):
        search = ablation.search_prompt(
            material="evidence",
            contract="contract",
            mandate="mandate",
            shared_history="FALSE ANCHOR",
            prior_outputs=[{"models": []}],
        )
        synth = ablation.synth_prompt(
            case_id="T01",
            material="evidence",
            contract="contract",
            search_outputs=[{"models": []}],
        )
        self.assertIn("FALSE ANCHOR", search)
        self.assertNotIn("FALSE ANCHOR", synth)


if __name__ == "__main__":
    unittest.main()
