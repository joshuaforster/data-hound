import requests
import os
from dotenv import load_dotenv

load_dotenv()


def _format_address(address):
    parts = [
        address.get("address_line_1"),
        address.get("address_line_2"),
        address.get("locality"),
        address.get("region"),
        address.get("postal_code"),
    ]
    return ", ".join(p for p in parts if p)


def _to_lead(company):
    address = company.get("registered_office_address", {})
    return {
        "lead_id": company.get("company_number"),
        "company_name": company.get("company_name"),
        "applicant_name": company.get("company_name"),
        "occupier_address": _format_address(address),
        "property_address": _format_address(address),
        "postcode": address.get("postal_code"),
        "date_created": company.get("date_of_creation"),
        "sic_codes": company.get("sic_codes"),
        "source": "companies_house",
    }


def search_new_companies(sic_code, location, incorporated_from="2026-01-04"):
    api_key = os.getenv("COMPANIES_HOUSE_API_KEY")

    url = "https://api.company-information.service.gov.uk/advanced-search/companies"
    params = {
        "sic_codes": sic_code,
        "location": location,
        "incorporated_from": incorporated_from,
        "size": 100,
    }

    response = requests.get(url, params=params, auth=(api_key, ""))
    response.raise_for_status()
    data = response.json()

    leads = []
    for company in data.get("items", []):
        leads.append(_to_lead(company))
    return leads


def verify_company(company_name):
    api_key = os.getenv("COMPANIES_HOUSE_API_KEY")
    url = "https://api.company-information.service.gov.uk/search/companies"
    params = {"q": company_name, "items_per_page": 1}

    response = requests.get(url, params=params, auth=(api_key, ""))
    response.raise_for_status()
    items = response.json().get("items", [])

    if not items:
        return None

    match = items[0]
    address = match.get("address", {})
    return {
        "verified_name": match.get("title"),
        "company_number": match.get("company_number"),
        "company_status": match.get("company_status"),
        "verified_address": _format_address(address),
        "postcode": address.get("postal_code"),
    }


if __name__ == "__main__":
    leads = search_new_companies("43210", "Norwich")
    print(f"Found {len(leads)} companies")
    for lead in leads:
        print(lead["company_name"], lead["postcode"], lead["occupier_address"])