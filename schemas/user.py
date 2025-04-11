from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    name: str
    created_at: int
    updated_at: int
    
    model_config = ConfigDict(
        from_attributes=True
    )

class UserCreate(BaseModel):
    name: str
    
    model_config = ConfigDict(
        from_attributes=True
    )

class UserUpdate(BaseModel):
    name: str | None = None
    
    model_config = ConfigDict(
        from_attributes=True
    )
