from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Flowable,
    Frame,
    KeepTogether,
    PageTemplate,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "public" / "consent.pdf"


class Rule(Flowable):
    def __init__(self, width, color=colors.HexColor("#6b7280"), thickness=0.75):
        super().__init__()
        self.width = width
        self.height = thickness
        self.color = color
        self.thickness = thickness

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, 0, self.width, 0)


class Checkbox(Flowable):
    def __init__(self, size=12):
        super().__init__()
        self.width = size
        self.height = size
        self.size = size

    def draw(self):
        self.canv.setStrokeColor(colors.HexColor("#111827"))
        self.canv.setLineWidth(1)
        self.canv.rect(0, 0, self.size, self.size, stroke=1, fill=0)


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#d1d5db"))
    canvas.setLineWidth(0.5)
    canvas.line(doc.leftMargin, 0.62 * inch, letter[0] - doc.rightMargin, 0.62 * inch)
    canvas.setFont("Helvetica", 8.5)
    canvas.setFillColor(colors.HexColor("#4b5563"))
    canvas.drawString(doc.leftMargin, 0.42 * inch, "For Bard College internal laboratory use only.")
    canvas.restoreState()


def field_row(label, width=3.2 * inch):
    return [
        Paragraph(label, STYLES["field_label"]),
        Rule(width, colors.HexColor("#111827"), 0.75),
    ]


def build_pdf():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=letter,
        rightMargin=0.68 * inch,
        leftMargin=0.68 * inch,
        topMargin=0.62 * inch,
        bottomMargin=0.86 * inch,
        title="Bard College RKC Monitor SMS Alert Consent Form",
        author="Bard College",
        subject="RKC Monitor SMS Alert Program Consent",
    )

    frame = Frame(
        doc.leftMargin,
        doc.bottomMargin,
        doc.width,
        doc.height,
        id="normal",
        showBoundary=0,
    )
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=footer)])

    story = []
    story.append(Paragraph("Bard College", STYLES["form_institution"]))
    story.append(Paragraph("Bard College RKC Monitor SMS Alert Consent Form", STYLES["form_title"]))
    story.append(Spacer(1, 0.12 * inch))
    story.append(Rule(doc.width, colors.HexColor("#1f2937"), 1.1))
    story.append(Spacer(1, 0.18 * inch))

    story.append(
        Paragraph(
            "The RKC Monitor SMS alert system sends operational text alerts related to laboratory "
            "monitoring conditions, equipment status, and other system events that may require "
            "attention from authorized personnel.",
            STYLES["form_body"],
        )
    )
    story.append(Spacer(1, 0.14 * inch))

    section_rows = [
        [
            Paragraph("Program Consent Terms", STYLES["form_section"]),
        ],
        [
            Paragraph(
                "Enrollment is voluntary and limited to authorized laboratory personnel.",
                STYLES["form_bullet"],
            )
        ],
        [
            Paragraph(
                "Message frequency varies based on system conditions.",
                STYLES["form_bullet"],
            )
        ],
        [
            Paragraph("Message and data rates may apply.", STYLES["form_bullet"]),
        ],
        [
            Paragraph("Reply HELP for help. Reply STOP to opt out.", STYLES["form_bullet"]),
        ],
        [
            Paragraph(
                "Mobile numbers and SMS consent are not shared with third parties or affiliates "
                "for marketing or promotional purposes.",
                STYLES["form_bullet"],
            )
        ],
    ]

    terms_table = Table(section_rows, colWidths=[doc.width])
    terms_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f3f4f6")),
                ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#9ca3af")),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#d1d5db")),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(terms_table)
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("Acknowledgment and Contact Information", STYLES["form_section"]))
    story.append(Spacer(1, 0.13 * inch))

    fields = [
        [field_row("Employee Name"), field_row("Department / Role")],
        [field_row("Mobile Number"), field_row("Date")],
    ]
    field_table = Table(fields, colWidths=[doc.width / 2, doc.width / 2], rowHeights=[0.58 * inch, 0.58 * inch])
    field_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 18),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(field_table)
    story.append(Spacer(1, 0.08 * inch))

    consent_table = Table(
        [
            [
                Checkbox(12),
                Paragraph("I consent to receive RKC Monitor SMS alerts.", STYLES["form_body"]),
            ]
        ],
        colWidths=[0.28 * inch, doc.width - 0.28 * inch],
    )
    consent_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(consent_table)
    story.append(Spacer(1, 0.22 * inch))

    signature = Table(
        [[Paragraph("Signature", STYLES["field_label"]), Rule(4.75 * inch, colors.HexColor("#111827"), 0.75)]],
        colWidths=[1.0 * inch, 4.9 * inch],
    )
    signature.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(signature)
    story.append(Spacer(1, 0.22 * inch))

    story.append(
        KeepTogether(
            [
                Paragraph("Policy References", STYLES["form_section"]),
                Spacer(1, 0.08 * inch),
                Paragraph("Privacy Policy: https://bard-box.org/privacy", STYLES["form_body"]),
                Paragraph("Terms & Conditions: https://bard-box.org/terms", STYLES["form_body"]),
            ]
        )
    )

    doc.build(story)


STYLES = getSampleStyleSheet()
STYLES.add(
    ParagraphStyle(
        name="form_institution",
        parent=STYLES["Normal"],
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#374151"),
        spaceAfter=4,
    )
)
STYLES.add(
    ParagraphStyle(
        name="form_title",
        parent=STYLES["Title"],
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#111827"),
    )
)
STYLES.add(
    ParagraphStyle(
        name="form_section",
        parent=STYLES["Heading2"],
        alignment=TA_LEFT,
        fontName="Helvetica-Bold",
        fontSize=11.5,
        leading=14,
        textColor=colors.HexColor("#111827"),
        spaceAfter=2,
    )
)
STYLES.add(
    ParagraphStyle(
        name="form_body",
        parent=STYLES["BodyText"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=15,
        textColor=colors.HexColor("#1f2937"),
    )
)
STYLES.add(
    ParagraphStyle(
        name="form_bullet",
        parent=STYLES["form_body"],
        bulletText="-",
        leftIndent=12,
        firstLineIndent=-7,
    )
)
STYLES.add(
    ParagraphStyle(
        name="field_label",
        parent=STYLES["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor("#374151"),
        spaceAfter=7,
    )
)


if __name__ == "__main__":
    build_pdf()
