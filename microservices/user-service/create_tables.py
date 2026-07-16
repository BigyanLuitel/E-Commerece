from sqlmodel import SQLModel
from database import engine
import models  # noqa: F401 - needed so SQLModel registers the User table

SQLModel.metadata.create_all(engine)