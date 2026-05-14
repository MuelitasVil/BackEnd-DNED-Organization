from sqlmodel import SQLModel, create_engine, Session
from app.configuration.settings import settings

MYSQL_USER = settings.MYSQL_USER
MYSQL_ROOT = settings.MYSQL_ROOT
MYSQL_ROOT_PASSWORD = settings.MYSQL_ROOT_PASSWORD
MYSQL_USER_PASSWORD = settings.MYSQL_USER_PASSWORD
MYSQL_HOST = settings.MYSQL_HOST
MYSQL_PORT = settings.MYSQL_PORT
MYSQL_DATABASE = settings.MYSQL_DATABASE

DATABASE_URL = (
    f"mysql+pymysql://{MYSQL_ROOT}:{MYSQL_ROOT_PASSWORD}"
    f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
)

print(f"Connecting to database at {DATABASE_URL}")
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
