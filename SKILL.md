---
name: paper-digest
description: Turns an academic paper (PDF) into a structured literature-review note covering Problem, Method, Key Results, and Limitations. Use this skill whenever the user uploads or references an academic/research paper (arXiv, journal PDF, conference paper) and asks for a summary, digest, literature note, or "what does this paper say" — even if they don't use the word "digest" explicitly.
---

# Paper Digest

Produces a consistent, structured summary of an academic paper so a reader can decide in 60 seconds whether it's worth reading in full.

## How it works (system design)

This skill deliberately splits work between a deterministic script and the model, rather than doing everything as one LLM call:

1. **Extraction (script, deterministic)** — `scripts/extract_text.py` pulls raw text out of the PDF using `pypdf`. This step never changes between runs: same PDF in, same text out. Keeping it a script (not an LLM call) makes it fast, free, and testable.
2. **Synthesis (model, generative)** — Claude reads the extracted text and produces the structured digest below. This is the part that benefits from a model's understanding, so it's the only part that consumes tokens.

This separation matters for two reasons: it's cheaper (no need to re-run extraction logic through the model), and it's independently testable (the extraction script can be unit-tested; the synthesis step is evaluated qualitatively).

## Steps to follow

1. **Locate the PDF.** If the user uploaded a file, find its path (usually under `/mnt/user-data/uploads/`). If they gave a URL instead, fetch it first.
2. **Run the extraction script:**
   ```bash
   python scripts/extract_text.py <path-to-pdf>
   ```
   This prints the paper's raw text to stdout (truncated to a reasonable length for long papers).
3. **Synthesize the digest** from the extracted text, in this exact format:

   ```markdown
   # <Paper Title>

   **Authors:** <if identifiable>
   **Source:** <arXiv ID / venue if identifiable>

   ## Problem
   1-3 sentences: what gap or question is this paper addressing, and why does it matter?

   ## Method
   2-4 sentences: what approach did they take? Name the key technique/architecture/algorithm.

   ## Key Results
   Bullet points (2-4) with the concrete, quantitative findings — numbers, not vague claims.

   ## Limitations
   1-3 sentences: what the authors themselves acknowledge, or what's clearly missing/unaddressed.
   ```
4. **Do not pad or editorialize.** If a section (e.g. limitations) isn't clearly stated in the paper, say "Not explicitly discussed" rather than inventing content.
5. Keep the whole digest under ~200 words. This is a triage tool, not a full review.

## Notes

- If the PDF is a scanned image with no extractable text, tell the user extraction failed rather than guessing at content.
- Never fabricate citation counts, benchmark numbers, or author affiliations that aren't in the extracted text.
