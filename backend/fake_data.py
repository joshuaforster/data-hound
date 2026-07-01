fake_users = [
    {
        "user_id": "c72f3b1a-9d4e-4f8a-b3c2-1a2b3c4d5e6f",
        "name": "Daniel Harper",
        "company_name": "Harper Property Solutions",
        "address": "12 Exchange Street, Norwich, NR2 1AT",
        "phone": "01603 556 789",
        "email": "daniel@harperpropertysolutions.co.uk",
        "website": "www.harperpropertysolutions.co.uk",
        "logo_path": "assets/logo.png",
        "sign_off": "Daniel Harper, Director",
    },
    {
        "user_id": "b84e2c3d-1a5f-4e9b-c6d7-2b3c4d5e6f7a",
        "name": "Sophie Brennan",
        "company_name": "Brennan Build & Renovate",
        "address": "7 Castle Meadow, Norwich, NR1 3DH",
        "phone": "01603 224 410",
        "email": "sophie@brennanbuild.co.uk",
        "website": "www.brennanbuild.co.uk",
        "logo_path": "assets/logo.png",
        "sign_off": "Sophie Brennan, Managing Director",
    },
    {
        "user_id": "d93f1a2b-4c6e-4d8f-a1b2-3c4d5e6f7a8b",
        "name": "Marcus Webb",
        "company_name": "Webb Extensions Ltd",
        "address": "34 Ber Street, Norwich, NR1 3EJ",
        "phone": "01603 771 852",
        "email": "marcus@webbextensions.co.uk",
        "website": "www.webbextensions.co.uk",
        "logo_path": "assets/logo.png",
        "sign_off": "Marcus Webb, Director",
    },
]

fake_leads = [
    {
        "lead_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
        "council_reference": "2026/0413/F",
        "property_address": "14 Earlham Road, Norwich, NR2 3DB",
        "occupier_address": "14 Earlham Road, Norwich, NR2 3DB",
        "proposal": "Single storey rear extension and loft conversion",
        "status": "Pending Consideration",
        "application_type": "Full Application",
        "parish": "Norwich",
        "ward": "Town Close",
        "applicant_name": "Mr James Holloway",
        "agent_name": "Sarah Bennett",
        "agent_company_name": "Bennett Architectural Design",
        "agent_company_address": "3 Upper King Street, Norwich, NR3 1RB",
        "eia_required": False,
        "received_date": "2026-05-12",
        "validation_date": "2026-05-15",
        "determination_deadline": "2026-07-10",
    },
    {
        "lead_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
        "council_reference": "2026/0418/HOU",
        "property_address": "27 Unthank Road, Norwich, NR2 2RW",
        "occupier_address": "27 Unthank Road, Norwich, NR2 2RW",
        "proposal": "Erection of detached garden room for use as home office",
        "status": "Approved",
        "application_type": "Householder Application",
        "parish": "Norwich",
        "ward": "Eaton",
        "applicant_name": "Mrs Priya Sharma",
        "agent_name": "Tom Wright",
        "agent_company_name": "Wright & Co Planning",
        "agent_company_address": "12 Prince of Wales Road, Norwich, NR1 1BG",
        "eia_required": False,
        "received_date": "2026-04-28",
        "validation_date": "2026-05-02",
        "determination_deadline": "2026-06-27",
    },
    {
        "lead_id": "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
        "council_reference": "2026/0425/F",
        "property_address": "Land adjacent to 8 Dereham Road, Norwich, NR5 8QW",
        "occupier_address": "8 Dereham Road, Norwich, NR5 8QW",
        "proposal": "Construction of two semi-detached dwellings with associated parking",
        "status": "Pending Consideration",
        "application_type": "Full Application",
        "parish": "Costessey",
        "ward": "Wensum",
        "applicant_name": "Hartley Homes Ltd",
        "agent_name": "David Mitchell",
        "agent_company_name": "Mitchell Planning Consultants",
        "agent_company_address": "45 St Giles Street, Norwich, NR2 1JR",
        "eia_required": False,
        "received_date": "2026-05-01",
        "validation_date": "2026-05-06",
        "determination_deadline": "2026-08-01",
    },
    {
        "lead_id": "3f2504e0-4f89-41d3-9a0c-0305e82c3301",
        "council_reference": "2026/0431/LB",
        "property_address": "The Old Bakery, 2 Elm Hill, Norwich, NR3 1HN",
        "occupier_address": "The Old Bakery, 2 Elm Hill, Norwich, NR3 1HN",
        "proposal": "Internal alterations and replacement of windows to listed building",
        "status": "Withdrawn",
        "application_type": "Listed Building Consent",
        "parish": "Norwich",
        "ward": "Mancroft",
        "applicant_name": "Mr Oliver Grant",
        "agent_name": "Emma Foxley",
        "agent_company_name": "Heritage Build Consultancy",
        "agent_company_address": "7 Tombland, Norwich, NR3 1HF",
        "eia_required": False,
        "received_date": "2026-03-19",
        "validation_date": "2026-03-24",
        "determination_deadline": "2026-05-19",
    },
    {
        "lead_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
        "council_reference": "2026/0440/F",
        "property_address": "Unit 4, Hurricane Way, Norwich, NR6 6EY",
        "occupier_address": "Riverside Trading Estate, Norwich, NR1 1WS",
        "proposal": "Change of use from warehouse (B8) to gym (E)",
        "status": "Refused",
        "application_type": "Full Application",
        "parish": "Norwich",
        "ward": "Sewell",
        "applicant_name": "Norfolk Fitness Holdings Ltd",
        "agent_name": "Rachel Adeyemi",
        "agent_company_name": "Adeyemi Commercial Planning",
        "agent_company_address": "21 Bank Plain, Norwich, NR2 4SF",
        "eia_required": False,
        "received_date": "2026-04-10",
        "validation_date": "2026-04-14",
        "determination_deadline": "2026-06-09",
    },
]

