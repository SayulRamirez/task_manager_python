import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()
DB_URL = os.getenv('SQLITE_PATH')

if not DB_URL:
    raise ValueError('No se encontro la ruta de la base de datos')

engine = create_engine(
    url=DB_URL,
    connect_args={'check_same_thread': False}
)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()