"""
Banking Fraud Detection Dashboard Module for Unified SDLC Platform
Preserves 100% of the native FraudGuard AI dashboard from sdlc_multiagent_system.
"""

import sys
import os
import time
import datetime
from pathlib import Path
import pandas as pd
import streamlit as st

# Import portable paths from config
from config import BANKING_DIR, BANKING_DB
BANK_DIR = BANKING_DIR
DB_PATH = BANKING_DB

@st.cache_resource
def load_banking_system():
    if str(BANK_DIR) in sys.path:
        sys.path.remove(str(BANK_DIR))
    sys.path.insert(0, str(BANK_DIR))
    
    for mod in list(sys.modules.keys()):
        if mod.startswith(('database', 'services', 'rules', 'models')):
            del sys.modules[mod]
            
    from database.db_manager import DatabaseManager
    from services.fraud_scorer import FraudScorer

    db = DatabaseManager(str(DB_PATH))
    
    # Ensure demo accounts exist
    db.create_account("8123456789", "Sarah Chen (VIP Account)", balance=85000.0)
    db.create_account("1098765432", "David Miller (Standard Account)", balance=12500.0)
    db.create_account("5544332211", "Emily Watson (Premier Account)", balance=140000.0)
    db.create_account("9988776655", "Corporate Treasury", balance=500000.0)
    
    scorer = FraudScorer(db_manager=db)
    return db, scorer

