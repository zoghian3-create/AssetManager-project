import os
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

DATABASE_URL = f"sqlite:///{os.path.join(DATA_DIR, 'asset_manager.db')}"
engine = create_engine(DATABASE_URL, echo=False)

Base = declarative_base()

class AssetDB(Base):
    __tablename__ = 'assets'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    purchase_date = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    category = Column(String, nullable=False)

class WarrantyDB(Base):
    __tablename__ = 'warranties'
    id = Column(Integer, primary_key=True, autoincrement=True)
    asset_id = Column(Integer, ForeignKey('assets.id'), nullable=False)
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)
    provider = Column(String, nullable=False)

def init_db():
    Base.metadata.create_all(engine)
    print("دیتابیس و جداول با موفقیت ساخته شدند.")

if __name__ == "__main__":
    init_db()