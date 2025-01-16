import aiohttp
from io import BytesIO


class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
    async def create_user(self, tg_id: str):
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.base_url}/user", json={"tg_id": tg_id}) as response:
                return await response.json()
    
    async def create_request(self, data: dict, file1: BytesIO):
        async with aiohttp.ClientSession() as session:
            form_data = aiohttp.FormData()
            form_data.add_field("user_id", str(data["user_id"]))
            form_data.add_field("building_name", data["building_name"])
            form_data.add_field("category", data["category"])
            form_data.add_field("room", data["room"])
            form_data.add_field("text", data["text"])
            form_data.add_field("file", file1, filename=file1.name, content_type="image/octet-stream")
            async with session.post(f"{self.base_url}/request/", data=form_data, allow_redirects=False) as response:
                print("test")