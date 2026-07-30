"""
Test suite for the paper-digest skill.

Run with: pytest tests/
"""
import os
import sys
import subprocess

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")
SAMPLE_PDF = os.path.join(REPO_ROOT, "examples", "sample_paper.pdf")
EXTRACT_SCRIPT = os.path.join(REPO_ROOT, "scripts", "extract_text.py")
SKILL_MD = os.path.join(REPO_ROOT, "SKILL.md")


def run_extract(pdf_path):
    result = subprocess.run(
        [sys.executable, EXTRACT_SCRIPT, pdf_path],
        capture_output=True,
        text=True,
    )
    return result


def test_extract_returns_known_content():
    result = run_extract(SAMPLE_PDF)
    assert result.returncode == 0
    assert "Efficient Retrieval" in result.stdout
    assert "62.3 EM" in result.stdout


def test_extract_missing_file_fails_cleanly():
    result = run_extract("does_not_exist.pdf")
    assert result.returncode == 1
    assert "not found" in result.stderr.lower()


def test_skill_md_has_required_frontmatter():
    with open(SKILL_MD) as f:
        content = f.read()

    assert content.startswith("---"), "SKILL.md must start with YAML frontmatter"

    frontmatter = content.split("---")[1]
    assert "name:" in frontmatter, "SKILL.md frontmatter missing 'name'"
    assert "description:" in frontmatter, "SKILL.md frontmatter missing 'description'"


def test_skill_md_under_line_limit():
    with open(SKILL_MD) as f:
        lines = f.readlines()
    # Best practice ceiling for SKILL.md files: keep under 500 lines
    assert len(lines) < 500, "SKILL.md is getting long -- consider splitting into references/"


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
