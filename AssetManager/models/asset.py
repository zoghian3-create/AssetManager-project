class Asset:
    def __init__(self, asset_id, name, purchase_date, price, category):
        self.asset_id = asset_id
        self.name = name 
        self.purchase_date = purchase_date
        self.price = price
        self.category = category
        
    def to_dict(self):
        return {
            "asset_id": self.asset_id,
            "name": self.name,
            "purchase_date": self.purchase_date,
            "price": self.price,
            "category": self.category,
            
            }
    
    
    def __str__(self):
      return f"ID: {self.asset_id} name: {self.name} price: {self.price}"
    
    
    @classmethod
    def from_dict(cls, data):
       return cls(
        data["asset_id"],
        data["name"],
        data["purchase_date"],
        data["price"],
        data["category"],
        )