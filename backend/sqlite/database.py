from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///./mydatabase.db', echo=True)
Base = declarative_base()

session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def db():
    db = session()
    try:
        yield db
    finally:
        db.close()