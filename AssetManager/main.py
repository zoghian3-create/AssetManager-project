import jdatetime
from models.asset import Asset
from models.warranty import Warranty
from services import storage_service


ASSETS_FILE = "assets.json"
WARRANTIES_FILE = "warranties.json"


def ask_int(prompt):
    """تا وقتی عدد معتبر وارد نشود، دوباره می‌پرسد."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("لطفاً فقط عدد وارد کنید.")


def find_asset(assets, asset_id):
    """دارایی با شناسه‌ی داده‌شده را برمی‌گرداند؛ اگر نبود None."""
    for asset in assets:
        if asset.asset_id == asset_id:
            return asset
    return None


def add_asset(assets):
    asset_id = max((a.asset_id for a in assets), default=0) + 1
    name = input("نام دارایی: ")
    purchase_date = input("تاریخ خرید (مثلاً 1405/05/05): ")
    price = ask_int("قیمت: ")
    category = input("دسته‌بندی: ")

    new_asset = Asset(asset_id, name, purchase_date, price, category)
    assets.append(new_asset)
    storage_service.save_asset(new_asset)
    print("دارایی جدید با موفقیت ثبت شد.")


def list_assets(assets):
    if not assets:
        print("هنوز هیچ دارایی‌ای ثبت نشده است.")
        return
    print("\n--- لیست دارایی‌ها ---")
    for asset in assets:
        print(asset)


def add_warranty(warranties, assets):
    if not assets:
        print("ابتدا باید حداقل یک دارایی ثبت کنید.")
        return

    warranty_id = max((w.warranty_id for w in warranties), default=0) + 1

    asset_id = ask_int("شناسه دارایی (Asset ID) که گارانتی برای آن است: ")
    if find_asset(assets, asset_id) is None:
        print("دارایی‌ای با این شناسه وجود ندارد.")
        return

    start_date = input("تاریخ شروع گارانتی (مثلاً 1405/05/05): ")
    end_date = input("تاریخ پایان گارانتی (مثلاً 1406/05/05): ")
    provider = input("شرکت گارانتی‌کننده: ")

    new_warranty = Warranty(warranty_id, asset_id, start_date, end_date, provider)
    warranties.append(new_warranty)
    storage_service.save_warranty(new_warranty)
    print("گارانتی با موفقیت ثبت شد.")


def list_warranties(warranties, assets):
    if not warranties:
        print("هنوز هیچ گارانتی‌ای ثبت نشده است.")
        return
    print("\n--- لیست گارانتی‌ها ---")
    for w in warranties:
        asset = find_asset(assets, w.asset_id)
        asset_name = asset.name if asset else "کالای نامشخص"
        print(f"{w} -> (کالا: {asset_name})")
def check_expiring_warranties(warranties, assets):
    if not warranties:
        print("هیچ گارانتی ثبت نشده است.")
        return
    
    today = jdatetime.date.today()
    print(f"--- گارانتی های منقضی شده یا نزدیک به انقضا در تاریخ {today.strftime('%y/%m/%d')} ---")
    found = False
    for w in warranties:
        try:
            parts = w.end_date.split('/')
            formatted_end_date = f"{int(parts[0]):04d}/{int(parts[2]):02d}"
            end_date_obj = jdatetime.datetime.strptime(formatted_end_date, "%y/%m/%d").date()
            
            days_left = (end_date_obj - today).days
            asset = find_asset(assets, w.asset_id)
            asset_name = asset.name if asset else "کالای نامشخص"
            if days_left < 0:
                print(f"هشدار: گارانتی کالای '{asset_name}' منقضی شده است یا در حال انقضا است! (تارسخ بایان: {w.end_date})")
                found = True
            elif 0 <= days_left <= 30:
                print(f"هشدار: کالای گارانتی '{asset_name}' تا {days_left} روز دیگر منقضی می شود! (تاریخ بایان: {w.end_date})")
                found = True
                
        except Exception:
            print(f"خطا در خواندن تاریخ گارانتی {w.warranty_id}: {w.end_date}")
    if not found:
        print("خبر خوب! هیچ گارانتی در وضعیت هشدار (کمتر از 30 روز) نیست")
    
        
def main():
     
     assets = storage_service.get_all_assets()
     warranties = storage_service.get_all_warranties()

     while True:
        print("\n--- منوی مدیریت دارایی ---")
        print("1) افزودن دارایی جدید")
        print("2) مشاهده لیست دارایی‌ها")
        print("3) ثبت گارانتی جدید")
        print("4) مشاهده لیست گارانتی‌ها")
        print("5) مشاهده گارانتی های در حال انقضا")
        print("0) خروج")

        choice = input("لطفاً یک گزینه را انتخاب کنید: ")

        if choice == "1":
             add_asset(assets)
        elif choice == "2":
             list_assets(assets)
        elif choice == "3":
             add_warranty(warranties, assets)
        elif choice == "4":
             list_warranties(warranties, assets)
        elif choice == "5":
             check_expiring_warranties(warranties, assets)
        elif choice == "0":
             print("از برنامه خارج شدید. خدانگهدار!")
             break
        else:
             print("گزینه نامعتبر است!")


if __name__ == "__main__":
    main()
    