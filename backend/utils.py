from fake_data import fake_leads as leads, fake_users as users

def get_lead(lead_id):
    for lead in leads:
        if lead.get("lead_id") == lead_id:
            return lead

def get_user(user_id):
    for user in users:
        if user.get("user_id") == user_id:
            return user