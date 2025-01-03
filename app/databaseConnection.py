from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

# PostgreSQL connection URL
SQLALCHEMY_DATABASE_URL = f'''postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{
                              settings.database_hostname}:{settings.database_port}/{settings.database_name}'''

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def connection_test():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print(f"Connection successful! {result.fetchone()}")
    except Exception as e:
        print(f"Connection failed! {str(e)}")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    get_db()