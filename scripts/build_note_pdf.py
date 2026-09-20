#!/usr/bin/env python3
# Copyright (c) 2026 Martial Systems LLC
"""Research-format PDF of NOTE.md. Locks stay on the trees."""

from __future__ import annotations

import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (
    Image,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "NOTE.md"
FIG = ROOT / "figures" / "stack.png"
OUT = ROOT / "docs" / "vial_vampire_note.pdf"

DATE = "2026-09-16"
TITLE = "Vampire-as-bite and vampire-as-mosquito-thief in the closed-vial engines"


def styles():
    s = getSampleStyleSheet()
    s.add(
        ParagraphStyle(
            name="PaperTitle",
            fontName="Times-Bold",
            fontSize=13,
            leading=16,
            alignment=TA_CENTER,
            spaceAfter=8,
        )
    )
    s.add(
        ParagraphStyle(
            name="Meta",
            fontName="Times-Roman",
            fontSize=10,
            leading=13,
            alignment=TA_CENTER,
            spaceAfter=4,
        )
    )
    s.add(
        ParagraphStyle(
            name="AbsHead",
            fontName="Times-Bold",
            fontSize=11,
            leading=14,
            spaceBefore=12,
            spaceAfter=6,
        )
    )
    s.add(
        ParagraphStyle(
            name="AbsBody",
            fontName="Times-Roman",
            fontSize=10,
            leading=13,
            alignment=TA_JUSTIFY,
            spaceAfter=7,
            firstLineIndent=0,
        )
    )
    s.add(
        ParagraphStyle(
            name="H",
            fontName="Times-Bold",
            fontSize=11,
            leading=14,
            spaceBefore=12,
            spaceAfter=6,
        )
    )
    s.add(
        ParagraphStyle(
            name="H3",
            fontName="Times-Bold",
            fontSize=10,
            leading=13,
            spaceBefore=9,
            spaceAfter=5,
        )
    )
    s.add(
        ParagraphStyle(
            name="BodyJ",
            fontName="Times-Roman",
            fontSize=10,
            leading=13,
            alignment=TA_JUSTIFY,
            spaceAfter=7,
            firstLineIndent=12,
        )
    )
    s.add(
        ParagraphStyle(
            name="BodyJ0",
            fontName="Times-Roman",
            fontSize=10,
            leading=13,
            alignment=TA_JUSTIFY,
            spaceAfter=7,
            firstLineIndent=0,
        )
    )
    s.add(
        ParagraphStyle(
            name="Cap",
            fontName="Times-Italic",
            fontSize=9,
            leading=12,
            alignment=TA_LEFT,
            spaceBefore=4,
            spaceAfter=10,
        )
    )
    s.add(
        ParagraphStyle(
            name="Cell",
            fontName="Times-Roman",
            fontSize=7.5,
            leading=9.5,
        )
    )
    s.add(
        ParagraphStyle(
            name="CellB",
            fontName="Times-Bold",
            fontSize=7.5,
            leading=9.5,
        )
    )
    s.add(
        ParagraphStyle(
            name="Kw",
            fontName="Times-Roman",
            fontSize=10,
            leading=13,
            spaceAfter=8,
        )
    )
    return s


def inline(text: str) -> str:
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"`([^`]+)`", r"<font face='Courier' size='7'>\1</font>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"<link href='\2'>\1</link>", text)
    return text


def parse_note() -> list[tuple[str, object]]:
    lines = NOTE.read_text(encoding="utf-8").splitlines()
    blocks: list[tuple[str, object]] = []
    i = 0
    if lines and lines[0].startswith("# "):
        i = 1
        while i < len(lines) and not lines[i].strip():
            i += 1
    while i < len(lines):
        line = lines[i]
        if line.startswith("### "):
            blocks.append(("h3", line[4:].strip()))
            i += 1
            continue
        if line.startswith("## "):
            blocks.append(("h", line[3:].strip()))
            i += 1
            continue
        if line.startswith("!["):
            i += 1
            continue
        if line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                raw = lines[i].strip()
                cells = [c.strip() for c in raw.strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c.replace(" ", "")) for c in cells):
                    rows.append(cells)
                i += 1
            blocks.append(("table", rows))
            continue
        if not line.strip():
            i += 1
            continue
        para = [line]
        i += 1
        while (
            i < len(lines)
            and lines[i].strip()
            and not lines[i].startswith("#")
            and not lines[i].startswith("|")
        ):
            para.append(lines[i])
            i += 1
        blocks.append(("p", " ".join(para)))
    return blocks


def col_widths(n: int, headers: list[str] | None = None) -> list[float]:
    usable = 6.5 * inch
    if n == 2:
        return [1.6 * inch, 4.9 * inch]
    if n == 4:
        return [1.15 * inch, 0.70 * inch, 2.80 * inch, 1.85 * inch]
    if n <= 0:
        return [usable]
    mate = bool(headers) and headers[1].lower() == "mate"
    if mate and n >= 7:
        first = 0.38 * inch
        second = 1.15 * inch
        rest = usable - first - second
        each = rest / (n - 2)
        return [first, second] + [each] * (n - 2)
    return [usable / n] * n


