# models.py
from datetime import datetime
from sqlalchemy import create_engine, Integer, String, Text, DateTime, func
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column

# Используем синхронный режим
PG_DSN = "postgresql://user:1234@localhost:5431/ads_db"

engine = create_engine(PG_DSN)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Advertisement(Base):
    __tablename__ = "advertisement"

    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String(100), nullable=False)
    description = mapped_column(Text, nullable=False)
    created_at = mapped_column(DateTime, server_default=func.now())
    owner = mapped_column(String(50), nullable=False)

    @property
    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "owner": self.owner,
        }
Base.metadata.create_all(engine)