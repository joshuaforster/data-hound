from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
import pdfplumber
import requests
import io
import re
from repository import insert_leads

COUNCILS = [
    # Derbyshire
    {
        "base_url": "https://publicaccess.chesterfield.gov.uk",
        "main_url": "https://publicaccess.chesterfield.gov.uk/online-applications/search.do?action=weeklyList",
    },
    {
        "base_url": "https://eplanning.derby.gov.uk",
        "main_url": "https://eplanning.derby.gov.uk/online-applications/search.do?action=weeklyList",
    },
    # Leicestershire
    {
        "base_url": "https://pa.blaby.gov.uk",
        "main_url": "https://pa.blaby.gov.uk/online-applications/search.do?action=weeklyList",
    },
    {
        "base_url": "https://pa2.harborough.gov.uk",
        "main_url": "https://pa2.harborough.gov.uk/online-applications/search.do?action=weeklyList",
    },
    {
        "base_url": "https://pa.hinckley-bosworth.gov.uk",
        "main_url": "https://pa.hinckley-bosworth.gov.uk/online-applications/search.do?action=weeklyList",
    },
    {
        "base_url": "https://plans.nwleics.gov.uk",
        "main_url": "https://plans.nwleics.gov.uk/public-access/search.do?action=weeklyList",
    },
    {
        "base_url": "https://pa.oadby-wigston.gov.uk",
        "main_url": "https://pa.oadby-wigston.gov.uk/online-applications/search.do?action=weeklyList",
    },
    {
        "base_url": "https://publicaccess.rutland.gov.uk",
        "main_url": "https://publicaccess.rutland.gov.uk/online-applications/search.do?action=weeklyList",
    },
    # Lincolnshire
    {
        "base_url": "https://planning.lincoln.gov.uk",
        "main_url": "https://planning.lincoln.gov.uk/online-applications/search.do?action=weeklyList",
    },
    {
        "base_url": "https://planningonline.n-kesteven.gov.uk",
        "main_url": "https://planningonline.n-kesteven.gov.uk/online-applications/search.do?action=weeklyList",
    },
    # Nottinghamshire
    {
        "base_url": "https://publicaccess.bassetlaw.gov.uk",
        "main_url": "https://publicaccess.bassetlaw.gov.uk/online-applications/search.do?action=weeklyList",
    },
    {
        "base_url": "https://pawam.gedling.gov.uk",
        "main_url": "https://pawam.gedling.gov.uk/online-applications/search.do?action=weeklyList",
    },
    {
        "base_url": "https://planning.mansfield.gov.uk",
        "main_url": "https://planning.mansfield.gov.uk/online-applications/search.do?action=weeklyList",
    },
    {
        "base_url": "https://publicaccess.newark-sherwooddc.gov.uk",
        "main_url": "https://publicaccess.newark-sherwooddc.gov.uk/online-applications/search.do?action=weeklyList",
    },
    {
        "base_url": "https://publicaccess.nottinghamcity.gov.uk",
        "main_url": "https://publicaccess.nottinghamcity.gov.uk/online-applications/search.do?action=weeklyList",
    },
    {
        "base_url": "https://planningon-line.rushcliffe.gov.uk",
        "main_url": "https://planningon-line.rushcliffe.gov.uk/online-applications/search.do?action=weeklyList",
    },
    # Northamptonshire
    {
        "base_url": "https://publicaccess.northnorthants.gov.uk",
        "main_url": "https://publicaccess.northnorthants.gov.uk/online-applications/search.do?action=weeklyList",
    },
]


# ---------------------------------------------------------------------------
# STANDARD IDOX PORTAL SCRAPER
# ---------------------------------------------------------------------------

def parse_table(locator):
    rows = locator.locator("tr")
    result = {}
    for i in range(rows.count()):
        row = rows.nth(i)
        key = row.locator("th").inner_text().strip()
        value = row.locator("td").inner_text().strip()
        if key:
            result[key] = value
    return result


