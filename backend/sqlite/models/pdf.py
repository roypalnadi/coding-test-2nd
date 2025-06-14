from fileinput import filename
from sqlite.database import Base, db
from sqlalchemy.orm import Session, Mapped, mapped_column
from sqlalchemy import String, Integer
from typing import List
from uuid import uuid4

class Pdf(Base):
    __tablename__ = 'pdfs'
    uuid: Mapped[str] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(String)
    path: Mapped[str] = mapped_column(String)
    upload_date: Mapped[str] = mapped_column(String)
    chunks_count: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String)

def create(filename: str, upload_date: str, chunks_count: int, path: str, status: str, db: Session) -> Pdf:
    pdf = Pdf(
        uuid=str(uuid4()),
        filename=filename,
        upload_date=upload_date,
        chunks_count=chunks_count,
        path=path,
        status=status
    )

    db.add(pdf)
    db.commit()
    db.refresh(pdf)
    return pdf

def get_all(db: Session) -> List[Pdf]:
    return db.query(Pdf).all()
