import re
from datetime import date
from fpdf import FPDF

# Matches standard UK postcodes (AN NAA, ANN NAA, AAN NAA, AANN NAA, etc.)
_UK_POSTCODE_RE = re.compile(
    r"^([A-PR-UWYZ][A-HK-Y0-9][A-HJKPSTUW0-9]?[ABEHMNPRVWXY0-9]?)\s*([0-9][ABD-HJLNP-UW-Z]{2})$",
    re.IGNORECASE,
)


def _parse_uk_address(raw):
    """
    Split a comma-separated UK address string into Royal Mail-compliant lines.
    Town is uppercased; postcode is uppercased and placed on its own final line.
    No blank lines are inserted between parts (Pingen/Royal Mail requirement).
    """
    parts = [p.strip() for p in raw.split(",") if p.strip()]

    postcode = None
    town = None
    street_lines = []

    for part in reversed(parts):
        m = _UK_POSTCODE_RE.match(part)
        if postcode is None and m:
            postcode = f"{m.group(1).upper()} {m.group(2).upper()}"
        elif town is None and postcode is not None:
            town = part.upper()
        else:
            street_lines.insert(0, part)

    lines = street_lines
    if town:
        lines = lines + [town]
    if postcode:
        lines = lines + [postcode]

    return lines

def generate_letter(lead, sender, letter):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(20, 15, 20)
    pdf.set_auto_page_break(auto=True, margin=25)

    NL = {"new_x": "LMARGIN", "new_y": "NEXT"}

    recipient_type = letter.get("recipient_type", "occupier")

    # --- Sender block: top right (UK standard layout) ---
    pdf.set_y(15)
    pdf.set_font("Helvetica", style="B", size=10)
    pdf.cell(0, 5, sender["company_name"], align="R", **NL)
    pdf.set_font("Helvetica", size=10)
    for line in _parse_uk_address(sender["address"]):
        pdf.cell(0, 5, line, align="R", **NL)
    pdf.cell(0, 5, sender["phone"], align="R", **NL)
    pdf.cell(0, 5, sender["email"], align="R", **NL)
    pdf.cell(0, 5, sender["website"], align="R", **NL)

    # --- Date: right-aligned below sender ---
    pdf.ln(5)
    pdf.cell(0, 5, date.today().strftime("%d %B %Y"), align="R", **NL)

    # --- Work out the recipient based on the letter type ---
    if recipient_type == "agent":
        recipient_name = lead.get("agent_name", "").strip()
        recipient_address = lead.get("agent_company_address", "")
        company = lead.get("agent_company_name", "").strip()
    else:
        recipient_name = lead.get("applicant_name", "").strip()
        recipient_address = lead.get("occupier_address", "")
        company = ""

    # --- Recipient address: Pingen left window (X=22mm, Y=60mm) ---
    pdf.set_font("Helvetica", size=10)
    pdf.set_xy(22, 60)
    name_line = recipient_name if recipient_name else "The Occupier"
    pdf.set_x(22)
    pdf.cell(85.5, 5, name_line, align="L", new_x="LMARGIN", new_y="NEXT")
    if company:
        pdf.set_x(22)
        pdf.cell(85.5, 5, company, align="L", new_x="LMARGIN", new_y="NEXT")
    for line in _parse_uk_address(recipient_address):
        pdf.set_x(22)
        pdf.cell(85.5, 5, line, align="L", new_x="LMARGIN", new_y="NEXT")

    # --- Salutation ---
    pdf.set_x(20)
    pdf.ln(12)
    salutation = f"Dear {recipient_name}," if recipient_name else "Dear Sir or Madam,"
    pdf.multi_cell(0, 5, salutation)

    # --- Subject line (from the letter) ---
    pdf.ln(5)
    pdf.set_font("Helvetica", style="B", size=10)
    pdf.multi_cell(0, 5, letter["subject"])

    # --- Body (from the letter) ---
    pdf.ln(5)
    pdf.set_font("Helvetica", size=10)
    paragraphs = letter["body"].split("\n\n")
    for i, para in enumerate(paragraphs):
        pdf.multi_cell(0, 5, para.strip())
        if i < len(paragraphs) - 1:
            pdf.ln(4)

    # --- Sign-off ---
    pdf.ln(10)
    sign_off = "Yours sincerely," if recipient_name else "Yours faithfully,"
    pdf.multi_cell(0, 5, sign_off)
    pdf.ln(15)
    pdf.multi_cell(0, 5, sender.get("name"))

    return pdf