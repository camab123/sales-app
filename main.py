from fastapi import FastAPI, UploadFile, HTTPException, Depends
from lib.utils import convert_upload_to_leads
from models.lead import Lead
from db_engine import get_session
from schemas.lead import LeadCreate, LeadUpdate, LeadFilters
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()


@app.post("/upload_csv/")
async def upload_csv(file: UploadFile, session: AsyncSession = Depends(get_session)):
    """
    Upload a CSV file and process it.
    """
    if not file.content_type == 'text/csv':
        raise HTTPException(status_code=400, detail="File is not a CSV")
    
    content = await file.read()
    leads = await convert_upload_to_leads(data=content, session=session)
    if not leads:
        raise HTTPException(status_code=400, detail="No valid leads found in the CSV")
    
    # Bulk upload leads to the database
    lead_objects = Lead.bulk_upload(leads=leads, session=session)
    await session.commit()
    return {"message": "CSV file processed successfully", "leads": lead_objects}

@app.get("/lead/")
async def get_lead(lead_id: int, session: AsyncSession = Depends(get_session)):
    """
    Retrieve a lead by ID.
    """
    lead = await session.get(Lead, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    return lead

@app.get("/leads/")
async def get_leads(session: AsyncSession = Depends(get_session), filters: LeadFilters = Depends()):
    """
    Retrieve leads with optional filters.
    """
    leads = await session.execute(
        Lead.build_query(filters=filters)
    )
    if not leads:
        raise HTTPException(status_code=404, detail="No leads found")
    return leads.scalars().all()

@app.delete("/lead/{lead_id}")
async def delete_lead(lead_id: int, session: AsyncSession = Depends(get_session)):
    """
    Delete a lead by ID.
    """
    lead = await session.get(Lead, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    await session.delete(instance=lead)
    session.commit()
    return {"message": "Lead deleted successfully"}

@app.put("/lead/{lead_id}")
async def update_lead(lead_id: int, lead_data: LeadUpdate, session: AsyncSession = Depends(get_session)):
    """
    Update a lead by ID.
    """
    lead = await session.get(Lead, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    for key, value in lead_data.model_dump(exclude_none=True).items():
        setattr(lead, key, value)
    
    await session.commit()
    return {"message": "Lead updated successfully", "lead": lead}

@app.post("/lead/")
async def create_lead(lead_data: LeadCreate, session: AsyncSession = Depends(get_session)):
    """
    Create a new lead.
    """
    lead = Lead(**lead_data.model_dump())
    session.add(lead)
    session.commit()
    return {"message": "Lead created successfully", "lead": lead}
