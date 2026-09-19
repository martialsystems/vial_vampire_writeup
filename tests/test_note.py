# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
NOTE = REPO / "NOTE.md"
README = REPO / "README.md"
SHAS = (
    "e2e22b7",
    "97aa7c8",
    "7e32830",
    "4946ab5",
    "69f4f6d",
    "b106228",
    "ddb73a8",
    "fa819c7",
    "12d6952",
    "e843b8c",
)
INDEX = "12835f747d6360781f3cc7f91f243178"


def test_note_lede() -> None:
    text = NOTE.read_text(encoding="utf-8")
    assert text.startswith("# Closed-vial vampire claims: note\n")
    body = text.split("\n", 1)[1].lstrip()
    assert body.startswith("Locks stay on the trees.")
    assert "What this is not" not in text
    assert "What it is not" not in text
    assert "\u2014" not in text
    assert INDEX in text
    for sha in SHAS:
        assert sha in text
    assert "0.524" in text
    assert "5.74" in text
    assert "t_first_biter=211" in text
    assert "fa819c7" in text
    assert "e843b8c" in text
    assert "93.34" in text
    words = re.findall(r"[A-Za-z0-9][A-Za-z0-9'./_-]*", text)
    assert 1400 <= len(words) <= 3200


def test_readme_points_at_note_and_index() -> None:
    text = README.read_text(encoding="utf-8")
    assert text.startswith("# vial_vampire_writeup\n")
    assert "NOTE.md" in text
    assert "vial_vampire_note.pdf" in text
    assert INDEX in text
    assert "52747cfd" in text
    assert "\u2014" not in text
    desc = (REPO / "description.txt").read_text(encoding="utf-8")
    assert "12835f74" in desc
    assert "\u2014" not in desc
    agents = (REPO / "AGENTS.md").read_text(encoding="utf-8")
    assert "not a finding tree" in agents
    assert "citation columns" in agents


def test_pdf_and_figure_exist() -> None:
    import pypdfium2 as pdfium

    pdf_path = REPO / "docs" / "vial_vampire_note.pdf"
    fig = REPO / "figures" / "stack.png"
    assert pdf_path.is_file() and pdf_path.stat().st_size > 1000
    assert fig.is_file() and fig.stat().st_size > 1000
    pdf = pdfium.PdfDocument(str(pdf_path))
    text = "\n".join(pdf[i].get_textpage().get_text_bounded() for i in range(len(pdf)))
    assert "Abstract" in text
    assert "Keywords" in text
    assert "Revisions" in text
    assert "2026-09-16" in text
    assert "e2e22b7" in text
    assert "4946ab5" in text
    assert "e843b8c" in text
    assert "5.74" in text
    assert "------" not in text
    assert "What it is not" not in text
    assert "\u2014" not in text
    assert len(pdf) >= 3