def header_footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont("Times-Roman", 8)
    canvas.drawString(inch, letter[1] - 0.55 * inch, "Closed-vial vampire claims  (locks stay on the trees)")
    canvas.drawRightString(letter[0] - inch, letter[1] - 0.55 * inch, DATE)
    canvas.line(inch, letter[1] - 0.62 * inch, letter[0] - inch, letter[1] - 0.62 * inch)
    canvas.drawCentredString(letter[0] / 2, 0.5 * inch, f"{doc.page}")
    canvas.restoreState()


def build() -> Path:
    st = styles()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    story = []
    story.append(Paragraph(TITLE, st["PaperTitle"]))
    story.append(
        Paragraph(
            "A note on the closed-vial vampire trees. Locks stay on the trees.",
            st["Meta"],
        )
    )
    story.append(Paragraph("Martial Systems LLC", st["Meta"]))
    story.append(Paragraph(DATE, st["Meta"]))
    story.append(
        Paragraph(
            "Index of locks: https://gist.github.com/martialsystems/12835f747d6360781f3cc7f91f243178",
            st["Meta"],
        )
    )

    blocks = parse_note()
    first_p = True
    in_abstract = False
    for kind, payload in blocks:
        if kind == "h":
            title = str(payload)
            if title.lower() == "abstract":
                story.append(Paragraph("Abstract", st["AbsHead"]))
                in_abstract = True
                first_p = True
                continue
            in_abstract = False
            if title.startswith("1."):
                story.append(Paragraph("Keywords", st["H"]))
                story.append(
                    Paragraph(
                        "Drosophila melanogaster; closed vial; IBD; prestomal rasp; bite share; mosquito kleptoparasitism; exudate; delayed kinship cap.",
                        st["Kw"],
                    )
                )
            story.append(Paragraph(inline(title), st["H"]))
            first_p = True
            continue
        if kind == "h3":
            in_abstract = False
            story.append(Paragraph(inline(str(payload)), st["H3"]))
            first_p = True
            continue
        if kind == "p":
            text = str(payload)
            if text.startswith("Locks stay on the trees."):
                continue
            if text.startswith("Figure 1"):
                continue
            if in_abstract:
                style = st["AbsBody"]
            elif first_p:
                style = st["BodyJ0"]
            else:
                style = st["BodyJ"]
            story.append(Paragraph(inline(text), style))
            first_p = False
            continue
        if kind == "table":
            rows = payload
            cell = st["Cell"]
            cellb = st["CellB"]
            data = []
            for r_i, row in enumerate(rows):
                data.append([Paragraph(inline(c), cellb if r_i == 0 else cell) for c in row])
            n = len(rows[0])
            widths = col_widths(n, rows[0])
            if len(widths) != n:
                widths = [6.5 * inch / n] * n
            tbl = Table(data, colWidths=widths, repeatRows=1)
            tbl.setStyle(
                TableStyle(
                    [
                        ("GRID", (0, 0), (-1, -1), 0.4, colors.Color(0.4, 0.4, 0.4)),
                        ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.92, 0.92, 0.92)),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 3),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                        ("TOPPADDING", (0, 0), (-1, -1), 2),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                    ]
                )
            )
            story.append(tbl)
            story.append(Spacer(1, 8))
            first_p = True

    if FIG.is_file():
        reader = ImageReader(str(FIG))
        iw, ih = reader.getSize()
        w = 6.5 * inch
        h = w * (ih / iw)
        img = Image(str(FIG), width=w, height=h)
        img.hAlign = "CENTER"
        story.append(
            KeepTogether(
                [
                    Paragraph(
                        "Figure 1. Parent F lock to bite arm to mosquito arm (2026-09-16).",
                        st["H"],
                    ),
                    img,
                    Paragraph(
                        "Lineage of locked trees. Not a new measurement.",
                        st["Cap"],
                    ),
                ]
            )
        )

    story.append(Paragraph("Revisions (2026-09-16)", st["H"]))
    story.append(
        Paragraph(
            "2026-09-16: first note from the locked vampire trees. Numbers copied from the origin JSON cited in each README. Index gist 12835f74 left unedited.",
            st["BodyJ0"],
        )
    )
    story.append(
        Paragraph(
            "2026-09-20: sources for MaleCNS (Berg et al., 2026), FlyWire (Dorkenwald et al., 2024), and Wright (1931). Accountability sentence. Cite parent fly_vial Release plus SWHID. No DOI. This PDF is not a software deposit.",
            st["BodyJ0"],
        )
    )

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=letter,
        leftMargin=inch,
        rightMargin=inch,
        topMargin=0.85 * inch,
        bottomMargin=0.75 * inch,
        title=TITLE,
        author="Martial Systems LLC",
        subject="Note on the closed-vial vampire trees. Locks stay on the trees.",
    )
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print("wrote", OUT)
    return OUT


if __name__ == "__main__":
    build()
