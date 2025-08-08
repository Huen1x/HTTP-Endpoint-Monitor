from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./endpoints.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Endpoint(Base):
    __tablename__ = "endpoints"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True, nullable=False)
    count = Column(Integer, default=0, nullable=False)


def init_db():
    Base.metadata.create_all(bind=engine)
