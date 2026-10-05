"""
Composite fraud scoring engine
"""
import uuid
import json
from typing import Dict, Any, List
from database.db_manager import DatabaseManager
from rules.fraud_rules import (
    AmountAnomalyRule,
    VelocityRule,
    ImpossibleTravelRule,
    HighRiskMerchantRule,
    CVVMismatchRule,
    VPNProxyGeoRule
)

class FraudScorer:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.amount_rule = AmountAnomalyRule()
        self.velocity_rule = VelocityRule()
        self.travel_rule = ImpossibleTravelRule()
        self.merchant_rule = HighRiskMerchantRule()
        self.cvv_rule = CVVMismatchRule()
        self.vpn_rule = VPNProxyGeoRule()

    def evaluate_transaction(self, tx_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates a transaction against all 6 fraud rules and computes composite score.
        """
        account_id = tx_dict["account_id"]
        history = self.db.get_recent_transactions(account_id, limit=10)
        last_tx = history[0] if history else None

        triggered_rules = []
        rule_scores = []

        # 1. Amount Rule
        amt_flag, amt_score, amt_msg = self.amount_rule.evaluate(tx_dict)
        if amt_flag:
            triggered_rules.append(amt_msg)
            rule_scores.append(amt_score)

        # 2. Velocity Rule
        vel_flag, vel_score, vel_msg = self.velocity_rule.evaluate(tx_dict, history)
        if vel_flag:
            triggered_rules.append(vel_msg)
            rule_scores.append(vel_score)

        # 3. Impossible Travel Rule
        travel_flag, travel_score, travel_msg = self.travel_rule.evaluate(tx_dict, last_tx)
        if travel_flag:
            triggered_rules.append(travel_msg)
            rule_scores.append(travel_score)

        # 4. High-Risk Merchant Category Rule
        mcc_flag, mcc_score, mcc_msg = self.merchant_rule.evaluate(tx_dict)
        if mcc_flag:
            triggered_rules.append(mcc_msg)
            rule_scores.append(mcc_score)

        # 5. CVV Verification Rule
        cvv_flag, cvv_score, cvv_msg = self.cvv_rule.evaluate(tx_dict)
        if cvv_flag:
            triggered_rules.append(cvv_msg)
            rule_scores.append(cvv_score)

        # 6. VPN / Proxy Geolocation Rule
        vpn_flag, vpn_score, vpn_msg = self.vpn_rule.evaluate(tx_dict)
        if vpn_flag:
            triggered_rules.append(vpn_msg)
            rule_scores.append(vpn_score)

        # Calculate composite score
        if not rule_scores:
            composite_score = 8.0
        else:
            base_score = max(rule_scores)
            compound_bonus = (len(rule_scores) - 1) * 6.0
            composite_score = min(99.0, base_score + compound_bonus)

        # Decision thresholds
        if composite_score >= 80.0:
            decision = "BLOCKED"
        elif composite_score >= 50.0:
            decision = "FLAGGED"
        else:
            decision = "APPROVED"

        # Record in SQLite Database
        self.db.insert_transaction(tx_dict)
        if decision in ("FLAGGED", "BLOCKED"):
            alert_id = f"ALT-{uuid.uuid4().hex[:8].upper()}"
            self.db.record_alert({
                "alert_id": alert_id,
                "transaction_id": tx_dict["transaction_id"],
                "account_id": account_id,
                "risk_score": round(composite_score, 1),
                "triggered_rules": json.dumps(triggered_rules),
                "decision": decision
            })

        return {
            "transaction_id": tx_dict["transaction_id"],
            "account_id": account_id,
            "risk_score": round(composite_score, 1),
            "decision": decision,
            "triggered_rules": triggered_rules
        }