fake_templates = [
    {
        "template_id": "occupier_intro",
        "recipient_type": "occupier",
        "source": "template",
        "subject": "Re: your planning application {council_reference}",
        "body": (
            "I noticed that a planning application ({council_reference}) was recently "
            "submitted for {property_address}, proposing {proposal}.\n\n"
            "I'm a local builder, and I work with homeowners on projects exactly like "
            "this one. I wanted to introduce myself early, before the diggers arrive, "
            "in case it's useful to have an experienced builder you can talk things "
            "through with.\n\n"
            "There's no obligation here at all. If you'd like an informal chat about the "
            "build, my details are at the top of this letter."
        ),
    },
    {
        "template_id": "occupier_local",
        "recipient_type": "occupier",
        "source": "template",
        "subject": "Re: your planning application {council_reference}",
        "body": (
            "I noticed that a planning application ({council_reference}) was recently "
            "submitted for {property_address}, proposing {proposal}.\n\n"
            "This kind of project is one of my favourites to work on, and I've completed "
            "a good few across {parish}, so I know what it takes to get it right.\n\n"
            "I'm a local builder, and I wanted to introduce myself early, before the "
            "work begins, in case it's useful to have an experienced pair of hands to "
            "talk it through with. No obligation at all. My details are at the top."
        ),
    },
    {
        "template_id": "occupier_developer",
        "recipient_type": "occupier",
        "source": "template",
        "subject": "Re: planning application {council_reference}",
        "body": (
            "I saw that you've applied for {proposal} at {property_address}.\n\n"
            "We specialise in projects exactly this size, where the applicant wants a "
            "reliable builder who can deliver to a consistent standard without the "
            "headache of managing several trades yourself.\n\n"
            "If you've not yet appointed a contractor, I'd value the chance to quote. "
            "Happy to share references from similar work we've completed locally."
        ),
    },
    {
        "template_id": "agent_intro",
        "recipient_type": "agent",
        "source": "template",
        "subject": "Re: planning application {council_reference}",
        "body": (
            "I saw that {agent_company_name} recently submitted planning application "
            "{council_reference} for {proposal} at {property_address}.\n\n"
            "I'm a local builder, and I work alongside agents and designers to deliver "
            "projects like this on the ground. I wanted to introduce myself in case "
            "you're ever looking for a reliable contractor to put in front of a "
            "client.\n\n"
            "I appreciate you'll have builders you already trust. If there's ever a gap, "
            "or a project that needs an extra pair of safe hands, I'd be glad to be on "
            "your list."
        ),
    },
    {
        "template_id": "occupier_change_of_use",
        "recipient_type": "occupier",
        "source": "template",
        "subject": "Re: change of use application {council_reference}",
        "body": (
            "I noticed your application for {proposal} at {property_address}.\n\n"
            "Projects like this live or die on getting the layout and the detail right "
            "for how the space will actually be used. It's a different job from a "
            "standard build, and it's one we've done before.\n\n"
            "If the scheme moves forward, I'd welcome the chance to talk it through with "
            "you. My details are above."
        ),
    },
    {
        "template_id": "contract_congrats",
        "recipient_type": "occupier",
        "source": "template",
        "subject": "Congratulations on your recent contract award",
        "body": (
            "I saw that {applicant_name} was recently awarded the contract for "
            "{contract_title} by {awarded_by}.\n\n"
            "Congratulations. Winning work like this often means ramping up quickly, "
            "and I wanted to introduce myself in case an extra reliable pair of hands "
            "on site would help you deliver it smoothly.\n\n"
            "No obligation at all. If it would be useful to have a local contractor you "
            "can call on, my details are at the top of this letter."
        ),
    },
    {
        "template_id": "contract_subcontract",
        "recipient_type": "occupier",
        "source": "template",
        "subject": "Subcontracting support for {contract_title}",
        "body": (
            "I noticed that {applicant_name} recently won the contract for "
            "{contract_title} with {awarded_by}.\n\n"
            "We work alongside main contractors on projects like this, taking on "
            "packages of work so you can hit your deadlines without stretching your own "
            "team too thin.\n\n"
            "If you're building out your supply chain for this one, I'd welcome a "
            "conversation. References from similar work available on request."
        ),
    },
]

