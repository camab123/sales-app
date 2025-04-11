from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from typing import AsyncGenerator
from config import DB_STRING

# Create an async engine
engine = create_async_engine(DB_STRING, echo=True)

# Create an async session
async_session = AsyncSession(engine, expire_on_commit=False)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session