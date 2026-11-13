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


### Spec Compliance

- ✅ Spec compliant for the reviewed implementation delta. All five requested paths are present in the diff: traversal, saved output, provenance, tests, and README. The additional AI-notes update records actual assistance and leaves human evidence pending (docs/catatan-ai.md:33–39).
- ✅ The public signature matches the brief; named children retain original child indices for field lookup, indentation is two spaces, rows are one-based and columns remain byte-based (tugas1-3/jelajah.py:9–15).
- ✅ CLI reads bytes, reports unreadable paths through argparse, and has a main guard (tugas1-3/jelajah.py:18–31). No dependency or package changes appear in the delta.
- ✅ Exact assignment output and UTF-8 byte positions are asserted, with importlib loading for the hyphenated folder; CLI success, missing-file errors, and quiet execution on import are covered (tests/test_tugas_awal.py:18–64).
- ✅ Real-source provenance, SHA, license, clone command, source size, generation command, and three source/output checks are documented (docs/bahan-uji.md:3–31). A focused external-source read independently confirmed 4018 lines and the function, parameter annotation, and class at source lines 62, 63, and 197. Saved output agrees at tugas1-3/output/t2.txt:329–335 and :942–949.
- ⚠️ The diff cannot independently prove historical RED/GREEN execution, clone-time SHA/license state, or every line of the generated artifact. The implementation report records three expected missing-file errors before implementation, then all five tests passing and diff-check exit 0. No reported warning/noise was present. Controller owns commit/push; these are explicitly pending and outside this uncommitted delta. Human Playground/handwriting evidence remains pending (tugas1-3/README.md:50; docs/bahan-uji.md:31).

### Strengths

- The implementation is 31 lines and directly uses the required parser API and existing dependencies; it adds no wrapper or configuration surface (tugas1-3/jelajah.py:1–31).
- Traversal looks up fields on the original children sequence, correctly handling anonymous punctuation; exact-output tests exercise the assignment operator case (tugas1-3/jelajah.py:13–15; tests/test_tugas_awal.py:25–36).
- Provenance separates the external source from the assignment repository and explicitly distinguishes machine checks from pending personal evidence (docs/bahan-uji.md:5–12,23–31).

### Issues

#### Critical (Must Fix)

None found.

#### Important (Should Fix)

None found.

#### Minor (Nice to Have)

None found that warrant a change for this task.

### Assessment

**Task quality:** Approved.

**Reasoning:** The small recursive implementation satisfies the requested interface and output semantics, and the tests exercise real parser nodes and CLI behavior. Required source/output samples match the external Python source inspected in one focused provenance check.

**Checks and limitations:** Read complete source/test/document diff hunks and selected saved-output ranges; no changed files were separately reread. Named external-source check: ensure documented output coordinates correspond to a real >=100-line Python source; checked only its line count and source lines 62–64 and 197. Did not rerun already-passing suites, mutate code/index/branch, inspect the entire 15307-line artifact, or verify clone history. Recursive traversal retains the documented Python recursion-depth limit for exceptionally deep input; this follows the requested recursive design.


### Spec Compliance

- ✅ Spec compliant for Task 3. The task delta supplies all requested files: runner, three patterns, exact fixture, recorded three-command output, tests, README comparison, and factual AI notes. Commit/push remains coordinator-owned as instructed.
- ✅ Exact function contract: `jalankan(src: bytes, pola: str) -> list[str]` uses Python 0.25 `Parser(language)`, `Query`, and `QueryCursor`; per-match name/parameter pairing excludes `/`, `*`, and comments while counting splats (`tugas1-3/q.py:9`, `tugas1-3/q.py:14`, `tugas1-3/q.py:17`). The mandatory fixture has five parameters and an empty function (`tugas1-3/contoh/query.py:1`); exact expected results are asserted (`tests/test_tugas_awal.py:35`).
- ✅ Direct-print contract: an identifier callee plus equality predicate excludes attribute calls and string contents (`tugas1-3/queries/print.scm:1`); fixture negatives and sole line-3 positive agree with the exact assertion and saved output (`tugas1-3/contoh/query.py:3`, `tests/test_tugas_awal.py:41`, `tugas1-3/output/t3.txt:6`).
- ✅ Module contract: ordinary imports capture original dotted names through aliased imports; from-imports capture module_name, preserving relative prefixes (`tugas1-3/queries/import.scm:1`, `tugas1-3/queries/import.scm:7`). Exact os/sys/pathlib/./..paket results and source lines agree across fixture, test, and artifact (`tugas1-3/contoh/query.py:6`, `tests/test_tugas_awal.py:45`, `tugas1-3/output/t3.txt:9`).
- ✅ CLI reads byte source and UTF-8 patterns, reports unreadable paths and invalid queries through argparse nonzero errors, prints each returned line, and has a main guard (`tugas1-3/q.py:31`, `tugas1-3/q.py:36`, `tugas1-3/q.py:42`, `tugas1-3/q.py:49`). Error/quiet-import tests exercise these behaviors (`tests/test_tugas_awal.py:49`).
- ⚠️ Grammar-tree discovery and subprocess/AST comparison execution are supported by the implementer report, not independently observable from the task diff. The report includes complete RED/GREEN output and independent AST results; no contradictory or noisy output is present. User understanding/handwritten evidence remains explicitly pending and is outside this task gate.

### Strengths

- Query patterns express the requested syntactic distinctions directly without a custom walker or new dependencies (`tugas1-3/queries/fungsi.scm:1`, `tugas1-3/queries/print.scm:1`, `tugas1-3/queries/import.scm:1`).
- Tests assert concrete results rather than mocks, including UTF-8 names and the standalone keyword separator in addition to the mandatory fixture (`tests/test_tugas_awal.py:33`).
- Saved evidence matches every required source item: two functions, one direct print, five original module names, and one-based import/print lines (`tugas1-3/output/t3.txt:1`, `tugas1-3/contoh/query.py:1`). README adds the corresponding source-by-source manual table and accurately labels it AI-generated rather than user handwriting (`tugas1-3/README.md:52`).

### Issues

#### Critical (Must Fix)

None.

#### Important (Should Fix)

None.

#### Minor (Nice to Have)

None.

### Assessment

**Task quality:** Approved.

**Reasoning:** The implementation meets the exact required fixture behavior and keeps the runner small, with correct match pairing, import alias handling, and readable CLI failures. The tests and output artifact give concrete evidence for the required contracts.

**Checks and limits:** Read the supplied brief, binding constraints, full implementer report, and task-only diff once; reviewed the diff against the fixture and literal outputs. No changed-file rereads, broader repository crawl, git commands, edits to product files, or tests were performed. Existing complete nine-test GREEN evidence answers the task's concrete behavior checks, so no additional focused run was warranted. UTF-8 input and syntactic print matching are documented limits; no new merge-blocking risk was found. Prior approved Task 2 work and later tasks were outside this review.
