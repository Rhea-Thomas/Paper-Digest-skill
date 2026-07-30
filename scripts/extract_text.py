#!/usr/bin/env python3
"""
Extract text from a PDF for the paper-digest skill.

Usage:
    python extract_text.py <path-to-pdf> [--max-chars 20000]

Prints extracted text to stdout. This script is intentionally deterministic
and dependency-light (pypdf only) so it can be unit tested independently
of any LLM call.
"""
import sys
import argparse
from pypdf import PdfReader


def extract_text(pdf_path: str, max_chars: int = 20000) -> str:
    reader = PdfReader(pdf_path)
    chunks = []
    total_len = 0

    for page in reader.pages:
        page_text = page.extract_text() or ""
        chunks.append(page_text)
        total_len += len(page_text)
        if total_len >= max_chars:
            break

    full_text = "\n".join(chunks)
    return full_text[:max_chars]


def main():
    parser = argparse.ArgumentParser(description="Extract text from a PDF.")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument(
        "--max-chars",
        type=int,
        default=20000,
        help="Maximum number of characters to extract (default: 20000)",
    )
    args = parser.parse_args()

    try:
        text = extract_text(args.pdf_path, args.max_chars)
    except FileNotFoundError:
        print(f"ERROR: file not found: {args.pdf_path}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: failed to extract text: {e}", file=sys.stderr)
        sys.exit(1)

    if not text.strip():
        print("ERROR: no extractable text found (likely a scanned/image PDF)", file=sys.stderr)
        sys.exit(2)

    print(text)


if __name__ == "__main__":
    main()
