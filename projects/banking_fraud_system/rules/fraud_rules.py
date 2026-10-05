"""
Rule algorithms for fraud detection
"""
import math
from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional

class AmountAnomalyRule:
    """Detects transactions exceeding single-transaction limits."""
    def __init__(self, high_risk_threshold: float = 10000.0):
        self.high_risk_threshold = high_risk_threshold

    def evaluate(self, tx_dict: Dict[str, Any]) -> Tuple[bool, float, str]:
        amount = tx_dict.get("amount", 0.0)
        if amount >= self.high_risk_threshold:
            # Score scaled up to 90.0 based on amount
            score = min(90.0, 50.0 + (amount / self.high_risk_threshold) * 20.0)
            return True, score, f"Amount exceeds high-risk threshold of ${self.high_risk_threshold:,.2f}"
        return False, 0.0, ""

class VelocityRule:
    """Detects rapid succession of transactions in a short window."""
    def __init__(self, max_allowed: int = 3, window_minutes: int = 5):
        self.max_allowed = max_allowed
        self.window_minutes = window_minutes

    def evaluate(self, current_tx: Dict[str, Any], history: List[Dict[str, Any]]) -> Tuple[bool, float, str]:
        if not history:
            return False, 0.0, ""
        try:
            cur_time = datetime.fromisoformat(current_tx["timestamp"])
        except ValueError:
            cur_time = datetime.strptime(current_tx["timestamp"], "%Y-%m-%d %H:%M:%S")

        recent_count = 0
        for past in history:
            try:
                past_time = datetime.fromisoformat(past["timestamp"])
            except ValueError:
                past_time = datetime.strptime(past["timestamp"], "%Y-%m-%d %H:%M:%S")
            diff_seconds = abs((cur_time - past_time).total_seconds())
            if diff_seconds <= self.window_minutes * 60:
                recent_count += 1

        if recent_count >= self.max_allowed:
            return True, 75.0, f"Velocity anomaly: {recent_count} transactions in {self.window_minutes} minutes"
        return False, 0.0, ""

class ImpossibleTravelRule:
    """Detects impossible physical travel speed between consecutive transactions."""
    def __init__(self, max_speed_kmh: float = 800.0):
        self.max_speed_kmh = max_speed_kmh

    @staticmethod
    def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        R = 6371.0 # Earth radius in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    def evaluate(self, current_tx: Dict[str, Any], last_tx: Optional[Dict[str, Any]]) -> Tuple[bool, float, str]:
        if not last_tx:
            return False, 0.0, ""
        
        lat1, lon1 = last_tx.get("location_lat"), last_tx.get("location_lon")
        lat2, lon2 = current_tx.get("location_lat"), current_tx.get("location_lon")
        
        if lat1 is None or lon1 is None or lat2 is None or lon2 is None:
            return False, 0.0, ""

        dist_km = self.haversine_km(lat1, lon1, lat2, lon2)
        try:
            t1 = datetime.fromisoformat(last_tx["timestamp"])
            t2 = datetime.fromisoformat(current_tx["timestamp"])
        except ValueError:
            t1 = datetime.strptime(last_tx["timestamp"], "%Y-%m-%d %H:%M:%S")
            t2 = datetime.strptime(current_tx["timestamp"], "%Y-%m-%d %H:%M:%S")

        hours = abs((t2 - t1).total_seconds()) / 3600.0
        if hours < 0.01:
            hours = 0.01

        speed = dist_km / hours
        if speed > self.max_speed_kmh:
            return True, 95.0, f"Impossible Travel ({dist_km:.0f} km in {hours:.1f}h - {speed:.0f} km/h)"
        return False, 0.0, ""

class HighRiskMerchantRule:
    HIGH_RISK_KEYWORDS = ["JEWELRY", "CRYPTO", "CASINO", "BETTING", "7995", "6051"]
    def evaluate(self, tx_dict: Dict[str, Any]) -> Tuple[bool, float, str]:
        mcc = str(tx_dict.get("mcc", "")).upper()
        if any(keyword in mcc for keyword in self.HIGH_RISK_KEYWORDS):
            return True, 70.0, "High-Risk Merchant Category (Jewelry/Crypto)"
        return False, 0.0, ""

class CVVMismatchRule:
    def evaluate(self, tx_dict: Dict[str, Any]) -> Tuple[bool, float, str]:
        if not tx_dict.get("cvv_verified", True):
            return True, 85.0, "CVV Verification Mismatch"
        return False, 0.0, ""

class VPNProxyGeoRule:
    SUSPICIOUS_TAGS = ["VPN", "PROXY", "TOR", "ANONYMOUS"]
    def evaluate(self, tx_dict: Dict[str, Any]) -> Tuple[bool, float, str]:
        ip_info = str(tx_dict.get("ip_address", "")).upper()
        if any(tag in ip_info for tag in self.SUSPICIOUS_TAGS):
            return True, 65.0, "VPN/Proxy Detected on Geolocation"
        return False, 0.0, ""
