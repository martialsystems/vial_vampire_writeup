#!/usr/bin/env python3
# Copyright (c) 2026 Martial Systems LLC
"""Lineage boxes: parent F lock to bite arm to mosquito arm."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
OUT_PDF = ROOT / "figures" / "stack.pdf"


def box(c: canvas.Canvas, x: float, y: float, w: float, h: float, title: str, lines: list[str], sha: str) -> None:
    c.setStrokeColorRGB(0.15, 0.15, 0.15)
    c.setFillColorRGB(0.97, 0.97, 0.97)
    c.roundRect(x, y, w, h, 3, fill=1, stroke=1)
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Times-Bold", 9)
    c.drawString(x + 6, y + h - 13, title)
    c.setFont("Times-Roman", 8)
    ty = y + h - 26
    for line in lines:
        c.drawString(x + 6, ty, line)
        ty -= 11
    c.setFont("Times-Italic", 8)
    c.drawString(x + 6, y + 7, sha)


def h_arrow(c: canvas.Canvas, x0: float, y: float, x1: float) -> None:
    c.setStrokeColorRGB(0.2, 0.2, 0.2)
    c.setFillColorRGB(0.2, 0.2, 0.2)
    c.line(x0, y, x1, y)
    path = c.beginPath()
    path.moveTo(x1, y)
    path.lineTo(x1 - 6, y + 3)
    path.lineTo(x1 - 6, y - 3)
    path.close()
    c.drawPath(path, fill=1, stroke=0)


def v_arrow(c: canvas.Canvas, x: float, y0: float, y1: float) -> None:
    c.setStrokeColorRGB(0.2, 0.2, 0.2)
    c.setFillColorRGB(0.2, 0.2, 0.2)
    c.line(x, y0, x, y1)
    path = c.beginPath()
    path.moveTo(x, y1)
    path.lineTo(x - 3, y1 + 6)
    path.lineTo(x + 3, y1 + 6)
    path.close()
    c.drawPath(path, fill=1, stroke=0)


def main() -> None:
    OUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    W, H = 7.4 * inch, 5.6 * inch
    c = canvas.Canvas(str(OUT_PDF), pagesize=(W, H))
    margin = 0.22 * inch
    bw, bh = 2.18 * inch, 1.22 * inch
    gapx, gapy = 0.20 * inch, 0.42 * inch
    xs = [margin + i * (bw + gapx) for i in range(3)]
    row_top = H - 0.22 * inch - bh
    row_mid = row_top - bh - gapy
    row_bot = row_mid - bh - gapy
    box(
        c,
        xs[0],
        row_top,
        bw,
        bh,
        "vial_culex",
        ["blank founders", "0 of 3; extinct t=5"],
        "science fa819c7",
    )
    box(
        c,
        xs[1],
        row_top,
        bw,
        bh,
        "fly_vial",
        ["k=3, N=1,000, 80 gen", "F=0.524 vs random 0.034"],
        "@e2e22b7",
    )

    bite = [
        ("vial_sanguis", ["crash, exudate recover", "k-NN kit at F=1"], "@97aa7c8"),
        ("vial_sanguis2", ["delayed-cap F about 0.23", "peak bite 5.74%"], "science 4946ab5"),
        ("vial_morsus", ["bridge T=400", "0 of 3; extinct t~400"], "science b106228"),
    ]
    for i, spec in enumerate(bite):
        box(c, xs[i], row_mid, bw, bh, *spec)
    for i in range(2):
        h_arrow(c, xs[i] + bw, row_mid + bh / 2, xs[i + 1])

    box(
        c,
        xs[2],
        row_bot,
        bw,
        bh,
        "vial_handoff",
        ["morsus t=200 mapped", "hemolymph 1.000; 0 of 3"],
        "science e843b8c",
    )

    # parent fly_vial (top center) to sanguis (mid left)
    c.setStrokeColorRGB(0.2, 0.2, 0.2)
    c.setFillColorRGB(0.2, 0.2, 0.2)
    c.line(xs[1] + bw / 2, row_top, xs[1] + bw / 2, row_mid + bh + 8)
    c.line(xs[1] + bw / 2, row_mid + bh + 8, xs[0] + bw / 2, row_mid + bh + 8)
    c.line(xs[0] + bw / 2, row_mid + bh + 8, xs[0] + bw / 2, row_mid + bh)
    path = c.beginPath()
    path.moveTo(xs[0] + bw / 2, row_mid + bh)
    path.lineTo(xs[0] + bw / 2 - 3, row_mid + bh + 6)
    path.lineTo(xs[0] + bw / 2 + 3, row_mid + bh + 6)
    path.close()
    c.setFillColorRGB(0.2, 0.2, 0.2)
    c.drawPath(path, fill=1, stroke=0)
    # morsus to handoff
    v_arrow(c, xs[2] + bw / 2, row_mid, row_bot + bh)

    c.setFont("Times-Italic", 8)
    c.drawString(margin, 0.16 * inch, "Bite arm under fly_vial. culex is a sibling. handoff maps morsus into the culex kitchen.")
    c.save()
    print("wrote", OUT_PDF)
    _pdf_to_png(OUT_PDF, ROOT / "figures" / "stack.png")


def _pdf_to_png(pdf_path: Path, png_path: Path) -> None:
    import pypdfium2 as pdfium

    doc = pdfium.PdfDocument(str(pdf_path))
    doc[0].render(scale=2.0).to_pil().save(str(png_path), "PNG")
    print("wrote", png_path)


if __name__ == "__main__":
    main()
