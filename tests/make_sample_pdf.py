"""
Generates a tiny sample PDF (examples/sample_paper.pdf) with known text content,
used purely for testing the extraction script. Not part of the skill's runtime
dependencies -- reportlab is a test-only dependency.
"""
import os
from reportlab.pdfgen import canvas

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "examples", "sample_paper.pdf")

SAMPLE_TEXT = [
    "Efficient Retrieval for Small Language Models",
    "",
    "Abstract: We study whether small retrieval-augmented models can match",
    "larger models on question answering benchmarks.",
    "",
    "Method: We combine a lightweight dense retriever with a 1B parameter",
    "generator and evaluate on NaturalQuestions.",
    "",
    "Results: Our approach reaches 62.3 EM on NaturalQuestions, within 2 points",
    "of a 7B parameter baseline while using 6x less compute.",
    "",
    "Limitations: We only evaluate on English text and do not test",
    "multi-hop reasoning benchmarks.",
]


def main():
    c = canvas.Canvas(OUTPUT_PATH)
    y = 800
    for line in SAMPLE_TEXT:
        c.drawString(50, y, line)
        y -= 20
    c.save()
    print(f"Wrote sample PDF to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
