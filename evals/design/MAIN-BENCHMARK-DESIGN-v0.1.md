# Main Benchmark Design v0.1 — frozen public design

Status: **FROZEN FOR MAIN STUDY.** No participant main-study run had been executed when this design was frozen.

This public document records the benchmark structure without exposing answer-bearing hidden keys. P01/P02 remain pilot-only and are not reused.

## Purpose

The benchmark tests where Convergence Guard improves decision-relevant causal reasoning enough to justify its additional cost, and where it instead creates over-analysis or over-abstention. Results must be analyzed both overall and by predeclared causal-difficulty regimes.

## Difficulty scale

Nine dimensions use a 1–5 challenge scale: hypothesis-space breadth, evidence separability, confounding/interaction, evidence quality, framing risk, testability, reversibility, cost of premature commitment, and sufficiency-boundary difficulty.

Higher numbers mean a harder causal-reasoning challenge. For evidence quality, testability, and reversibility, higher means noisier/weaker evidence, harder testing, and less reversible decisions.

## Case progression

- M01 is deliberately narrow and low-ambiguity.
- M02 adds a strong temporally correlated distractor.
- M03 adds several serious alternative causal models and discriminating intervention evidence.
- M04 increases sufficiency-boundary difficulty.
- M05 adds evidence-dependence and framing pressure.
- M06 changes the causal topology from a single homogeneous incident to heterogeneous simultaneous branches.
- M07 adds interaction/layered causality.
- M08 is a 22-document mini open-world investigation with mixed provenance and an incomplete prompt-supplied hypothesis space.

The public descriptions intentionally do not disclose the keyed semantic status, preferred cause, decisive evidence set, calibration truth labels, or case-specific judge anchors. Those are stored outside the repository in the private eval tree.

## Freeze rules

Before the first main participant run, freeze the case-class mapping, difficulty vectors, public evidence, hidden truth, acceptable semantic status, action families, decisive evidence, evidence ancestry, calibration truth labels, judge anchors, model/runtime/settings, maximum resource budget, normalization version, randomization seed/run plan, and harness/CG hashes.

Literal status-token matching remains diagnostic only. Winner/abstention scoring is semantic against the private key and blind rubric. No post-hoc single weighted score is permitted.
