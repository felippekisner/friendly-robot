import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker
import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError

load_dotenv()

try:
    secret_config = st.secrets["database"]
except (KeyError, StreamlitSecretNotFoundError):
    secret_config = {}

mysql_config = {
    "MYSQL_HOST": os.getenv("MYSQL_HOST") or secret_config.get("host"),
    "MYSQL_PORT": os.getenv("MYSQL_PORT") or secret_config.get("port"),
    "MYSQL_DATABASE": os.getenv("MYSQL_DATABASE") or secret_config.get("database"),
    "MYSQL_USER": os.getenv("MYSQL_USER") or secret_config.get("user"),
    "MYSQL_PASSWORD": os.getenv("MYSQL_PASSWORD") or secret_config.get("password"),
}
use_mysql_setting = os.getenv("USE_MYSQL")
use_mysql = (
    use_mysql_setting.strip().lower() == "true"
    if use_mysql_setting is not None
    else any(mysql_config.values())
)

if use_mysql:
    missing_settings = [name for name, value in mysql_config.items() if not value]
    if missing_settings:
        raise ValueError(
            "Missing MySQL settings in the environment or Streamlit secrets: "
            + ", ".join(missing_settings)
        )

    database_url = URL.create(
        "mysql+pymysql",
        username=mysql_config["MYSQL_USER"],
        password=mysql_config["MYSQL_PASSWORD"],
        host=mysql_config["MYSQL_HOST"],
        port=int(mysql_config["MYSQL_PORT"]),
        database=mysql_config["MYSQL_DATABASE"],
    )
    engine = create_engine(database_url, pool_pre_ping=True)
else:
    project_root = Path(__file__).resolve().parent.parent
    database_path = project_root / "data" / "festa_ifc.sqlite3"
    database_path.parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine(
        f"sqlite:///{database_path.as_posix()}",
        connect_args={"check_same_thread": False},
    )

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db():
    if __package__ == "src":
        from .models import Base
    else:
        from models import Base

    Base.metadata.create_all(bind=engine)