def scrape_council(page, base_url, main_url):
    page.goto(main_url)

    council = page.locator("#footercontent").inner_text().split("\n")[0]

    page.get_by_role("button", name="Search").click()
    page.locator("#resultsPerPage").select_option("100")
    page.get_by_role("button", name="Go").click()
    page.wait_for_selector("ul#searchresults li.searchresult")

    links = page.locator("ul#searchresults li.searchresult a")
    urls = [
        f"{base_url}{links.nth(i).get_attribute('href')}"
        for i in range(links.count())
        if links.nth(i).get_attribute("href")
    ]

    results = []

    for url in urls:
        page.goto(url)
        page.wait_for_selector("table#simpleDetailsTable")

        summary = parse_table(page.locator("table#simpleDetailsTable"))
        if "Application Received Date" in summary:
            summary["Application Received"] = summary.pop("Application Received Date")

        page.locator("a#subtab_details").click()
        page.wait_for_selector("a#subtab_details.active")
        further = parse_table(page.locator("table#applicationDetails"))

        page.locator("a#subtab_dates").click()
        page.wait_for_selector("a#subtab_dates.active")
        dates = parse_table(page.locator("table#simpleDetailsTable"))

        eia_raw = further.get("Environmental Assessment Requested", "")

        results.append({
            "council": council,
            "url": url,
            "council_reference": summary.get("Reference"),
            "property_address": summary.get("Address"),
            "occupier_address": summary.get("Address"),
            "proposal": summary.get("Proposal"),
            "status": summary.get("Status"),
            "application_type": further.get("Application Type"),
            "parish": further.get("Parish"),
            "ward": further.get("Ward"),
            "applicant_name": further.get("Applicant Name"),
            "agent_name": further.get("Agent Name"),
            "agent_company_name": further.get("Agent Company Name"),
            "agent_company_address": further.get("Agent Address"),
            "eia_required": eia_raw.lower() == "yes" if eia_raw else False,
            "received_date": summary.get("Application Received"),
            "validation_date": summary.get("Application Validated"),
            "determination_deadline": dates.get("Determination Deadline"),
        })

    return results


# ---------------------------------------------------------------------------
# ASHFIELD DISTRICT COUNCIL (Civica portal)
# ---------------------------------------------------------------------------

ASHFIELD_BASE_URL = "https://planning.ashfield.gov.uk"
ASHFIELD_SEARCH_URL = f"{ASHFIELD_BASE_URL}/planning-applications/search-applications/"


def _parse_agent_from_pdf(pdf_bytes):
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            text = ""
            for pdf_page in pdf.pages:
                text += pdf_page.extract_text() or ""

        def extract_field(label, source):
            match = re.search(rf'{re.escape(label)}\s*\n([^\n]+)', source)
            return match.group(1).strip() if match else ""

        agent_section = ""
        if "Agent Details" in text:
            agent_section = text.split("Agent Details")[-1]

        company = extract_field("Company Name", agent_section)
        title = extract_field("Title", agent_section)
        first = extract_field("First name", agent_section)
        surname = extract_field("Surname", agent_section)
        addr1 = extract_field("Address line 1", agent_section)
        addr2 = extract_field("Address line 2", agent_section)
        town = extract_field("Town/City", agent_section)
        county = extract_field("County", agent_section)
        postcode = extract_field("Postcode", agent_section)

        if company:
            agent_name = company
        elif first or surname:
            agent_name = f"{title} {first} {surname}".strip()
        else:
            agent_name = ""

        address_parts = [p for p in [addr1, addr2, town, county] if p]
        agent_address = "\n".join(address_parts)

        return agent_name, agent_address, postcode

    except Exception as e:
        print(f"PDF parse error: {e}")
        return "", "", ""


