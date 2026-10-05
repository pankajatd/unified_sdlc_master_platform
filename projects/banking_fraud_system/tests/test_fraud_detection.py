"""
Comprehensive Pytest Test Suite for Banking Fraud Detection System
"""
import pytest
import os
import tempfile
from database.db_manager import DatabaseManager
from services.fraud_scorer import FraudScorer
from models.transaction import Transaction

@pytest.fixture
def setup_scorer():
    fd, temp_db = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    db = DatabaseManager(db_path=temp_db)
    db.create_account("ACC_101", "Alice Wonderland", balance=50000.0)
    scorer = FraudScorer(db_manager=db)
    yield scorer, db
    try:
        if os.path.exists(temp_db):
            os.remove(temp_db)
    except OSError:
        pass

def test_normal_transaction_approved(setup_scorer):
    scorer, _ = setup_scorer
    tx = {
        "transaction_id": "TX_001",
        "account_id": "ACC_101",
        "amount": 150.0,
        "currency": "USD",
        "timestamp": "2026-09-30 10:00:00",
        "location_lat": 40.7128,
        "location_lon": -74.0060,
        "status": "COMPLETED"
    }
    result = scorer.evaluate_transaction(tx)
    assert result["decision"] == "APPROVED"
    assert result["risk_score"] < 50.0
    assert len(result["triggered_rules"]) == 0

def test_high_amount_triggers_anomaly(setup_scorer):
    scorer, _ = setup_scorer
    tx = {
        "transaction_id": "TX_002",
        "account_id": "ACC_101",
        "amount": 25000.0,
        "currency": "USD",
        "timestamp": "2026-09-30 10:05:00",
        "location_lat": 40.7128,
        "location_lon": -74.0060,
        "status": "COMPLETED"
    }
    result = scorer.evaluate_transaction(tx)
    assert result["risk_score"] >= 70.0
    assert any("Amount exceeds high-risk threshold" in r for r in result["triggered_rules"])

def test_velocity_anomaly_detection(setup_scorer):
    scorer, _ = setup_scorer
    # Insert 3 transactions rapidly
    for i in range(3):
        scorer.evaluate_transaction({
            "transaction_id": f"TX_VEL_{i}",
            "account_id": "ACC_101",
            "amount": 200.0,
            "currency": "USD",
            "timestamp": f"2026-09-30 10:0{i}:00",
            "location_lat": 40.7128,
            "location_lon": -74.0060,
            "status": "COMPLETED"
        })
    # 4th transaction within the 5 min window should trigger velocity rule
    tx4 = {
        "transaction_id": "TX_VEL_4",
        "account_id": "ACC_101",
        "amount": 200.0,
        "currency": "USD",
        "timestamp": "2026-09-30 10:04:00",
        "location_lat": 40.7128,
        "location_lon": -74.0060,
        "status": "COMPLETED"
    }
    result = scorer.evaluate_transaction(tx4)
    assert any("Velocity anomaly" in r for r in result["triggered_rules"])
    assert result["risk_score"] >= 75.0

def test_impossible_travel_triggers_block(setup_scorer):
    scorer, _ = setup_scorer
    # Transaction 1: New York at 12:00:00
    scorer.evaluate_transaction({
        "transaction_id": "TX_GEO_1",
        "account_id": "ACC_101",
        "amount": 50.0,
        "currency": "USD",
        "timestamp": "2026-09-30 12:00:00",
        "location_lat": 40.7128, # New York
        "location_lon": -74.0060,
        "status": "COMPLETED"
    })
    # Transaction 2: London (5570 km away) only 10 minutes later!
    tx_london = {
        "transaction_id": "TX_GEO_2",
        "account_id": "ACC_101",
        "amount": 50.0,
        "currency": "USD",
        "timestamp": "2026-09-30 12:10:00",
        "location_lat": 51.5074, # London
        "location_lon": -0.1278,
        "status": "COMPLETED"
    }
    result = scorer.evaluate_transaction(tx_london)
    assert result["decision"] == "BLOCKED"
    assert result["risk_score"] >= 80.0
    assert any("impossible travel" in r.lower() for r in result["triggered_rules"])

def test_invalid_transaction_amount_raises_error():
    with pytest.raises(ValueError):
        Transaction(
            transaction_id="TX_ERR",
            account_id="ACC_101",
            amount=-100.0,
            timestamp="2026-09-30 10:00:00"
        )
