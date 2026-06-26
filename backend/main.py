from fastapi import FastAPI
from fake_data import fake_leads as leads

app = FastAPI()

@app.get("/leads/{id}")
def get_leads_by_id(id:str):
    for lead in leads:
        if lead.get('my_reference') == id:
            return lead


@app.get("/leads/")
def get_leads():
    return leads