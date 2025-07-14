from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
from typing import List, Dict

app = FastAPI(title="Lead Scoring API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Lead(BaseModel):
    phone_number: str
    email: str
    credit_score: int
    age_group: str
    family_background: str
    income: int
    comments: str
    consent: bool

class LeadScoreResponse(BaseModel):
    email: str
    initial_score: float
    reranked_score: float
    comments: str

# In-memory storage for leads
leads = []

# Load the trained model
try:
    model = joblib.load("model/lead_scoring_model.pkl")
except:
    model = None

@app.post("/score", response_model=LeadScoreResponse)
async def score_lead(lead: Lead):
    if not lead.consent:
        raise HTTPException(status_code=400, detail="Consent is required")
    
    # Validate email format
    if "@" not in lead.email:
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    # Validate phone number format
    if not lead.phone_number.startswith("+91"):
        raise HTTPException(status_code=400, detail="Invalid phone number format")
    
    # Convert categorical variables
    age_map = {
        "18-25": 0,
        "26-35": 1,
        "36-50": 2,
        "51+": 3
    }
    
    family_map = {
        "Single": 0,
        "Married": 1,
        "Married with Kids": 2
    }
    
    # Prepare features for prediction
    features = {
        "credit_score": lead.credit_score,
        "age_group": age_map[lead.age_group],
        "family_background": family_map[lead.family_background],
        "income": lead.income
    }
    
    # Convert to DataFrame
    df = pd.DataFrame([features])
    
    # Get initial score from ML model
    if model is not None:
        initial_score = float(model.predict_proba(df)[0][1]) * 100
    else:
        initial_score = 50.0  # Default score if model not loaded
    
    # LLM-inspired re-ranking based on comments
    keywords = {
        "urgent": 10,
        "now": 5,
        "immediately": 5,
        "interested": 5,
        "not interested": -10,
        "later": -5,
        "maybe": -5
    }
    
    reranked_score = initial_score
    for keyword, adjustment in keywords.items():
        if keyword.lower() in lead.comments.lower():
            reranked_score += adjustment
    
    # Cap score between 0 and 100
    reranked_score = max(0, min(100, reranked_score))
    
    # Store lead
    leads.append({
        "email": lead.email,
        "initial_score": initial_score,
        "reranked_score": reranked_score,
        "comments": lead.comments
    })
    
    return LeadScoreResponse(
        email=lead.email,
        initial_score=initial_score,
        reranked_score=reranked_score,
        comments=lead.comments
    )

@app.get("/leads")
async def get_leads():
    return leads

@app.options("/score")
async def score_lead_options():
    return {"message": "Options request received"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
