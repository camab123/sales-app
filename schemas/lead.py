from pydantic import BaseModel, ConfigDict


class Lead(BaseModel):
    id: int
    name: str
    contact_information: str
    source: str
    interest_level: str
    status: str
    assigned_salesperson_id: int
    created_at: int
    updated_at: int

    model_config = ConfigDict(
        from_attributes=True
    )

class LeadCreate(BaseModel):
    name: str
    contact_information: str
    source: str
    interest_level: str
    status: str
    assigned_salesperson_id: int

    model_config = ConfigDict(
        from_attributes=True
    )

class LeadUpdate(BaseModel):
    name: str | None = None
    contact_information: str | None = None
    source: str | None = None
    interest_level: str | None = None
    status: str | None = None
    assigned_salesperson_id: int | None = None

    model_config = ConfigDict(
        from_attributes=True
    )

class LeadFilters(BaseModel):
    name: str | None = None
    contact_information: str | None = None
    source: str | None = None
    interest_level: str | None = None
    status: str | None = None
    assigned_salesperson_id: int | None = None
    page: int = 1
    page_size: int = 10
    sort_by: str | None = None
    sort_order: str | None = None
