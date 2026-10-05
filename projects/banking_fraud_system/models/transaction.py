"""
Data models for Banking Fraud Detection System
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Transaction:
    transaction_id: str
    account_id: str
    amount: float
    timestamp: str
    currency: str = "USD"
    mcc: str = "5411: GROCERIES"
    channel: str = "ONLINE"
    device_id: Optional[str] = None
    ip_address: Optional[str] = None
    card_present: bool = False
    cvv_verified: bool = True
    location_lat: Optional[float] = None
    location_lon: Optional[float] = None
    status: str = "COMPLETED"

    def __post_init__(self):
        if self.amount <= 0:
            raise ValueError("Transaction amount must be strictly greater than 0")

@dataclass
class FraudEvaluationResult:
    transaction_id: str
    account_id: str
    risk_score: float
    decision: str  # APPROVED, FLAGGED, BLOCKED
    triggered_rules: list
