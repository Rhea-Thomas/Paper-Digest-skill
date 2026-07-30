# Paper Digest — a Claude Skill

A [Claude Skill](https://docs.claude.com) that turns an academic paper (PDF) into a
short, structured digest: **Problem → Method → Key Results → Limitations**. Built to
help quickly triage whether a paper is worth reading in full.

![CI](https://github.com/Rhea-Thomas/paper-digest-skill/actions/workflows/ci.yml/badge.svg)

## How it works (system design)

The skill is split into two stages, deliberately kept separate:

```
   PDF file
      |
      v
+-----------------+        deterministic, no LLM call
| extract_text.py |  <-------------------------------
+-----------------+
      |
      v
  raw paper text
      |
      v
+---------------------+     generative, follows SKILL.md
| Claude (synthesis)  |  <----------------------------
+---------------------+
      |
      v
 structured digest (Problem / Method / Results / Limitations)
```

**Why split it this way?**
- **Extraction is deterministic** — the same PDF always produces the same text, so it
  belongs in a plain script, not an LLM call. This makes it fast, free to run, and
  independently unit-testable (see `tests/test_skill.py`).
- **Synthesis is generative** — turning raw text into a structured, judgment-based
  summary is where a model adds value, so that's the only step that costs tokens.

This keeps the skill cheap to run repeatedly and easy to test in isolation — the
extraction script has full test coverage with no dependency on any API.

## Repo structure

```
paper-digest-skill/
├── SKILL.md                    # Skill definition (frontmatter + instructions)
├── scripts/
│   └── extract_text.py         # Deterministic PDF -> text extraction
├── tests/
│   ├── test_skill.py           # Unit tests for extraction + SKILL.md validity
│   └── make_sample_pdf.py       # Generates the sample PDF used in tests
├── examples/
│   ├── sample_paper.pdf         # Tiny synthetic sample paper
│   └── sample_digest_output.md  # Example output of the full pipeline
├── requirements.txt              # Runtime deps
├── requirements-dev.txt          # Test-only deps
└── .github/workflows/ci.yml      # CI: runs the test suite on every push
```

## Usage

1. Install the skill in Claude (Claude.ai or Claude Code) by pointing it at this
   folder, or package it into a `.skill` file.
2. Give Claude a paper — upload a PDF or point it to one.
3. Ask something like *"summarize this paper"* or *"what's the key finding here"* —
   the skill triggers automatically and runs the pipeline above.

See `examples/sample_digest_output.md` for a full sample run.

## Running tests locally

```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest tests/ -v
```

## CI/CD

Every push to `main` (and every pull request) runs the full test suite via
GitHub Actions (`.github/workflows/ci.yml`). This catches broken extraction logic
or malformed `SKILL.md` frontmatter before it merges.
