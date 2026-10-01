import asyncio
import httpx


class InventoryAPIClient:

    def __init__(
        self,
        base_url: str = "https://dummyjson.com/products",
    ):
        self.base_url = base_url
        


    async def __aenter__(self):
        self.client = httpx.AsyncClient(
            timeout=10.0,
            limits=httpx.Limits(
                max_connections=10,
                max_keepalive_connections=5,
            ),
            verify=False
        )

        return self

    async def __aexit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        await self.client.aclose()


    async def fetch_page(
        self,
        limit: int,
        skip: int,
    ) -> dict:

        response = await self.client.get(
            self.base_url,
            params={
                "limit": limit,
                "skip": skip,
            },
        )

        response.raise_for_status()

        return response.json()

    async def fetch_all_products(
        self,
        batch_size: int = 30,
    ) -> list[dict]:

        # First request tells us how many items exist
        first_page = await self.fetch_page(
            limit=batch_size,
            skip=0,
        )

        total = first_page["total"]

        products = first_page["products"]

        # Calculate remaining offsets
        offsets = range(
            batch_size,
            total,
            batch_size,
        )

        # Create concurrent tasks
        tasks = [
            self.fetch_page(
                limit=batch_size,
                skip=skip,
            )
            for skip in offsets
        ]

        # Run requests concurrently
        pages = await asyncio.gather(*tasks)

        for page in pages:
            products.extend(page["products"])

        return products

    async def close(self):
        await self.client.aclose()