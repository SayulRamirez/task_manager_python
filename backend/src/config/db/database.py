from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.enviroment import get_env

DB_HOST = get_env('DB_HOST')
DB_PORT = get_env('DB_PORT')
DB_USER = get_env('DB_USER')
DB_PASS = get_env('DB_PASS')
DB_NAME = get_env('DB_NAME')

DB_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DB_URL)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()