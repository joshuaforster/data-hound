from db import get_connection


def insert_leads(results: list[dict], source: str = "midlands_scraper") -> int:
    """Insert scraper results into leads, skipping duplicates by council_reference + council."""
    conn = get_connection()
    cur = conn.cursor()
    inserted = 0
    for r in results:
        cur.execute(
            """
            INSERT INTO leads (
                source, applicant_name, occupier_address, property_address,
                postcode, council, proposal, council_reference,
                agent_name, agent_company_name, agent_company_address
            )
            SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            WHERE NOT EXISTS (
                SELECT 1 FROM leads
                WHERE council_reference = %s AND council = %s
            )
            """,
            (
                source,
                r.get("applicant_name"),
                r.get("occupier_address"),
                r.get("property_address"),
                r.get("agent_postcode"),
                r.get("council"),
                r.get("proposal"),
                r.get("council_reference"),
                r.get("agent_name"),
                r.get("agent_company_name"),
                r.get("agent_company_address"),
                r.get("council_reference"),
                r.get("council"),
            ),
        )
        inserted += cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    return inserted
