from datetime import datetime
from enum import Enum
from sqlalchemy import String, Integer, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncSession
from models.base import Base
from schemas.lead import LeadCreate
from sqlalchemy import select, and_
from models.user import User
from schemas.lead import LeadFilters

class Source(Enum):
    referral = 0
    website = 1
    cold_call = 2
    event = 3

class InterestLevel(Enum):
    low = 0
    medium = 1
    high = 2

class Status(Enum):
    new = 0
    closed = 1
    qualified = 2
    contacted = 3

class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, index=True)
    contact_information: Mapped[str] = mapped_column(String)
    source: Mapped[Source] = mapped_column(SQLAlchemyEnum(Source))
    interest_level: Mapped[InterestLevel] = mapped_column(SQLAlchemyEnum(InterestLevel))
    status: Mapped[Status] = mapped_column(SQLAlchemyEnum(Status))
    
    assigned_salesperson_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    assigned_salesperson: Mapped[User] = relationship("User", back_populates="leads")
    
    created_at: Mapped[int] = mapped_column(
        Integer, default=lambda: int(datetime.now().timestamp())
    )
    updated_at: Mapped[int] = mapped_column(
        Integer, default=lambda: int(datetime.now().timestamp())
    )

    def bulk_upload(leads: list[LeadCreate], session: AsyncSession) -> list["Lead"]:
        lead_objects = []
        for lead in leads:
            lead_object = Lead(
                name=lead.name,
                contact_information=lead.contact_information,
                source=lead.source,
                interest_level=lead.interest_level,
                status=lead.status,
                assigned_salesperson_id=lead.assigned_salesperson_id
            )
            lead_objects.append(lead_object)
        session.add_all(lead_objects)
        return lead_objects
    
    def build_query(filters: LeadFilters):
        query_filters = []

        # Filter by name using a case-insensitive like search
        if filters.name:
            query_filters.append(Lead.name.ilike(f"%{filters.name}%"))
        
        # Filter by contact_information using a case-insensitive like search
        if filters.contact_information:
            query_filters.append(Lead.contact_information.ilike(f"%{filters.contact_information}%"))
        
        # Convert the string source to its enum and add filter condition
        if filters.source:
            try:
                source_enum = Source[filters.source]  # uses enum member lookup by name
            except KeyError:
                raise ValueError(f"Invalid source '{filters.source}'. Valid options: {[e.name for e in Source]}")
            query_filters.append(Lead.source == source_enum)
        
        # Convert the string interest_level to its enum and add filter condition
        if filters.interest_level:
            try:
                interest_level_enum = InterestLevel[filters.interest_level]
            except KeyError:
                raise ValueError(f"Invalid interest level '{filters.interest_level}'. Valid options: {[e.name for e in InterestLevel]}")
            query_filters.append(Lead.interest_level == interest_level_enum)
        
        # Convert the string status to its enum and add filter condition
        if filters.status:
            try:
                status_enum = Status[filters.status]
            except KeyError:
                raise ValueError(f"Invalid status '{filters.status}'. Valid options: {[e.name for e in Status]}")
            query_filters.append(Lead.status == status_enum)
        
        # Filter on assigned_salesperson_id, if provided
        if filters.assigned_salesperson_id is not None:
            query_filters.append(Lead.assigned_salesperson_id == filters.assigned_salesperson_id)
        
        query = select(Lead)
        if query_filters:
            query = query.where(and_(*query_filters))

        # Apply sorting if specified
        if filters.sort_by:
            if filters.sort_order == "desc":
                query = query.order_by(getattr(Lead, filters.sort_by).desc())
            else:
                query = query.order_by(getattr(Lead, filters.sort_by))
        else:
            query = query.order_by(Lead.created_at.desc())

        query = query.offset((filters.page - 1) * filters.page_size).limit(filters.page_size)
        return query
