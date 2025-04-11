from sqlalchemy import MetaData

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs


meta = MetaData()

class Base(DeclarativeBase, AsyncAttrs):
    pass