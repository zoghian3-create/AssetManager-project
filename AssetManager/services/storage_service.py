from sqlalchemy.orm import sessionmaker
from AssetManager.services.database import engine, AssetDB, WarrantyDB
from models.asset import Asset
from models.warranty import Warranty

# ساخت نشست (Session) برای ارتباط با دیتابیس
SessionLocal = sessionmaker(bind=engine)

def get_all_assets():
    session = SessionLocal()
    db_assets = session.query(AssetDB).all()
    session.close()
    # تبدیل به شیء Asset برای استفاده در main.py
    return [Asset(a.id, a.name, a.purchase_date, a.price, a.category) for a in db_assets]

def save_asset(asset):
    session = SessionLocal()
    db_asset = AssetDB(name=asset.name, purchase_date=asset.purchase_date, price=asset.price, category=asset.category)
    session.add(db_asset)
    session.commit()
    session.close()

def get_all_warranties():
    session = SessionLocal()
    db_warranties = session.query(WarrantyDB).all()
    session.close()
    return [Warranty(w.id, w.asset_id, w.start_date, w.end_date, w.provider) for w in db_warranties]

def save_warranty(warranty):
    session = SessionLocal()
    db_warranty = WarrantyDB(asset_id=warranty.asset_id, start_date=warranty.start_date, end_date=warranty.end_date, provider=warranty.provider)
    session.add(db_warranty)
    session.commit()
    session.close()