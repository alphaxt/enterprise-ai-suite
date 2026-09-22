"""
ETL Data Pipeline & SQLite Relational Storage
Validates, cleans, and tracks price drop deltas.
"""

import sqlite3
import csv
import io
from pathlib import Path
from typing import List, Dict, Any, Tuple

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "market_intelligence.db"


class ETLPipeline:
    def __init__(self):
        self.init_database()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        return conn

    def init_database(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sku TEXT NOT NULL,
                    title TEXT NOT NULL,
                    category TEXT NOT NULL,
                    competitor TEXT NOT NULL,
                    current_price REAL NOT NULL,
                    original_price REAL NOT NULL,
                    discount_percentage REAL NOT NULL,
                    in_stock INTEGER NOT NULL,
                    rating REAL NOT NULL,
                    last_scraped_at TEXT NOT NULL,
                    UNIQUE(sku, competitor)
                )
            """)
            conn.commit()

    def process_and_save(self, raw_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Ingests raw records, cleans schema, and checks for price drop alerts."""
        price_drops = []

        with self.get_connection() as conn:
            cursor = conn.cursor()
            for r in raw_records:
                # Check for existing record to calculate delta
                cursor.execute("SELECT current_price FROM products WHERE sku = ? AND competitor = ?", (r["sku"], r["competitor"]))
                existing = cursor.fetchone()

                if existing and existing["current_price"] > r["current_price"]:
                    diff = round(existing["current_price"] - r["current_price"], 2)
                    price_drops.append({
                        "sku": r["sku"],
                        "title": r["title"],
                        "competitor": r["competitor"],
                        "old_price": existing["current_price"],
                        "new_price": r["current_price"],
                        "drop_amount": diff
                    })

                cursor.execute("""
                    INSERT INTO products (sku, title, category, competitor, current_price, original_price, discount_percentage, in_stock, rating, last_scraped_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(sku, competitor) DO UPDATE SET
                        current_price = excluded.current_price,
                        discount_percentage = excluded.discount_percentage,
                        in_stock = excluded.in_stock,
                        rating = excluded.rating,
                        last_scraped_at = excluded.last_scraped_at
                """, (
                    r["sku"],
                    r["title"],
                    r["category"],
                    r["competitor"],
                    r["current_price"],
                    r["original_price"],
                    r["discount_percentage"],
                    1 if r["in_stock"] else 0,
                    r["rating"],
                    r["last_scraped_at"]
                ))
            conn.commit()

        return {
            "records_processed": len(raw_records),
            "price_drops_detected": len(price_drops),
            "price_drops": price_drops
        }

    def fetch_all(self, category: str = None, in_stock_only: bool = False) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM products WHERE 1=1"
            params = []
            if category:
                query += " AND category = ?"
                params.append(category)
            if in_stock_only:
                query += " AND in_stock = 1"
            query += " ORDER BY sku ASC, current_price ASC"
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def get_market_summary(self) -> Dict[str, Any]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as total FROM products")
            total = cursor.fetchone()["total"]

            cursor.execute("SELECT COUNT(DISTINCT competitor) as total_comp FROM products")
            total_comp = cursor.fetchone()["total_comp"]

            cursor.execute("SELECT AVG(discount_percentage) as avg_disc FROM products WHERE discount_percentage > 0")
            avg_disc = cursor.fetchone()["avg_disc"] or 0.0

            cursor.execute("SELECT COUNT(*) as out_of_stock FROM products WHERE in_stock = 0")
            out_of_stock = cursor.fetchone()["out_of_stock"]

            return {
                "total_products": total,
                "competitors_monitored": total_comp,
                "avg_discount_pct": round(avg_disc, 1),
                "out_of_stock_count": out_of_stock
            }

    def export_csv_string(self) -> str:
        products = self.fetch_all()
        if not products:
            return ""
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=list(products[0].keys()))
        writer.writeheader()
        writer.writerows(products)
        return output.getvalue()
