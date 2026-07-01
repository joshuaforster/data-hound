from db import query


def seed_templates():
    # wipe existing generics first so re-running never duplicates
    query("DELETE FROM templates WHERE user_id IS NULL")

    templates = [
        ("Occupier Introduction", "planning", "occupier",
         "Re: your planning application {council_reference}",
         "I noticed that a planning application ({council_reference}) was recently "
         "submitted for {property_address}, proposing {proposal}.\n\n"
         "I'm a local builder, and I work with homeowners on projects exactly like "
         "this one. I wanted to introduce myself early, before the diggers arrive, "
         "in case it's useful to have an experienced builder you can talk things "
         "through with.\n\n"
         "There's no obligation here at all. If you'd like an informal chat about the "
         "build, my details are at the top of this letter."),

        ("Occupier Local Angle", "planning", "occupier",
         "Re: your planning application {council_reference}",
         "I noticed that a planning application ({council_reference}) was recently "
         "submitted for {property_address}, proposing {proposal}.\n\n"
         "This kind of project is one of my favourites to work on, and I've completed "
         "a good few across {parish}, so I know what it takes to get it right.\n\n"
         "I'm a local builder, and I wanted to introduce myself early, before the "
         "work begins, in case it's useful to have an experienced pair of hands to "
         "talk it through with. No obligation at all. My details are at the top."),

        ("Occupier Developer", "planning", "occupier",
         "Re: planning application {council_reference}",
         "I saw that you've applied for {proposal} at {property_address}.\n\n"
         "We specialise in projects exactly this size, where the applicant wants a "
         "reliable builder who can deliver to a consistent standard without the "
         "headache of managing several trades yourself.\n\n"
         "If you've not yet appointed a contractor, I'd value the chance to quote. "
         "Happy to share references from similar work we've completed locally."),

        ("Change of Use", "planning", "occupier",
         "Re: change of use application {council_reference}",
         "I noticed your application for {proposal} at {property_address}.\n\n"
         "Projects like this live or die on getting the layout and the detail right "
         "for how the space will actually be used. It's a different job from a "
         "standard build, and it's one we've done before.\n\n"
         "If the scheme moves forward, I'd welcome the chance to talk it through with "
         "you. My details are above."),

        ("Agent Introduction", "planning", "agent",
         "Re: planning application {council_reference}",
         "I saw that {agent_company_name} recently submitted planning application "
         "{council_reference} for {proposal} at {property_address}.\n\n"
         "I'm a local builder, and I work alongside agents and designers to deliver "
         "projects like this on the ground. I wanted to introduce myself in case "
         "you're ever looking for a reliable contractor to put in front of a "
         "client.\n\n"
         "I appreciate you'll have builders you already trust. If there's ever a gap, "
         "or a project that needs an extra pair of safe hands, I'd be glad to be on "
         "your list."),

        ("Contract Congratulations", "contract", "occupier",
         "Congratulations on your recent contract award",
         "I saw that {applicant_name} was recently awarded the contract for "
         "{contract_title} by {awarded_by}.\n\n"
         "Congratulations. Winning work like this often means ramping up quickly, "
         "and I wanted to introduce myself in case an extra reliable pair of hands "
         "on site would help you deliver it smoothly.\n\n"
         "No obligation at all. If it would be useful to have a local contractor you "
         "can call on, my details are at the top of this letter."),

        ("Contract Subcontracting", "contract", "occupier",
         "Subcontracting support for {contract_title}",
         "I noticed that {applicant_name} recently won the contract for "
         "{contract_title} with {awarded_by}.\n\n"
         "We work alongside main contractors on projects like this, taking on "
         "packages of work so you can hit your deadlines without stretching your own "
         "team too thin.\n\n"
         "If you're building out your supply chain for this one, I'd welcome a "
         "conversation. References from similar work available on request."),
    ]

    for name, category, recipient_type, subject, body in templates:
        query("""
            INSERT INTO templates (name, category, recipient_type, subject, body)
            VALUES (%s, %s, %s, %s, %s)
        """, [name, category, recipient_type, subject, body])

    print(f"Seeded {len(templates)} generic templates.")


def seed_users():
    # wipe test users first (careful: this clears ALL users)
    # comment this line out once you have real users you want to keep
    query("DELETE FROM users")

    users = [
        ("Larry Lambert", "Lambert and Wright",
         "19 Warren Park Way, Leicester, LE19 4SA", "07710 311165",
         "info@lambertandwright.co.uk", "https://lambertandwright.co.uk",
         "assets/logo.png", "Larry Lambert, Lambert and Wright"),
    ]

    for name, company, address, phone, email, website, logo, sign_off in users:
        query("""
            INSERT INTO users (name, company_name, address, phone, email, website, logo_path, sign_off)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, [name, company, address, phone, email, website, logo, sign_off])

    print(f"Seeded {len(users)} users.")


if __name__ == "__main__":
    seed_templates()
    seed_users()