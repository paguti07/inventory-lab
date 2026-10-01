import json
from pathlib import Path

import pandas as pd


class InventoryReportGenerator:
    """Transforms raw product API data into structured business reports."""

    def __init__(self, raw_data: list[dict]):
        self.df = pd.DataFrame(raw_data)

    def process_inventory(
        self,
        low_stock_threshold: int = 10,
    ) -> pd.DataFrame:
        """Calculate discounted prices and identify low-stock items."""

        self.df["discounted_price"] = (
            self.df["price"]
            * (1 - self.df["discountPercentage"] / 100)
        )

        self.df["low_stock_warning"] = (
            self.df["stock"] < low_stock_threshold
        )

        columns = [
            "id",
            "title",
            "category",
            "price",
            "discountPercentage",
            "discounted_price",
            "stock",
            "low_stock_warning",
        ]

        self.df = self.df[columns]

        return self.df

    def export_csv(self, destination: str | Path) -> None:
        """Export the processed DataFrame to CSV."""

        self.df.to_csv(
            destination,
            index=False,
        )

    def export_summary_metrics(
        self,
        destination: str | Path,
    ) -> None:
        """Export high-level metrics as JSON."""

        total_inventory_value = (
            self.df["price"] * self.df["stock"]
        ).sum()

        metrics = {
            "item_count": int(len(self.df)),
            "total_inventory_value": float(total_inventory_value),
        }

        Path(destination).write_text(
            json.dumps(metrics, indent=2),
            encoding="utf-8",
        )