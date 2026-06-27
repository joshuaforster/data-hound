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


def generate_letter(lead, sender):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(25, 25, 25)
    pdf.set_auto_page_break(auto=True, margin=25)

    NL = {"new_x": "LMARGIN", "new_y": "NEXT"}

    # --- Sender block: top right (UK standard layout) ---
    pdf.set_font("Helvetica", style="B", size=10)
    pdf.cell(0, 5, sender["company_name"], align="R", **NL)
    pdf.set_font("Helvetica", size=10)
    for line in _parse_uk_address(sender["address"]):
        pdf.cell(0, 5, line, align="R", **NL)
    pdf.cell(0, 5, sender["phone"], align="R", **NL)
    pdf.cell(0, 5, sender["email"], align="R", **NL)
    pdf.cell(0, 5, sender["website"], align="R", **NL)

    # --- Date: right-aligned below sender (UK format: DD Month YYYY) ---
    pdf.ln(5)
    pdf.cell(0, 5, date.today().strftime("%d %B %Y"), align="R", **NL)

    # --- Recipient address: left-aligned, Royal Mail compliant ---
    # No blank lines between address lines; town in CAPS; postcode in CAPS on own line
    pdf.ln(10)
    for line in _parse_uk_address(lead["occupier_address"]):
        pdf.cell(0, 5, line, align="L", **NL)

    # --- Salutation ---
    # Occupier name is unknown, so "Dear Sir or Madam" requires "Yours faithfully" sign-off
    pdf.ln(10)
    pdf.multi_cell(0, 5, "Dear Sir or Madam,")

    # --- Subject line ---
    pdf.ln(5)
    pdf.set_font("Helvetica", style="B", size=10)
    pdf.multi_cell(0, 5, f"Re: Planning Application {lead['lead_id']}")

    # --- Body ---
    pdf.ln(5)
    pdf.set_font("Helvetica", size=10)
    pdf.multi_cell(0, 5,
        f"We are writing regarding the recent planning application submitted for "
        f"{lead['property_address']}, proposing: {lead['proposal']}."
    )
    pdf.ln(5)
    pdf.multi_cell(0, 5,
        "We would welcome the opportunity to discuss how we might assist with this project. "
        "Please do not hesitate to get in touch using the contact details above."
    )

    # --- Sign-off (matches "Dear Sir or Madam" salutation) ---
    pdf.ln(10)
    pdf.multi_cell(0, 5, "Yours faithfully,")
    pdf.ln(15)
    pdf.multi_cell(0, 5, sender.get("name"))

    return pdf


if __name__ == "__main__":
    from fake_data import fake_leads as leads, fake_user as sender

    pdf = generate_letter(leads[1], sender)
    pdf.output("test_letter.pdf")
    print("done, check test_letter.pdf")
