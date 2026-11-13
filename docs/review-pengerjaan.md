# Task 1 independent review

What this change does: Adds three Python syntax-tree examples, one broken example, saved output, predictions labelled as AI, and two tests. It explains named and anonymous children and keeps the user's handwriting requirement open.

## Spec Compliance verdict

**PASS for the authorized Task 1 implementation scope. Human submission remains incomplete.**

Reviewed the Task 1 brief, global constraints, implementation report, and complete implementation portions of `task-1-review-package.diff`. The approved plan-file addition is permitted scope, not an extra Task 1 implementation requirement. Consulted the original Tugas 1 instructions (lines 333–383), existing setup script and requirements, and searched references to the new script/test to check their integration.

- Fixtures match the required function, if/else, class with one method, and missing-colon case. Python source is read as bytes.
- `t1.py:8` exposes `main() -> None`; the guard at line 40 prevents running examples on import. Paths resolve relative to the script, so execution does not depend on the caller's working directory.
- `output/t1.txt:1` contains the three expected root structures, each with `has_error: False`; lines 6–14 identify `def`, `:`, `(` and `)` as anonymous. Lines 28–29 show ERROR and `has_error: True` for the broken function.
- `tests/test_tugas_awal.py:15` checks valid/invalid trees and decodes the complete UTF-8 string node from byte offsets, preserving `José`. The second test checks the script's public output and quiet loading.
- `tugas1-3/README.md:21` correctly explains direct children versus named children, including the deeper parameter punctuation.
- `perkiraan.md` preserves the AI predictions and records the actual string-node detail omitted from the condition prediction. The saved trees agree with the fixtures and comparison text. AI notes describe the actual limitation without claiming a user-authored prediction or manual Playground result.
- The implementation report records Python 3.12.15, installed compatible-series bindings and CLI 0.25.10, setup success, the missing-file RED run, and both tests passing after implementation. CLI grammar generation is expressly deferred to Task 4, consistent with this task boundary.

The original assignment's handwritten predictions and personal explanation/Playground activity are not fulfilled by these machine artifacts. `perkiraan.md:29`, the README checklist, and AI notes honestly leave them pending. This is an outstanding human requirement, not grounds to ask the implementer to fabricate evidence or block the reviewed code. The coordinator must keep that submission status open.

## Strengths

- Small implementation using the existing dependencies and standard-library unittest; no new abstraction or dependency.
- Exact teaching examples show the difference between named nodes and anonymous punctuation without hiding error recovery.
- Byte slicing and a multibyte fixture directly address the UTF-8 failure mode.
- Saved output, prediction comparison, and AI notes agree; no claim of MISSING when this parser actually returns ERROR.
- Expected load is one student running a local teaching script over four small checked-in fixtures. There are no service, concurrency, or large-input requirements.

## Critical findings

None.

## Important findings

None.

## Minor findings

None with a concrete Task 1 impact. No speculative features or cosmetic rewrites requested.

## Verification and limits

Inspected the saved output, source and tests in the review package, references in the repository, and original assignment wording. The initial combined read truncated only part of the approved plan-file context; all implementation, tests, output and prediction sections were visible. No changed implementation file needed to be reread.

The implementer's report records `.venv/bin/python -m unittest discover -s tests -p test_tugas_awal.py -v` and full discovery passing two tests, direct output generation succeeding, setup printing a valid module, and `git diff --check` passing. These are reported execution results, not fresh reviewer runs. Following the review instruction, I did not repeat a passing suite without a specific unanswered doubt. No executable claim required an additional focused check from this inspection. Prediction-before-parse chronology is documented by the implementer and cannot be reconstructed independently from the final snapshot alone.

## Task quality verdict

**Approved.** No implementation correction required before coordinator integration.

Verdict: Ship the reviewed implementation; keep human submission requirements open.

Not checked: fresh suite execution, independent reconstruction of prediction chronology, user handwriting/Playground understanding, or CLI generation (Task 4). Risk: approval of the code must not be represented as completion of the human assignment evidence.
