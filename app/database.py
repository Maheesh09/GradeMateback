from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

# Use SQLite for testing - no database server required
DATABASE_URL = "mysql+aiomysql://root:Maheesha%40123@localhost:3306/hackathon_db"

# Uncomment the line below to use MySQL (requires MySQL server running)
# DATABASE_URL = (
#     f"mysql+aiomysql://{settings.DB_USER}:{settings.DB_PASS}"
#     f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
# )

engine = create_async_engine(DATABASE_URL, echo=False, future=True)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
