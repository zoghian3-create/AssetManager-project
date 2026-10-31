from fastapi import FastAPI
from services.storage_service import get_all_assets

# ساخت اپلیکیشن FastAPI
app = FastAPI(title="Persian Date & Asset Manager API")

# تعریف یک مسیر (Endpoint) برای گرفتن لیست کالاها
@app.get("/assets")
def read_assets():
    assets = get_all_assets()
    # تبدیل شیء به دیکشنری برای اینکه FastAPI بتونه نشونش بده
    return [asset.to_dict() for asset in assets]

@app.get("/")
def home():
    return {"message": "سیستم مدیریت دارایی تسلا آماده است!"}

from pydantic import BaseModel
from services.storage_service import save_asset
from models.asset import Asset

# تعریف ساختاری که کاربر باید بفرسته
class AssetCreate(BaseModel):
    name: str
    purchase_date: str
    price: float
    category: str

@app.post("/assets")
def create_asset(asset_data: AssetCreate):
    new_asset = Asset(
        asset_id=0, # دیتابیس خودش ID میده
        name=asset_data.name,
        purchase_date=asset_data.purchase_date,
        price=asset_data.price,
        category=asset_data.category
    )
    save_asset(new_asset)
    return {"message": "کالا با موفقیت ثبت شد", "name": new_asset.name}