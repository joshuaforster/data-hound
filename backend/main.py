from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fake_data import fake_leads as leads
from fake_data import fake_users as users
from fake_data import fake_contract_leads as contract_leads
from gov_contracts import fetch_open_construction_tenders, fetch_awarded_construction_contracts
from generate_letter import generate_letter
from utils import get_lead, get_user, get_template, fill_template, get_contract_lead
from pingen import post_letter, create_letter
from streetview import get_latlon, street_view_link
from epc import get_epc_for_council, get_epc_for_postcode
from companies_house import search_new_companies, verify_company

import io

app = FastAPI()


# ============================================================
#  LEADS
#  Specific routes first, then the /{lead_id} wildcard last.
# ============================================================

@app.get("/leads/")
def get_leads():
    return leads


@app.get("/leads/tenders")
def get_tender_leads(published_from: str = "2026-04-01", region: str = None):
    target_regions = {region} if region else None
    results = fetch_open_construction_tenders(published_from, target_regions)
    return {"source": "tenders", "count": len(results), "leads": results}


@app.get("/leads/companies")
def get_company_leads(sic_code: str, location: str):
    results = search_new_companies(sic_code, location)
    return {"source": "companies", "count": len(results), "leads": results}


@app.get("/leads/contracts")
def get_contract_leads(published_from: str = "2026-04-01", region: str = None):
    try:
        target_regions = {region} if region else None
        awards = fetch_awarded_construction_contracts(published_from, target_regions)

        leads = []
        for award in awards[:20]:
            name = award.get("company_name")
            if not name:
                continue

            verified = verify_company(name)
            if not verified:
                continue

            if verified["company_status"] != "active":
                continue

            leads.append({
                "lead_id": verified["company_number"],
                "source": "contract",
                "recipient_type": "occupier",
                "applicant_name": verified["verified_name"],
                "occupier_address": verified["verified_address"],
                "property_address": verified["verified_address"],
                "postcode": verified["postcode"],
                "company_number": verified["company_number"],
                "company_status": verified["company_status"],
                "contract_title": award.get("contract_title"),
                "awarded_by": award.get("awarded_by"),
                "contract_value": award.get("contract_value"),
            })

        return {"count": len(leads), "leads": leads}
    except Exception as e:
        return {"error": str(e)}


@app.get("/leads/fake-contracts/{lead_id}")
def get_fake_contract_lead(lead_id: str):
    contract_lead = get_contract_lead(lead_id)
    return {"source": "contract", "contract_lead": contract_lead}


# wildcard LAST so it doesn't swallow the routes above
@app.get("/leads/{lead_id}")
def get_leads_by_id(lead_id: str):
    lead = get_lead(lead_id)
    return lead


# ============================================================
#  LETTERS  (preview + send)
# ============================================================

@app.get("/leads/{lead_id}/preview/{user_id}/{template_id}")
def preview_letter(lead_id: str, user_id: str, template_id: str):
    lead = get_lead(lead_id)
    sender = get_user(user_id)
    template = get_template(template_id)

    subject, body = fill_template(template, lead)
    letter = {
        "recipient_type": template["recipient_type"],
        "subject": subject,
        "body": body,
    }

    pdf = generate_letter(lead, sender, letter)
    return StreamingResponse(
        io.BytesIO(pdf.output()),
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=preview.pdf"},
    )


@app.get("/contract_leads/{lead_id}/preview/{user_id}/{template_id}")
def preview_contract_letter(lead_id: str, user_id: str, template_id: str):
    lead = get_contract_lead(lead_id)
    sender = get_user(user_id)
    template = get_template(template_id)

    subject, body = fill_template(template, lead)
    letter = {
        "recipient_type": template["recipient_type"],
        "subject": subject,
        "body": body,
    }

    pdf = generate_letter(lead, sender, letter)
    return StreamingResponse(
        io.BytesIO(pdf.output()),
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=preview.pdf"},
    )


@app.post("/leads/{lead_id}/send/{user_id}/{template_id}")
def send_letter(lead_id: str, user_id: str, template_id: str):
    lead = get_lead(lead_id)
    sender = get_user(user_id)
    template = get_template(template_id)

    subject, body = fill_template(template, lead)
    letter = {
        "recipient_type": template["recipient_type"],
        "subject": subject,
        "body": body,
    }

    pdf = generate_letter(lead, sender, letter)
    letter_content = pdf.output()

    letter_id = create_letter(lead, letter_content)["data"]["id"]
    result = post_letter(letter_id)
    return result


@app.post("/webhooks/pingen")
async def pingen_webhook(request: Request):
    payload = await request.json()
    print("Pingen knocked", payload)
    return payload


# ============================================================
#  PROPERTY DATA  (street view, coords, EPC)
# ============================================================

@app.post("/streetview/{postcode}")
def submit_postcode(postcode: str):
    latitude, longitude = get_latlon(postcode)
    return street_view_link(latitude, longitude)


@app.post("/cords/{postcode}")
def get_cordinates(postcode: str):
    latitude, longitude = get_latlon(postcode)
    return latitude, longitude


@app.get("/address/{postcode}/{housenumber}")
def find_address(postcode: str, housenumber: str):
    results = get_epc_for_postcode(postcode, housenumber)
    if not results:
        return {"error": "No EPC found for that address"}

    addresses = [f"{r['address']}, {r['postcode']}" for r in results]
    return addresses[0]


@app.get("/epc/{postcode}/{housenumber}")
def get_epc(postcode: str, housenumber: str):
    results = get_epc_for_postcode(postcode, housenumber)
    if not results:
        return {"error": "No EPC found for that address"}

    return [r["energy_rating"] for r in results]


# ============================================================
#  USER SETTINGS
# ============================================================

@app.get("/settings/{user_id}")
def get_user_settings(user_id: str):
    for u in users:
        if u["user_id"] == user_id:
            return {
                "name": u["name"],
                "company_name": u["company_name"],
                "phone": u["phone"],
                "website": u["website"],
                "logo": u["logo_path"],
            }


@app.patch("/settings/{user_id}")
def update_user_settings(user_id: str, changes: dict):
    found_user = None
    for u in users:
        if u["user_id"] == user_id:
            found_user = u
    if found_user is None:
        return {"error": "User not found"}

    if "name" in changes:
        found_user["name"] = changes["name"]
    if "company_name" in changes:
        found_user["company_name"] = changes["company_name"]
    if "phone" in changes:
        found_user["phone"] = changes["phone"]
    if "website" in changes:
        found_user["website"] = changes["website"]

    return found_user