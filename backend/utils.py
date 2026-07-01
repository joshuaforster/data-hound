from db import query


def get_user(user_id):
    return query("SELECT * FROM users WHERE user_id = %s", [user_id], fetch="one")


def get_lead(lead_id):
    return query("SELECT * FROM leads WHERE lead_id = %s", [lead_id], fetch="one")


def get_template(template_id):
    return query("SELECT * FROM templates WHERE template_id = %s", [template_id], fetch="one")


def fill(text, data):
    for key, value in data.items():
        if value is not None:
            text = text.replace("{" + key + "}", str(value))
    return text


def fill_template(template, lead):
    subject = fill(template["subject"], lead)
    body = fill(template["body"], lead)
    return subject, body