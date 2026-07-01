import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def create_tables():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME", "scraper"),
        user=os.getenv("DB_USER", "joshuaforster"),
        host="localhost",
    )
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id       uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            name          text,
            company_name  text,
            address       text,
            phone         text,
            email         text UNIQUE,
            hashed_password text,
            website       text,
            logo_path     text,
            sign_off      text,
            created_at    timestamptz DEFAULT now()
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            lead_id       uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            source        text NOT NULL,
            applicant_name text,
            occupier_address text,
            property_address text,
            postcode      text,
            council       text,
            proposal      text,
            council_reference text,
            agent_name    text,
            agent_company_name text,
            agent_company_address text,
            company_number text,
            contract_title text,
            awarded_by    text,
            contract_value numeric,
            created_at    timestamptz DEFAULT now()
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS templates (
            template_id    uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id        uuid REFERENCES users(user_id),
            recipient_type text,
            subject        text,
            body           text,
            created_at     timestamptz DEFAULT now()
        );
    """)

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

    conn.commit()
    cur.close()
    conn.close()
    print("All tables created (or already existed).")



def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME", "scraper"),
        user=os.getenv("DB_USER", "joshuaforster"),
        host="localhost",
    )


if __name__ == "__main__":
    create_tables()