def _scrape_ashfield_application(page, key_no):
    url = f"{ASHFIELD_SEARCH_URL}#VIEW?RefType=GFPlanning&KeyNo={key_no}&KeyText=Subject"
    page.goto(url)
    page.wait_for_selector(".civicamainheader", timeout=10000)
    page.wait_for_timeout(500)

    def get_field(css_class):
        locator = page.locator(f".civica-keyobject-fulldetails .civicadetailtext.{css_class}")
        if locator.count() > 0:
            return locator.first.inner_text().strip()
        locator = page.locator(f".civicadetailtext.{css_class}")
        if locator.count() > 0:
            return locator.first.inner_text().strip()
        return ""

    reference_raw = get_field("civica-gfplanning-internetdesc")
    reference = reference_raw.split(" - ")[0].strip() if reference_raw else ""
    address = get_field("civica-gfplanning-applicationaddress")
    proposal = get_field("civica-gfplanning-proposal")
    applicant_name = get_field("civica-gfplanning-stext1")
    decision_due = get_field("civica-gfplanning-sdate2")
    date_valid = get_field("civica-gfplanning-sdate1")
    agent_name_page = get_field("civica-gfplanning-stext3")

    docs_header = page.locator(".civicaaccordionheader").filter(has_text="Documents")
    if docs_header.count() > 0:
        docs_header.first.click()
        page.wait_for_timeout(1000)

    agent_name, agent_address, agent_postcode = "", "", ""
    doc_links = page.locator(".civica-doclistitem a")
    for i in range(doc_links.count()):
        title = doc_links.nth(i).inner_text().strip()
        if "Application Form" in title:
            href = doc_links.nth(i).get_attribute("href") or ""
            doc_no_match = re.search(r'DocNo=(\d+)', href)
            if doc_no_match:
                doc_no = doc_no_match.group(1)
                pdf_url = f"{ASHFIELD_BASE_URL}/civica/Resource/Civica/Handler.ashx/Doc/pagestream?cd=inline&pdf=true&docno={doc_no}"
                try:
                    response = requests.get(pdf_url, timeout=15)
                    if response.status_code == 200:
                        agent_name, agent_address, agent_postcode = _parse_agent_from_pdf(response.content)
                except Exception as e:
                    print(f"PDF download error: {e}")
            break

    if not agent_name:
        agent_name = agent_name_page

    return {
        "council": "Ashfield District Council",
        "url": url,
        "council_reference": reference,
        "property_address": address,
        "occupier_address": address,
        "proposal": proposal,
        "status": "",
        "application_type": "",
        "parish": "",
        "ward": "",
        "applicant_name": applicant_name,
        "agent_name": agent_name,
        "agent_company_name": "",
        "agent_company_address": agent_address,
        "agent_postcode": agent_postcode or None,
        "eia_required": False,
        "received_date": date_valid,
        "validation_date": date_valid,
        "determination_deadline": decision_due,
    }


def gather_ashfield_results(page):
    today = datetime.today()
    week_ago = today - timedelta(days=7)
    date_from = week_ago.strftime("%d/%m/%Y")
    date_to = today.strftime("%d/%m/%Y")

    page.goto(ASHFIELD_SEARCH_URL)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    page.get_by_label("Valid Date (From)").click()
    page.keyboard.type(date_from)
    page.get_by_label("Valid Date (To)").click()
    page.keyboard.type(date_to)
    page.wait_for_timeout(500)
    page.locator("button.advancedsearchbutton").click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    key_nos = []
    while True:
        links = page.locator("a.civica-gfplanning-internetdesc")
        for i in range(links.count()):
            href = links.nth(i).get_attribute("href") or ""
            match = re.search(r'KeyNo=(\d+)', href)
            if match:
                key_nos.append(match.group(1))

        next_btn = page.locator(".civicapager .btn").filter(has_text="Next")
        if next_btn.count() > 0 and "disabled-btn" not in (next_btn.get_attribute("class") or ""):
            next_btn.click()
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1500)
        else:
            break

    print(f"Ashfield: found {len(key_nos)} applications")
    results = []
    for key_no in key_nos:
        try:
            results.append(_scrape_ashfield_application(page, key_no))
        except Exception as e:
            print(f"  -> Ashfield KeyNo {key_no} failed: {e}")
    return results


# ---------------------------------------------------------------------------
# WEST NORTHAMPTONSHIRE COUNCIL (planning-register.co.uk portal)
# ---------------------------------------------------------------------------

WNC_BASE_URL = "https://wnc.planning-register.co.uk"


