from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from dotenv import load_dotenv
import os
# load_dotenv()

# DATABASE_URL = os.environ.get("DATABASE_URL")
# DATABASE_URL = "postgresql://root:toor@postgres:5432/db"
DATABASE_URL=os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for getting DB session
def get_db():
    with Session() as session:
        yield session


if __name__ == "__main__":
    try:
        db = Session()
        print("Database connection successful!")
    except Exception as e:
        print("Error connecting to the database:", e)
    finally:
        db.close()
