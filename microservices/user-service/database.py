import os
from dotenv import load_dotenv  
from sqlmodel  import Session, create_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(os.getenv("DATABASE_URL"))

def get_engine():
    with Session(engine) as session:
        yield session