def gather_west_northamptonshire_results(page):
    page.goto(f"{WNC_BASE_URL}/WeeklyList")
    page.wait_for_load_state("networkidle")

    page.locator("a").filter(has_text="Applications Registered Valid During Period").first.click()
    page.wait_for_load_state("networkidle")

    page.locator("#resultsPerPage").select_option("50")
    page.wait_for_load_state("networkidle")

    urls = []
    while True:
        links = page.locator("td a[href*='/Planning/Display/']")
        for i in range(links.count()):
            href = links.nth(i).get_attribute("href")
            if href:
                full_url = f"{WNC_BASE_URL}{href}" if href.startswith("/") else href
                if full_url not in urls:
                    urls.append(full_url)

        next_link = page.locator("a").filter(has_text="Next")
        if next_link.count() > 0:
            next_link.first.click()
            page.wait_for_load_state("networkidle")
        else:
            break

    print(f"West Northamptonshire: found {len(urls)} applications")
    results = []

    for url in urls:
        try:
            page.goto(url)
            page.wait_for_selector(".summaryTbl", timeout=10000)

            main_tab = page.locator(".tab-button").filter(has_text="Main Details")
            if main_tab.count() > 0:
                main_tab.first.click()
                page.wait_for_timeout(500)

            def get_cell(label):
                rows = page.locator(".summaryTbl td")
                for i in range(rows.count()):
                    text = rows.nth(i).inner_text()
                    if label in text:
                        span = rows.nth(i).locator("span")
                        if span.count() > 0:
                            return span.first.inner_text().strip()
                return ""

            reference = get_cell("Application Number")
            app_type = get_cell("Application Type")
            status = get_cell("Status")
            location = get_cell("Location")
            proposal = get_cell("Proposal")
            received_date = get_cell("Received Date")
            valid_date = get_cell("Valid Date")
            target_date = get_cell("Target Decision Date")

            agents_tab = page.locator(".tab-button").filter(has_text="Applicant")
            if agents_tab.count() > 0:
                agents_tab.first.click()
                page.wait_for_timeout(500)

            def get_tab_cell(label):
                cells = page.locator("#Applicant\\/ Agents td, #Applicant\\/\\ Agents td")
                for i in range(cells.count()):
                    text = cells.nth(i).inner_text()
                    if label in text:
                        span = cells.nth(i).locator("span")
                        if span.count() > 0:
                            return span.first.inner_text().strip()
                return ""

            applicant_name = get_tab_cell("Applicant")
            agent_name = get_tab_cell("Agent")
            agent_address_raw = get_tab_cell("Agents's Address")

            agent_address = ""
            agent_postcode = None
            if agent_address_raw:
                lines = [l.strip() for l in agent_address_raw.split("\n") if l.strip()]
                postcode_match = re.search(r'[A-Z]{1,2}\d{1,2}[A-Z]?\s*\d[A-Z]{2}', agent_address_raw)
                if postcode_match:
                    agent_postcode = postcode_match.group(0)
                agent_address = "\n".join(lines)

            results.append({
                "council": "West Northamptonshire Council",
                "url": url,
                "council_reference": reference,
                "property_address": location,
                "occupier_address": location,
                "proposal": proposal,
                "status": status,
                "application_type": app_type,
                "parish": "",
                "ward": "",
                "applicant_name": applicant_name,
                "agent_name": agent_name,
                "agent_company_name": "",
                "agent_company_address": agent_address,
                "agent_postcode": agent_postcode,
                "eia_required": False,
                "received_date": received_date or valid_date,
                "validation_date": valid_date,
                "determination_deadline": target_date,
            })

        except Exception as e:
            print(f"  -> West Northants {url} failed: {e}")
            continue

    return results


# ---------------------------------------------------------------------------
# MAIN ENTRY POINT
# ---------------------------------------------------------------------------

def _insert_and_report(results, label):
    inserted = insert_leads(results)
    print(f"  -> {len(results)} scraped, {inserted} inserted ({len(results) - inserted} duplicates skipped) [{label}]")


def gather_all_results():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        for council in COUNCILS:
            print(f"Scraping {council['base_url']} ...")
            try:
                results = scrape_council(page, council["base_url"], council["main_url"])
                _insert_and_report(results, council["base_url"])
            except Exception as e:
                print(f"  -> failed: {e}")

        print("Scraping Ashfield District Council ...")
        try:
            results = gather_ashfield_results(page)
            _insert_and_report(results, "Ashfield")
        except Exception as e:
            print(f"  -> Ashfield failed: {e}")

        print("Scraping West Northamptonshire Council ...")
        try:
            results = gather_west_northamptonshire_results(page)
            _insert_and_report(results, "West Northamptonshire")
        except Exception as e:
            print(f"  -> West Northants failed: {e}")

        browser.close()


if __name__ == "__main__":
    gather_all_results()
