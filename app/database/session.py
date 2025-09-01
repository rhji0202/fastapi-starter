import logging
from urllib.parse import urlparse
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.config.settings import settings


logger = logging.getLogger(__name__)
engine = create_async_engine(settings.DATABASE_URL, echo=False, isolation_level="AUTOCOMMIT")
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
  async with AsyncSessionLocal() as session:
    try:
      yield session
    finally:
      await session.close()


async def initialize_db():
  url_parts = urlparse(settings.DATABASE_URL)
  db_name = url_parts.path.lstrip("/")

  if not db_name:
    logger.warning("No database name found in DATABASE_URL; cannot proceed with creation.")
    raise ValueError("DATABASE_URL must include a database name.")

  # SQLite는 별도의 데이터베이스 생성이 필요하지 않음
  # 파일이 존재하지 않으면 자동으로 생성됨
  if "sqlite" in settings.DATABASE_URL:
    logger.info(f"SQLite database '{db_name}' will be automatically created if it doesn't exist.")
    return

  # PostgreSQL 데이터베이스 생성 로직
  default_engine = create_async_engine(settings.DEFAULT_DATABASE_URL, echo=False, isolation_level="AUTOCOMMIT")
  try:
    async with default_engine.connect() as conn:
      result = await conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'"))
      if not result.scalar():
        logger.info(f"Database '{db_name}' does not exist. Creating ...")
        await conn.execute(text(f'CREATE DATABASE "{db_name}"'))
        logger.info(f"Database '{db_name}' created successfully.")
      else:
        logger.info(f"Database '{db_name}' already exists; skipping creation.")
  except OperationalError as e:
    logger.error(f"An error occurred while initializing the database: {e}")
    raise SystemExit("Database connectivity check failed at startup.") from e
  finally:
    await default_engine.dispose()
