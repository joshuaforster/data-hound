import requests

CONTRACTS_FINDER_URL = "https://www.contractsfinder.service.gov.uk/Published/Notices/OCDS/Search"


def _get_regions(release):
    regions = set()
    items = release.get("tender", {}).get("items") or []
    for item in items:
        for addr in item.get("deliveryAddresses") or []:
            region = addr.get("region")
            if region:
                regions.add(region)
    return regions


def _in_target_region(regions, targets):
    for r in regions:
        for t in targets:
            if t.lower() in r.lower():
                return True
    return False


def _get_apply_link(release):
    documents = release.get("tender", {}).get("documents") or []
    for doc in documents:
        if doc.get("url"):
            return doc["url"]

    notice_id = release.get("id")
    if notice_id:
        return f"https://www.contractsfinder.service.gov.uk/Notice/{notice_id}"

    return None


def _get_winner(release):
    parties = release.get("parties") or []
    for p in parties:
        if "supplier" in (p.get("roles") or []):
            return p.get("name")
    return None


def extract_leads(releases, target_regions=None):
    leads = []

    for release in releases:
        regions = _get_regions(release)

        if target_regions and not _in_target_region(regions, target_regions):
            continue

        tender = release.get("tender", {})
        tender_period = tender.get("tenderPeriod") or {}

        leads.append({
            "title": tender.get("title"),
            "description": tender.get("description"),
            "buyer": release.get("buyer", {}).get("name"),
            "value": tender.get("value", {}).get("amount"),
            "regions": ", ".join(regions) if regions else None,
            "status": tender.get("status"),
            "closing_date": tender_period.get("endDate"),
            "apply_link": _get_apply_link(release),
        })

    return leads


def fetch_open_construction_tenders(published_from="2026-04-01", target_regions=None):
    url = CONTRACTS_FINDER_URL
    params = {
        "publishedFrom": published_from,
        "stages": "tender",
        "keyword": "construction refurbishment building",
        "limit": 100,
    }

    all_leads = []
    max_pages = 20

    try:
        for _ in range(max_pages):
            response = requests.get(
                url,
                params=params,
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()

            releases = data.get("releases", [])
            all_leads.extend(extract_leads(releases, target_regions))

            next_url = data.get("links", {}).get("next")
            if not next_url:
                break

            url = next_url
            params = None

        return all_leads
    except Exception as e:
        print(f"Error: {e}")
        return all_leads


def fetch_awarded_construction_contracts(published_from="2026-04-01", target_regions=None):
    url = CONTRACTS_FINDER_URL
    params = {
        "publishedFrom": published_from,
        "stages": "award",
        "keyword": "construction refurbishment building",
        "limit": 100,
    }

    all_leads = []
    max_pages = 20

    try:
        for _ in range(max_pages):
            response = requests.get(
                url,
                params=params,
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()

            for release in data.get("releases", []):
                regions = _get_regions(release)
                if target_regions and not _in_target_region(regions, target_regions):
                    continue

                tender = release.get("tender", {})
                awards = release.get("awards") or []
                award = awards[0] if awards else {}

                all_leads.append({
                    "company_name": _get_winner(release),
                    "contract_title": tender.get("title"),
                    "awarded_by": release.get("buyer", {}).get("name"),
                    "contract_value": award.get("value", {}).get("amount"),
                    "regions": ", ".join(regions) if regions else None,
                })

            next_url = data.get("links", {}).get("next")
            if not next_url:
                break

            url = next_url
            params = None

        return all_leads
    except Exception as e:
        print(f"Error: {e}")
        return all_leads


if __name__ == "__main__":
    leads = fetch_open_construction_tenders()
    print(f"Found {len(leads)} open tenders")
    for lead in leads:
        print(lead)