fake_contract_leads = [
    {
        "lead_id": "e1c2a3b4-5d6f-4a7b-8c9d-1e2f3a4b5c6d",
        "source": "contract",
        "recipient_type": "occupier",
        "applicant_name": "Broadland Construction Ltd",
        "occupier_address": "12 Vulcan Road North, Norwich, NR6 6AQ",
        "property_address": "12 Vulcan Road North, Norwich, NR6 6AQ",
        "postcode": "NR6 6AQ",
        "company_number": "09112233",
        "company_status": "active",
        "contract_title": "Refurbishment of Community Sports Pavilion",
        "awarded_by": "Broadland District Council",
        "contract_value": 342000,
    },
    {
        "lead_id": "f2d3b4c5-6e7a-4b8c-9d0e-2f3a4b5c6d7e",
        "source": "contract",
        "recipient_type": "occupier",
        "applicant_name": "Fenland Building Services Limited",
        "occupier_address": "8 Hurricane Way, Norwich, NR6 6EY",
        "property_address": "8 Hurricane Way, Norwich, NR6 6EY",
        "postcode": "NR6 6EY",
        "company_number": "07445566",
        "company_status": "active",
        "contract_title": "School Roofing Replacement Programme",
        "awarded_by": "Norfolk County Council",
        "contract_value": 588400,
    },
    {
        "lead_id": "a3e4c5d6-7f8b-4c9d-0e1f-3a4b5c6d7e8f",
        "source": "contract",
        "recipient_type": "occupier",
        "applicant_name": "Wensum Groundworks Ltd",
        "occupier_address": "3 Barnard Road, Norwich, NR5 9JB",
        "property_address": "3 Barnard Road, Norwich, NR5 9JB",
        "postcode": "NR5 9JB",
        "company_number": "10998877",
        "company_status": "active",
        "contract_title": "Highways Drainage and Resurfacing Works",
        "awarded_by": "Norwich City Council",
        "contract_value": 214750,
    },
    {
        "lead_id": "b4f5d6e7-8a9c-4d0e-1f2a-4b5c6d7e8f9a",
        "source": "contract",
        "recipient_type": "occupier",
        "applicant_name": "Yare Valley Contractors Limited",
        "occupier_address": "Unit 5, Harford Bridge Business Park, Norwich, NR4 6AZ",
        "property_address": "Unit 5, Harford Bridge Business Park, Norwich, NR4 6AZ",
        "postcode": "NR4 6AZ",
        "company_number": "08334455",
        "company_status": "active",
        "contract_title": "Extension and Fit-Out of Council Depot",
        "awarded_by": "South Norfolk Council",
        "contract_value": 465900,
    },
]