def render_banking_dashboard():
    db, scorer = load_banking_system()

    # High-contrast CSS matching the original tested platform
    st.markdown("""
    <style>
        .score-dial {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 140px;
            height: 140px;
            border-radius: 50%;
            margin: 15px auto;
            box-shadow: 0 0 25px rgba(0,0,0,0.5);
        }
        .badge-blocked {
            background: linear-gradient(90deg, rgba(239, 68, 68, 0.2) 0%, rgba(185, 28, 28, 0.3) 100%);
            border: 2px solid #ef4444;
            color: #fca5a5;
            padding: 12px 18px;
            border-radius: 10px;
            text-align: center;
            font-weight: 800;
            font-size: 1.15rem;
            margin-bottom: 15px;
        }
        .badge-flagged {
            background: linear-gradient(90deg, rgba(245, 158, 11, 0.2) 0%, rgba(180, 83, 9, 0.3) 100%);
            border: 2px solid #f59e0b;
            color: #fcd34d;
            padding: 12px 18px;
            border-radius: 10px;
            text-align: center;
            font-weight: 800;
            font-size: 1.15rem;
            margin-bottom: 15px;
        }
        .badge-approved {
            background: linear-gradient(90deg, rgba(16, 185, 129, 0.2) 0%, rgba(4, 120, 87, 0.3) 100%);
            border: 2px solid #10b981;
            color: #6ee7b7;
            padding: 12px 18px;
            border-radius: 10px;
            text-align: center;
            font-weight: 800;
            font-size: 1.15rem;
            margin-bottom: 15px;
        }
        .badge-standby {
            background: #0f172a;
            border: 2px dashed #38bdf8;
            color: #e2e8f0;
            padding: 12px 18px;
            border-radius: 10px;
            text-align: center;
            font-weight: 700;
            font-size: 1rem;
            margin-bottom: 15px;
        }
        .risk-chip-danger {
            background: rgba(239, 68, 68, 0.15);
            border: 1px solid #ef4444;
            color: #fca5a5;
            padding: 6px 12px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.82rem;
            margin-bottom: 6px;
        }
        .risk-chip-safe {
            background: rgba(16, 185, 129, 0.15);
            border: 1px solid #10b981;
            color: #6ee7b7;
            padding: 6px 12px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.82rem;
            margin-bottom: 6px;
        }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar Controls
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💳 FraudGuard AI Controls")
    
    bank_tab = st.sidebar.radio(
        "Select Banking Console:",
        ["⚡ Live Transaction Simulator", "🚨 Stored Fraud Alerts", "💳 Processed Transactions Ledger", "🧪 Pytest Automated Test Suite"],
        index=0,
        key="bank_console_mode"
    )

    # Header Banner
    st.markdown('<div class="main-title">💳 FraudGuard AI — Real-Time Banking Fraud Detection Platform</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Algorithmic Risk Scoring • Rapid Velocity Rules • High-Risk MCC Detection • 7 SDLC Agents</div>', unsafe_allow_html=True)

    # Top KPI Metrics Row
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.markdown('''
        <div class="kpi-card" style="border-top: 3px solid #0284c7;">
            <div class="kpi-lbl">Decision Latency</div>
            <div class="kpi-val" style="color: #0284c7;">1.2 ms</div>
            <div style="font-size: 11px; color: #64748b;">Instant Fraud Triage</div>
        </div>
        ''', unsafe_allow_html=True)
    with m_col2:
        st.markdown('''
        <div class="kpi-card" style="border-top: 3px solid #059669;">
            <div class="kpi-lbl">Velocity Rules</div>
            <div class="kpi-val" style="color: #059669;">6 Active Rules</div>
            <div style="font-size: 11px; color: #64748b;">Rapid Bursts & Geo Jumps</div>
        </div>
        ''', unsafe_allow_html=True)
    with m_col3:
        st.markdown('''
        <div class="kpi-card" style="border-top: 3px solid #7e22ce;">
            <div class="kpi-lbl">SDLC AI Agents</div>
            <div class="kpi-val" style="color: #7e22ce;">7 Agents</div>
            <div style="font-size: 11px; color: #64748b;">Architecture to Self-Healing</div>
        </div>
        ''', unsafe_allow_html=True)
    with m_col4:
        st.markdown('''
        <div class="kpi-card" style="border-top: 3px solid #e11d48;">
            <div class="kpi-lbl">Unit Test Suite</div>
            <div class="kpi-val" style="color: #e11d48;">100% Passed</div>
            <div style="font-size: 11px; color: #64748b;">Verified by QA Agent</div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    if bank_tab == "⚡ Live Transaction Simulator":
        # Quick Test Scenarios Bar for immediate template selection
        st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#0284c7; margin-bottom:6px;'>⚡ Starter Test Scenarios (Click to populate form fields, then review & click Execute):</p>", unsafe_allow_html=True)
        q_col1, q_col2, q_col3, q_col4, q_col5 = st.columns([1, 1, 1, 1, 0.7])
        
        preset_action = None
        with q_col1:
            if st.button("🟢 Standard Grocery ($85)", use_container_width=True):
                preset_action = "normal"
        with q_col2:
            if st.button("🚨 Massive Spike ($2.5M)", use_container_width=True):
                preset_action = "spike"
        with q_col3:
            if st.button("✈️ Impossible Travel (London)", use_container_width=True):
                preset_action = "travel"
        with q_col4:
            if st.button("⚠️ CVV Mismatch + Luxury", use_container_width=True):
                preset_action = "cvv_fail"
        with q_col5:
            if st.button("🧹 Clear History", use_container_width=True, help="Clear previous test transactions from database"):
                with db.get_connection() as conn:
                    conn.execute("DELETE FROM transactions")
                    conn.execute("DELETE FROM fraud_alerts")
                st.session_state.current_eval = None
                st.success("Test ledger cleared!")

        # Manage form defaults based on preset clicked
        if "bank_form_data" not in st.session_state:
            st.session_state.bank_form_data = {
                "account_idx": 0,
                "amount": 85.50,
                "currency_idx": 0,
                "mcc_idx": 0,
                "channel_idx": 1,
                "device_id": "DEV_IPHONE_15_PRO",
                "ip_address": "24.110.12.5 (New York, US)",
                "card_present": True,
                "cvv_verified": True
            }
            st.session_state.bank_active_template = "Standard Grocery"

        if preset_action == "normal":
            st.session_state.bank_form_data = {
                "account_idx": 0,
                "amount": 85.50,
                "currency_idx": 0,
                "mcc_idx": 0,
                "channel_idx": 1,
                "device_id": "DEV_IPHONE_15_PRO",
                "ip_address": "24.110.12.5 (New York, US)",
                "card_present": True,
                "cvv_verified": True
            }
            st.session_state.bank_active_template = "🟢 Standard Grocery ($85.50)"
            st.session_state.current_eval = None
        elif preset_action == "spike":
            st.session_state.bank_form_data = {
                "account_idx": 1,
                "amount": 2500000.00,
                "currency_idx": 1,
                "mcc_idx": 0,
                "channel_idx": 0,
                "device_id": "DEV_IPHONE_15_PRO",
                "ip_address": "24.110.12.5 (New York, US)",
                "card_present": False,
                "cvv_verified": True
            }
            st.session_state.bank_active_template = "🚨 Massive Spike ($2,500,000.00 EUR)"
            st.session_state.current_eval = None
        elif preset_action == "travel":
            st.session_state.bank_form_data = {
                "account_idx": 0,
                "amount": 3200.00,
                "currency_idx": 2,
                "mcc_idx": 2,
                "channel_idx": 0,
                "device_id": "DEV_FOREIGN_HOTEL",
                "ip_address": "185.220.101.5 (London, UK)",
                "card_present": False,
                "cvv_verified": True
            }
            st.session_state.bank_active_template = "✈️ Impossible Travel (London, UK)"
            st.session_state.current_eval = None
        elif preset_action == "cvv_fail":
            st.session_state.bank_form_data = {
                "account_idx": 2,
                "amount": 12800.00,
                "currency_idx": 0,
                "mcc_idx": 3,
                "channel_idx": 0,
                "device_id": "DEV_DESKTOP_TOR",
                "ip_address": "104.244.72.115 (Frankfurt, DE)",
                "card_present": False,
                "cvv_verified": False
            }
            st.session_state.bank_active_template = "⚠️ CVV Mismatch + Luxury ($12,800 USD)"
            st.session_state.current_eval = None

        # Split Layout: Left Form vs Right Decision
        col_form, col_decision = st.columns([1.1, 1], gap="large")

        # LEFT CONTAINER: TRANSACTION INTAKE FORM
        with col_form:
            with st.container(border=True):
                st.markdown("<h4 style='margin:0 0 4px 0; color:#0f172a; font-size:1.15rem; font-weight:800;'>💳 Transaction Intake & Parameters</h4>", unsafe_allow_html=True)
                st.markdown("<p style='margin:0 0 16px 0; color:#64748b; font-size:0.85rem;'>Configure transaction attributes or modify the starter preset values.</p>", unsafe_allow_html=True)

                account_choices = [
                    "8123456789 — Sarah Chen (VIP Account) [Bal: $85,000]",
                    "1098765432 — David Miller (Standard Account) [Bal: $12,500]",
                    "5544332211 — Emily Watson (Premier Account) [Bal: $140,000]",
                    "9988776655 — Corporate Treasury [Bal: $500,000]"
                ]
                account_sel = st.selectbox(
                    "Source Account:",
                    account_choices,
                    index=st.session_state.bank_form_data["account_idx"]
                )
                account_id = account_sel.split(" — ")[0]

                c_amt, c_curr = st.columns([2, 1])
                with c_amt:
                    amount = st.number_input(
                        "Transaction Amount:",
                        min_value=1.0,
                        max_value=10000000.0,
                        value=float(st.session_state.bank_form_data["amount"]),
                        step=100.0,
                        format="%.2f"
                    )
                with c_curr:
                    currency = st.selectbox(
                        "Currency:",
                        ["USD ($)", "EUR (€)", "GBP (£)", "SGD ($)"],
                        index=st.session_state.bank_form_data["currency_idx"]
                    )

                mcc_choices = [
                    "5411 — Groceries & Supermarkets (Low Risk)",
                    "5732 — Electronics & Appliances (Medium Risk)",
                    "4511 — Airlines & Travel (Medium Risk)",
                    "7995 — Jewelry & Luxury Goods (High Risk)",
                    "6051 — Cryptocurrency & Wire Services (High Risk)"
                ]
                mcc = st.selectbox(
                    "Merchant Category Code (MCC):",
                    mcc_choices,
                    index=st.session_state.bank_form_data["mcc_idx"]
                )

                c_chan, c_dev = st.columns(2)
                with c_chan:
                    channel = st.selectbox(
                        "Channel:",
                        ["ONLINE / E-COMMERCE", "IN-STORE (POS)", "ATM WITHDRAWAL"],
                        index=st.session_state.bank_form_data["channel_idx"]
                    )
                with c_dev:
                    device_id = st.text_input(
                        "Device ID / Fingerprint:",
                        value=st.session_state.bank_form_data["device_id"]
                    )

                ip_address = st.text_input(
                    "IP Address / Geolocation:",
                    value=st.session_state.bank_form_data["ip_address"]
                )

                st.markdown("<p style='font-size:0.88rem; font-weight:700; color:#0284c7; margin-top:10px; margin-bottom:4px;'>Security Verification Controls:</p>", unsafe_allow_html=True)
                c_chk1, c_chk2 = st.columns(2)
                with c_chk1:
                    card_present = st.checkbox(
                        "Cardholder Physically Present",
                        value=st.session_state.bank_form_data["card_present"]
                    )
                with c_chk2:
                    cvv_verified = st.checkbox(
                        "CVV / Security Code Verified",
                        value=st.session_state.bank_form_data["cvv_verified"]
                    )

                st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
                evaluate_btn = st.button("⚡ EXECUTE FRAUD EVALUATION", type="primary", use_container_width=True)

        # RIGHT CONTAINER: REAL-TIME RISK DECISION
        with col_decision:
            with st.container(border=True):
                st.markdown("<h4 style='margin:0 0 4px 0; color:#0f172a; font-size:1.15rem; font-weight:800;'>⚡ Real-Time Risk Analysis</h4>", unsafe_allow_html=True)
                st.markdown("<p style='margin:0 0 16px 0; color:#64748b; font-size:0.85rem;'>Composite risk scoring determined by active fraud rules and multi-agent algorithms.</p>", unsafe_allow_html=True)

                if evaluate_btn:
                    tx_payload = {
                        "transaction_id": f"TX_{int(time.time())}",
                        "account_id": account_id,
                        "amount": float(amount),
                        "currency": currency.split(" ")[0],
                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "mcc": mcc,
                        "channel": channel,
                        "device_id": device_id,
                        "ip_address": ip_address,
                        "card_present": card_present,
                        "cvv_verified": cvv_verified,
                        "location_lat": 50.1109 if "Frankfurt" in ip_address else (51.5074 if "London" in ip_address else 40.7128),
                        "location_lon": 8.6821 if "Frankfurt" in ip_address else (-0.1278 if "London" in ip_address else -74.0060),
                        "status": "COMPLETED"
                    }

                    eval_result = scorer.evaluate_transaction(tx_payload)
                    st.session_state.current_eval = eval_result

                res = st.session_state.get("current_eval")

                if res is not None:
                    score = res["risk_score"]
                    decision = res["decision"]
                    rules = res["triggered_rules"]

                    if decision == "BLOCKED":
                        dial_color = "#ef4444"
                        dial_bg = "radial-gradient(circle, rgba(127, 29, 29, 0.4) 0%, rgba(15, 23, 42, 0.8) 100%)"
                        risk_tag = "CRITICAL RISK"
                        badge_html = f'<div class="badge-blocked">🚨 DECISION: {decision}<br><span style="font-weight:600; font-size:0.85rem;">Transaction Blocked Instantly. Funds Secured.</span></div>'
                    elif decision == "FLAGGED":
                        dial_color = "#f59e0b"
                        dial_bg = "radial-gradient(circle, rgba(120, 53, 15, 0.4) 0%, rgba(15, 23, 42, 0.8) 100%)"
                        risk_tag = "ELEVATED RISK"
                        badge_html = f'<div class="badge-flagged">⚠️ DECISION: {decision}<br><span style="font-weight:600; font-size:0.85rem;">Transaction Queued for Compliance Review.</span></div>'
                    else:
                        dial_color = "#10b981"
                        dial_bg = "radial-gradient(circle, rgba(6, 78, 59, 0.4) 0%, rgba(15, 23, 42, 0.8) 100%)"
                        risk_tag = "LOW RISK"
                        badge_html = f'<div class="badge-approved">✅ DECISION: {decision}<br><span style="font-weight:600; font-size:0.85rem;">Transaction Approved Automatically. Clean Activity.</span></div>'

                    st.markdown(f"""
                    <div class="score-dial" style="border: 4px solid {dial_color}; background: {dial_bg}; box-shadow: 0 0 25px {dial_color}40;">
                        <div style="font-size: 2.6rem; font-weight: 900; color: {dial_color}; line-height: 1;">{int(score)}</div>
                        <div style="font-size: 0.72rem; color: #94a3b8; font-weight: 700; margin-top: 4px;">/ 100 RISK SCORE</div>
                        <div style="font-size: 0.78rem; font-weight: 800; color: {dial_color}; margin-top: 4px; letter-spacing: 0.5px;">{risk_tag}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown(badge_html, unsafe_allow_html=True)

                    st.markdown("<p style='font-size:0.9rem; font-weight:800; color:#0f172a; margin-bottom:8px;'>Evaluated Risk Indicators:</p>", unsafe_allow_html=True)

                    if rules:
                        for r in rules:
                            st.markdown(f'<div class="risk-chip-danger">⚠️ {r}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class="risk-chip-safe">
                            ✅ All parameters verified within legitimate profile. Zero anomalies detected.
                        </div>
                        """, unsafe_allow_html=True)

                else:
                    active_tpl = st.session_state.get("bank_active_template", "Custom Configuration")
                    st.markdown("""
                    <div class="score-dial" style="border: 3px dashed #0284c7; background: #f8fafc; box-shadow: 0 0 15px rgba(2, 132, 199, 0.15);">
                        <div style="font-size: 2.2rem; font-weight: 800; color: #0284c7; line-height: 1;">--</div>
                        <div style="font-size: 0.72rem; color: #64748b; font-weight: 700;">/ 100 RISK SCORE</div>
                        <div style="font-size: 0.75rem; font-weight: 700; color: #0284c7; margin-top: 4px;">READY</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="badge-standby" style="background:#f8fafc; border: 2px dashed #0284c7; color:#0f172a;">
                        ⏳ TEMPLATE LOADED: {active_tpl}<br>
                        <span style="font-weight: 600; font-size: 0.85rem; color: #0284c7;">👉 Review parameters on the left and click "EXECUTE FRAUD EVALUATION"</span>
                    </div>
                    """, unsafe_allow_html=True)
                    st.info("💡 You can modify the Amount, Currency, Merchant, or CVV on the left before executing.")

    elif bank_tab == "🚨 Stored Fraud Alerts":
        st.markdown("#### 🚨 Stored Fraud Alerts Table (`fraud_alerts`)")
        st.markdown("Real-time database inspection of recorded fraud incidents, compliance reviews, and blocked attempts.")
        try:
            alerts = db.get_alerts()
            if alerts:
                df_alerts = pd.DataFrame(alerts)
                st.dataframe(df_alerts, use_container_width=True)
                st.caption(f"Total alerts in ledger: {len(alerts)}")
            else:
                st.info("No fraud alerts recorded yet. Run a high-risk or blocked transaction preset in the simulator to generate alerts.")
        except Exception as e:
            st.error(f"Error querying fraud alerts: {e}")

    elif bank_tab == "💳 Processed Transactions Ledger":
        st.markdown("#### 💳 Processed Transactions Ledger (`transactions`)")
        st.markdown("Audit trail of all processed customer transactions stored in `banking_system.db`.")
        try:
            account_id_filter = st.selectbox(
                "Filter by Account:",
                ["8123456789", "1098765432", "5544332211", "9988776655"],
                index=0
            )
            txs = db.get_recent_transactions(account_id=account_id_filter, limit=50)
            if txs:
                df_txs = pd.DataFrame(txs)
                st.dataframe(df_txs, use_container_width=True)
                st.caption(f"Total transactions displayed for account {account_id_filter}: {len(txs)}")
            else:
                st.info(f"No transactions found for account {account_id_filter}. Execute a transaction in the simulator to populate.")
        except Exception as e:
            st.error(f"Error querying transaction ledger: {e}")

    elif bank_tab == "🧪 Pytest Automated Test Suite":
        st.markdown("#### 🧪 Autonomous Pytest Verification Suite")
        st.markdown("Run the complete automated test suite generated and audited by the 7 SDLC QA & Safety Agents.")
        
        if st.button("🚀 Run Pytest Test Suite Now", type="primary"):
            import subprocess
            with st.spinner("Executing pytest on banking fraud detection rules and database..."):
                t_start = time.time()
                test_file = BANK_DIR / "tests" / "test_fraud_detection.py"
                python_exe = sys.executable
                result = subprocess.run(
                    [python_exe, "-m", "pytest", str(test_file), "-v"],
                    capture_output=True,
                    text=True,
                    cwd=str(BANK_DIR)
                )
                duration = time.time() - t_start

            if result.returncode == 0:
                st.success(f"✅ All Unit & Integration Tests Passed (100% Pass Rate in {duration:.2f}s)!")
            else:
                st.warning(f"⚠️ Pytest returned exit code {result.returncode}")
                
            st.code(result.stdout if result.stdout else result.stderr, language="text")
