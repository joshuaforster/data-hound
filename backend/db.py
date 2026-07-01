import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME", "scraper"),
        user=os.getenv("DB_USER", "joshuaforster"),
        host="localhost",
    )


def query(sql, params=None, fetch=None):
    """One door to the database. fetch='one' or 'all' to get rows back."""
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(sql, params or [])

    result = None
    if fetch == "one":
        result = cur.fetchone()
    elif fetch == "all":
        result = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()
    return result


def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    # -------- USERS (your clients) --------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            name            text,
            company_name    text,
            address         text,
            phone           text,
            email           text UNIQUE,
            hashed_password text,
            website         text,
            logo_path       text,
            sign_off        text,
            created_at      timestamptz DEFAULT now()
        );
    """)

    # -------- LEADS (all sources: planning, contract, company) --------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            lead_id               uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            source                text NOT NULL,
            recipient_type        text,

            -- shared
            applicant_name        text,
            occupier_address      text,
            property_address      text,
            postcode              text,
            status                text,

            -- planning-specific
            council               text,
            council_reference     text,
            proposal              text,
            application_type      text,
            parish                text,
            ward                  text,
            agent_name            text,
            agent_company_name    text,
            agent_company_address text,
            eia_required          boolean,
            received_date         text,
            validation_date       text,
            determination_deadline text,
            url                   text,

            -- contract/company-specific
            company_number        text,
            company_status        text,
            contract_title        text,
            awarded_by            text,
            contract_value        numeric,

            created_at            timestamptz DEFAULT now()
        );
    """)

    # -------- TEMPLATES (per-user later; user_id null = shared default) --------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS templates (
            template_id    uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id        uuid REFERENCES users(user_id),
            name           text,
            category       text,
            recipient_type text,
            subject        text,
            body           text,
            created_at     timestamptz DEFAULT now()
        );
    """)

    # -------- SENT LETTERS (history + cost tracking) --------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sent_letters (
            id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id     uuid REFERENCES users(user_id),
            lead_id     uuid REFERENCES leads(lead_id),
            template_id uuid,
            subject     text,
            body        text,
            status      text DEFAULT 'sent',
            pingen_id   text,
            cost        numeric,
            created_at  timestamptz DEFAULT now()
        );
    """)

    # -------- FAVOURITES (which user starred which lead) --------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS favourites (
            user_id    uuid REFERENCES users(user_id),
            lead_id    uuid REFERENCES leads(lead_id),
            created_at timestamptz DEFAULT now(),
            PRIMARY KEY (user_id, lead_id)
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("All tables created (or already existed).")


if __name__ == "__main__":
    create_tables()
  