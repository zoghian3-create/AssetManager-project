class Warranty:
    def __init__(self, warranty_id, asset_id, start_date, end_date, provider):
        self.warranty_id = warranty_id
        self.asset_id = asset_id
        self.start_date = start_date
        self.end_date = end_date
        self.provider = provider

    def to_dict(self):
        return {
            "warranty_id": self.warranty_id,
            "asset_id": self.asset_id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "provider": self.provider,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["warranty_id"],
            data["asset_id"],
            data["start_date"],
            data["end_date"],
            data["provider"],
        )

    def __str__(self):
        return (
            f"Warranty {self.warranty_id} | Asset {self.asset_id} | "
            f"Provider: {self.provider} | {self.start_date} تا {self.end_date}"
        )