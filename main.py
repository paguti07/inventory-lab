import asyncio
from api_client import InventoryAPIClient
from report_generator import InventoryReportGenerator
import time

async def main():
    async_start = time.perf_counter()

    async with InventoryAPIClient() as client:
        raw_data = await client.fetch_all_products(
            batch_size=100
        )

    async_end = time.perf_counter()

    async_elapsed = async_end - async_start


    sync_start = time.perf_counter()

    report = InventoryReportGenerator(raw_data)

    report.process_inventory(
        low_stock_threshold=10
    )

    report.export_csv(
        "inventory_report.csv"
    )

    report.export_summary_metrics(
        "inventory_summary.json"
    )

    sync_end = time.perf_counter()

    sync_elapsed = sync_end - sync_start


    print(f"Async API time:   {async_elapsed:.4f} seconds")
    print(f"Sync report time: {sync_elapsed:.4f} seconds")
    print(f"Total time:       {async_elapsed + sync_elapsed:.4f} seconds")
    print("Inventory report generated successfully.")


if __name__ == "__main__":
    asyncio.run(main())
