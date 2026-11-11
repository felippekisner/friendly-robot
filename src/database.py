import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

try:
    from src.models import Base
except ModuleNotFoundError:
    from models import Base

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)


def get_database_url() -> str:
    use_mysql = os.getenv("USE_MYSQL", "false").strip().lower() in {"1", "true", "yes", "y"}

    if use_mysql:
        host = os.getenv("MYSQL_HOST", "localhost")
        port = os.getenv("MYSQL_PORT", "3306")
        database = os.getenv("MYSQL_DATABASE", "festa_ifc")
        user = os.getenv("MYSQL_USER", "root")
        password = os.getenv("MYSQL_PASSWORD", "")
        return f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

    sqlite_path = DATA_DIR / "festa_ifc.sqlite3"
    return f"sqlite:///{sqlite_path}"


def get_engine():
    url = get_database_url()
    if url.startswith("sqlite"):
        return create_engine(url, connect_args={"check_same_thread": False})
    return create_engine(url, pool_pre_ping=True)


SessionLocal = sessionmaker(bind=get_engine(), autoflush=False, autocommit=False)


def init_db() -> None:
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
