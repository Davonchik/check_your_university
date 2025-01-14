import aiohttp


class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
    async def create_user(self, tg_id: str):
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.base_url}/user", json={"tg_id": tg_id}) as response:
                return await response.json()
    
    async def create_request(self, data: dict):
        async with aiohttp.ClientSession() as session:
            data["user_id"] = 2
            async with session.post(f"{self.base_url}/request", json=data) as response:
                return await response.json()