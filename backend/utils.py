from fake_data import fake_leads as leads, fake_users as users, fake_templates as templates, fake_contract_leads as contract_leads

def get_lead(lead_id):
    for lead in leads:
        if lead.get("lead_id") == lead_id:
            return lead

def get_contract_lead(lead_id):
    for lead in contract_leads:
        if lead["lead_id"] == lead_id:
            return lead
    return None

def get_user(user_id):
    for user in users:
        if user.get("user_id") == user_id:
            return user
        
def get_template(template_id):
    for template in templates:
        if template.get("template_id") == template_id:
            return template

def fill(text, lead):
    for key, value in lead.items():
        text = text.replace("{" + key + "}", str(value))
    return text

def fill_template(template, lead):
    subject = fill(template["subject"], lead)
    body = fill(template["body"], lead)
    return subject, body