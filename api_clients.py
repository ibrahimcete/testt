import requests

class TrendyolClient:
    BASE_URL = "https://api.trendyol.com/sapigw/suppliers"

    def __init__(self, api_key, api_secret, supplier_id):
        self.api_key = api_key
        self.api_secret = api_secret
        self.supplier_id = supplier_id

    def get_orders(self, status=None, page=0, size=20):
        url = f"{self.BASE_URL}/{self.supplier_id}/orders"
        headers = {
            "Authorization": f"Basic {self.api_key}:{self.api_secret}",
            "Content-Type": "application/json"
        }
        params = {
            "status": status or "Created",
            "page": page,
            "size": size
        }
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        return resp.json().get("content", [])