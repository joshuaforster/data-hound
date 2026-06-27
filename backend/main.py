from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fake_data import fake_leads as leads
from generate_letter import generate_letter 
from utils import get_lead, get_user
import io 


app = FastAPI()

# Gets individual lead by id
@app.get("/leads/{lead_id}")
def get_leads_by_id(lead_id:str):
    lead = get_lead(lead_id)
    return lead

# Gets all leads 
@app.get("/leads/")
def get_leads():
    return leads


# Gets posts info for letter preview 
@app.post("/leads/{lead_id}/preview/{user_id}")
def preview_letter(lead_id:str, user_id:str):
    lead = get_lead(lead_id)
    sender = get_user(user_id)
    letter = generate_letter(lead, sender)
    response = StreamingResponse(
    io.BytesIO(letter.output()),
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=preview.pdf"}
    )
    return response
    
