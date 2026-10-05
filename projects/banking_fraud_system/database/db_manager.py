"""
Database manager for SQLite operations
"""
import sqlite3
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

class DatabaseManager:
    def __init__(self, db_path: str = "banking_system.db"):
        self.db_path = db_path
        self._init_db()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        schema_path = Path(__file__).resolve().parent / "schema.sql"
        if schema_path.exists():
            with open(schema_path, "r", encoding="utf-8") as f:
                schema_sql = f.read()
            with self.get_connection() as conn:
                conn.executescript(schema_sql)

    def create_account(self, account_id: str, holder_name: str, balance: float = 0.0):
        with self.get_connection() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO accounts (account_id, holder_name, balance) VALUES (?, ?, ?)",
                (account_id, holder_name, balance)
            )

    def insert_transaction(self, tx_dict: Dict[str, Any]):
        with self.get_connection() as conn:
            conn.execute(
                """INSERT INTO transactions 
                   (transaction_id, account_id, amount, currency, timestamp, mcc, channel, device_id, ip_address, card_present, cvv_verified, location_lat, location_lon, status)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    tx_dict["transaction_id"],
                    tx_dict["account_id"],
                    tx_dict["amount"],
                    tx_dict.get("currency", "USD"),
                    tx_dict["timestamp"],
                    tx_dict.get("mcc", "5411: GROCERIES"),
                    tx_dict.get("channel", "ONLINE"),
                    tx_dict.get("device_id", "dev_default"),
                    tx_dict.get("ip_address", "127.0.0.1"),
                    1 if tx_dict.get("card_present", False) else 0,
                    1 if tx_dict.get("cvv_verified", True) else 0,
                    tx_dict.get("location_lat"),
                    tx_dict.get("location_lon"),
                    tx_dict.get("status", "COMPLETED")
                )
            )

    def get_recent_transactions(self, account_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cur = conn.execute(
                "SELECT * FROM transactions WHERE account_id = ? ORDER BY timestamp DESC LIMIT ?",
                (account_id, limit)
            )
            return [dict(row) for row in cur.fetchall()]

    def record_alert(self, alert_dict: Dict[str, Any]):
        with self.get_connection() as conn:
            conn.execute(
                """INSERT INTO fraud_alerts 
                   (alert_id, transaction_id, account_id, risk_score, triggered_rules, decision)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    alert_dict["alert_id"],
                    alert_dict["transaction_id"],
                    alert_dict["account_id"],
                    alert_dict["risk_score"],
                    alert_dict["triggered_rules"],
                    alert_dict["decision"]
                )
            )

    def get_alerts(self, account_id: Optional[str] = None) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            if account_id:
                cur = conn.execute("SELECT * FROM fraud_alerts WHERE account_id = ? ORDER BY created_at DESC", (account_id,))
            else:
                cur = conn.execute("SELECT * FROM fraud_alerts ORDER BY created_at DESC")
            return [dict(row) for row in cur.fetchall()]
