import csv
from schemas.lead import LeadCreate
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging

logger = logging.getLogger(__name__)

async def convert_upload_to_leads(data: bytes, session: AsyncSession) -> list[LeadCreate]:
    leads = []
    lines = data.decode('utf-8').splitlines()
    reader = csv.DictReader(lines)
    
    for row in reader:
        print(row)
        user = await session.execute(
            select(User).where(User.name == row["Assigned Salesperson"])
        )
        user = user.scalars().first()
        if not user:
            logger.warning(f"User with ID {row['Assigned Salesperson']} not found. Creating a new user.")
            user = User(name=row["Assigned Salesperson"])
            session.add(user)
            await session.flush([user])
            await session.refresh(user)
            logger.info(f"User created with ID {user.id}")

        lead = LeadCreate(
            name=row["Lead Name"],
            contact_information=row["Contact Information"],
            source=row["Source"].lower().replace(" ", "_"),
            interest_level=row["Interest Level"].lower(),
            status=row["Status"].lower(),
            assigned_salesperson_id=user.id,
        )
        leads.append(lead)
    return leads