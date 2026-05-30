from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
OUTPUT = ROOT / "Scholarship_Eligibility_Checker_Documentation.pdf"


def clean_inline(text):
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"`([^`]+)`", r"<font name='Courier'>\1</font>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    return text


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#60727d"))
    canvas.drawString(0.72 * inch, 0.45 * inch, "Scholarship Eligibility Checker - Project Documentation")
    canvas.drawRightString(A4[0] - 0.72 * inch, 0.45 * inch, f"Page {doc.page}")
    canvas.restoreState()


def build_pdf():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="CoverTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=26,
            leading=32,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#0d4d43"),
            spaceAfter=18,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverSub",
            parent=styles["BodyText"],
            fontSize=11,
            leading=16,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#60727d"),
            spaceAfter=10,
        )
    )
    styles.add(
        ParagraphStyle(
            name="H1Custom",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=23,
            textColor=colors.HexColor("#126b5c"),
            spaceBefore=14,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="H2Custom",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=17,
            textColor=colors.HexColor("#17202a"),
            spaceBefore=10,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyCustom",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=14,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CodeCustom",
            parent=styles["Code"],
            fontName="Courier",
            fontSize=8,
            leading=11,
            backColor=colors.HexColor("#f5f8f6"),
            borderColor=colors.HexColor("#d8e1e3"),
            borderWidth=0.5,
            borderPadding=6,
            spaceBefore=4,
            spaceAfter=8,
        )
    )

    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=0.72 * inch,
        leftMargin=0.72 * inch,
        topMargin=0.72 * inch,
        bottomMargin=0.72 * inch,
        title="Scholarship Eligibility Checker Documentation",
        author="Gnanender",
    )

    content = []
    content.append(Spacer(1, 1.2 * inch))
    content.append(Paragraph("Scholarship Eligibility Checker", styles["CoverTitle"]))
    content.append(Paragraph("Formal Project Documentation", styles["CoverSub"]))
    content.append(
        Paragraph(
            "SchemeSetu is a scholarship eligibility checker for matching student profiles with structured scholarship rules.",
            styles["CoverSub"],
        )
    )
    content.append(Spacer(1, 0.25 * inch))
    meta = [
        ["Live Demo", "https://gnanenderchinnu.github.io/scholorship-eligibility-checker/"],
        ["Repository", "https://github.com/GnanenderChinnu/scholorship-eligibility-checker"],
        ["Stack", "Django, SQLite, HTML, CSS, JavaScript"],
    ]
    table = Table(meta, colWidths=[1.3 * inch, 4.8 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#edf5f2")),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#0d4d43")),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#d8e1e3")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    content.append(table)
    content.append(PageBreak())

    lines = README.read_text(encoding="utf-8").splitlines()
    in_code = False
    code_lines = []
    bullet_items = []
    table_rows = []

    def flush_bullets():
        nonlocal bullet_items
        if bullet_items:
            content.append(
                ListFlowable(
                    [ListItem(Paragraph(clean_inline(item), styles["BodyCustom"])) for item in bullet_items],
                    bulletType="bullet",
                    leftIndent=18,
                )
            )
            bullet_items = []

    def flush_table():
        nonlocal table_rows
        if table_rows:
            data = [[Paragraph(clean_inline(cell.strip()), styles["BodyCustom"]) for cell in row] for row in table_rows]
            tbl = Table(data, hAlign="LEFT")
            tbl.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#edf5f2")),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#d8e1e3")),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 6),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                        ("TOPPADDING", (0, 0), (-1, -1), 5),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                    ]
                )
            )
            content.append(tbl)
            content.append(Spacer(1, 6))
            table_rows = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            if in_code:
                content.append(Paragraph("<br/>".join(clean_inline(l) for l in code_lines), styles["CodeCustom"]))
                code_lines = []
                in_code = False
            else:
                flush_bullets()
                flush_table()
                in_code = True
            continue
        if in_code:
            code_lines.append(line)
            continue
        if not stripped:
            flush_bullets()
            flush_table()
            continue
        if stripped.startswith("|") and not re.match(r"^\|\s*-", stripped):
            cells = [cell.strip() for cell in stripped.strip("|").split("|")]
            table_rows.append(cells)
            continue
        if re.match(r"^\|\s*-", stripped):
            continue
        flush_table()
        if stripped.startswith("# "):
            flush_bullets()
            continue
        if stripped.startswith("## "):
            flush_bullets()
            content.append(Paragraph(clean_inline(stripped[3:]), styles["H1Custom"]))
            continue
        if stripped.startswith("### "):
            flush_bullets()
            content.append(Paragraph(clean_inline(stripped[4:]), styles["H2Custom"]))
            continue
        if stripped.startswith("- "):
            bullet_items.append(stripped[2:])
            continue
        if re.match(r"^\d+\. ", stripped):
            bullet_items.append(re.sub(r"^\d+\. ", "", stripped))
            continue
        flush_bullets()
        content.append(Paragraph(clean_inline(stripped), styles["BodyCustom"]))

    flush_bullets()
    flush_table()
    doc.build(content, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    build_pdf()
    print(OUTPUT)
