from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "harness"
P01 = ROOT / "cases" / "pilot" / "P01"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


vf = load_module("validate_final", HARNESS / "validate_final.py")


def valid_payload() -> dict:
    return {
        "case_id": "P01",
        "causal_assessment": {
            "status": "CHOOSE",
            "candidate_causes": [
                {"id": "C1", "claim": "The deployed database hostname is invalid."}
            ],
            "preferred_cause": "C1",
        },
        "action": {
            "recommended_action": "Restore the previous database hostname.",
            "reason": "The deployment diff and DNS probe identify the bad hostname.",
        },
        "evidence": [
            {
                "evidence_ids": ["E01", "E02", "E03"],
                "claim": "The new hostname fails while the old hostname resolves.",
            }
        ],
        "uncertainty": ["Verify recovery after the reversible correction."],
        "next_test": {
            "test": "Correct the hostname in a canary and run one checkout.",
            "outcome_a_implication": "Recovery supports the configuration mechanism.",
            "outcome_b_implication": "Continued failure implies another cause.",
        },
    }


class ValidateFinalTests(unittest.TestCase):
    def setUp(self):
        self.case_id, self.evidence_ids = vf.discover_case(P01)

    def validate(self, payload: dict) -> list[str]:
        return vf.validate(
            payload,
            expected_case_id=self.case_id,
            allowed_evidence_ids=self.evidence_ids,
        )

    def test_valid_payload_passes(self):
        self.assertEqual(self.validate(valid_payload()), [])

    def test_extra_root_field_fails(self):
        payload = valid_payload()
        payload["extra"] = "forbidden"
        self.assertTrue(any("unsupported field extra" in e for e in self.validate(payload)))

    def test_missing_preferred_cause_fails(self):
        payload = valid_payload()
        del payload["causal_assessment"]["preferred_cause"]
        self.assertTrue(any("missing preferred_cause" in e for e in self.validate(payload)))

    def test_unknown_evidence_id_fails(self):
        payload = valid_payload()
        payload["evidence"][0]["evidence_ids"] = ["E99"]
        self.assertTrue(any("unknown case evidence E99" in e for e in self.validate(payload)))

    def test_case_mismatch_fails(self):
        payload = valid_payload()
        payload["case_id"] = "P02"
        self.assertTrue(any("does not match expected case" in e for e in self.validate(payload)))

    def test_choose_requires_candidate_binding(self):
        payload = valid_payload()
        payload["causal_assessment"]["preferred_cause"] = "C9"
        self.assertTrue(any("must match one candidate" in e for e in self.validate(payload)))

    def test_insufficient_requires_null_preference(self):
        payload = valid_payload()
        payload["causal_assessment"]["status"] = "INSUFFICIENT"
        self.assertTrue(any("requires preferred_cause=null" in e for e in self.validate(payload)))


class StructuralScorerTests(unittest.TestCase):
    def test_scorer_emits_diagnostics_not_primary_scores(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            final_path = tmp / "final.json"
            key_path = tmp / "key.json"
            final_path.write_text(json.dumps(valid_payload()), encoding="utf-8")
            key_path.write_text(
                json.dumps(
                    {
                        "case_id": "P01",
                        "causal_structure": {"acceptable_status": ["CHOOSE"]},
                    }
                ),
                encoding="utf-8",
            )
            proc = subprocess.run(
                [
                    sys.executable,
                    str(HARNESS / "score_structural.py"),
                    "--final",
                    str(final_path),
                    "--key",
                    str(key_path),
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            data = json.loads(proc.stdout)
            self.assertIn("diagnostics_only", data)
            self.assertIn("semantic_judging_required", data)
            self.assertNotIn("premature_winner", data["diagnostics_only"])

    def test_scorer_rejects_case_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            final_path = tmp / "final.json"
            key_path = tmp / "key.json"
            payload = valid_payload()
            payload["case_id"] = "P02"
            final_path.write_text(json.dumps(payload), encoding="utf-8")
            key_path.write_text(
                json.dumps(
                    {
                        "case_id": "P01",
                        "causal_structure": {"acceptable_status": ["CHOOSE"]},
                    }
                ),
                encoding="utf-8",
            )
            proc = subprocess.run(
                [
                    sys.executable,
                    str(HARNESS / "score_structural.py"),
                    "--final",
                    str(final_path),
                    "--key",
                    str(key_path),
                ],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("case binding mismatch", proc.stderr + proc.stdout)


if __name__ == "__main__":
    unittest.main()
