# ================== CAR INSURANCE MANAGEMENT SYSTEM - ENTERPRISE EDITION ==================
from datetime import date
import pandas as pd
import mysql.connector
import streamlit as st

# ================== CONFIGURATION ==================
st.set_page_config(
    page_title="Enterprise Insurance Management | CarIns Pro",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================== PREMIUM CSS STYLING ==================
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    /* Root colors - Premium corporate palette */
    :root {
        --primary: #0066cc;
        --secondary: #00a3e0;
        --accent: #00d4ff;
        --success: #00c853;
        --warning: #ffb300;
        --danger: #ff3b30;
        --dark: #0a0e27;
        --darker: #050812;
        --gray-light: #e8eef7;
        --gray-mid: #64748b;
        --white: #ffffff;
    }

    /* Main container */
    .main {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1629 100%);
        color: #e2e8f0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1629 100%);
    }

    /* Premium Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1427 0%, #1a1f3a 50%, #0f1629 100%);
        border-right: 2px solid #00d4ff;
        box-shadow: inset -10px 0px 30px rgba(0, 212, 255, 0.1);
    }

    .stSidebar {
        background: linear-gradient(180deg, #0d1427 0%, #1a1f3a 50%, #0f1629 100%);
    }

    /* Headers - Premium gradient */
    h1 {
        background: linear-gradient(135deg, #00d4ff 0%, #0099ff 50%, #6633ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem;
        font-weight: 900;
        letter-spacing: -2px;
        margin-bottom: 10px;
        text-shadow: 0 2px 10px rgba(0, 212, 255, 0.2);
    }

    h2 {
        color: #00d4ff;
        font-size: 2rem;
        font-weight: 700;
        border-bottom: 3px solid #0066cc;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }

    h3 {
        color: #00a3e0;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 15px;
    }

    /* Premium Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #0066cc 0%, #00a3e0 50%, #00d4ff 100%);
        color: white !important;
        border: none !important;
        border-radius: 12px;
        padding: 14px 32px !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        box-shadow: 0 8px 24px rgba(0, 102, 204, 0.35);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }

    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s;
    }

    .stButton > button:hover::before {
        left: 100%;
    }

    .stButton > button:hover {
        box-shadow: 0 12px 35px rgba(0, 212, 255, 0.6);
        transform: translateY(-3px);
        background: linear-gradient(135deg, #00a3e0 0%, #00d4ff 50%, #00ffff 100%);
    }

    .stButton > button:active {
        transform: translateY(-1px);
    }

    /* Premium Input Fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stDateInput > div > div > input,
    .stSelectbox > div > div > select {
        background: linear-gradient(135deg, #0d1b2a 0%, #1a2a3a 100%) !important;
        border: 2px solid #00a3e0 !important;
        border-radius: 10px !important;
        padding: 14px 18px !important;
        font-size: 15px !important;
        color: #e2e8f0 !important;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 163, 224, 0.1);
    }

    .stTextInput > div > div > input::placeholder,
    .stNumberInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: #64748b !important;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stDateInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 0 4px rgba(0, 212, 255, 0.25), 0 8px 25px rgba(0, 212, 255, 0.35) !important;
    }

    /* Premium Expanders */
    .streamlit-expanderHeader {
        background: linear-gradient(90deg, #0d1b2a 0%, #1a2a3a 100%);
        border-radius: 10px;
        border-left: 5px solid #00d4ff;
        color: #00d4ff;
        font-weight: 700;
        font-size: 16px;
        padding: 16px 20px !important;
        transition: all 0.3s ease;
    }

    .streamlit-expanderHeader:hover {
        background: linear-gradient(90deg, #1a2a3a 0%, #2a3a4a 100%);
        border-left-color: #00ffff;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
    }

    /* Premium Dataframes */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 8px 30px rgba(0, 212, 255, 0.2);
        border: 2px solid #00a3e0;
        background: linear-gradient(135deg, #0d1b2a 0%, #1a2a3a 100%);
    }

    /* Premium Metrics */
    .stMetric {
        background: linear-gradient(135deg, #0d1b2a 0%, #1a2a3a 100%);
        border-radius: 15px;
        padding: 28px 24px;
        box-shadow: 0 8px 30px rgba(0, 212, 255, 0.2);
        border: 2px solid #00a3e0;
        transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        position: relative;
        overflow: hidden;
    }

    .stMetric::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle, rgba(0, 212, 255, 0.1), transparent);
        transition: all 0.4s ease;
    }

    .stMetric:hover {
        box-shadow: 0 12px 40px rgba(0, 212, 255, 0.4);
        border-color: #00ffff;
        transform: translateY(-8px);
    }

    .stMetricLabel {
        color: #00a3e0;
        font-weight: 700;
        font-size: 14px;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    .stMetricValue {
        color: #00ffff;
        font-size: 3rem !important;
        font-weight: 900;
        text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
    }

    /* Premium Alerts */
    div[data-testid="stAlert"] {
        border-radius: 12px;
        padding: 18px 22px;
        margin: 16px 0;
        border-left: 5px solid;
        backdrop-filter: blur(10px);
        font-weight: 600;
    }

    div[data-testid="stAlert"]:has-text("✅") {
        background: linear-gradient(135deg, rgba(0, 200, 83, 0.15), rgba(0, 150, 50, 0.1));
        border-left-color: #00c853;
        color: #4ade80;
    }

    div[data-testid="stAlert"]:has-text("❌") {
        background: linear-gradient(135deg, rgba(255, 59, 48, 0.15), rgba(255, 0, 0, 0.1));
        border-left-color: #ff3b30;
        color: #ff6b6b;
    }

    div[data-testid="stAlert"]:has-text("⚠️") {
        background: linear-gradient(135deg, rgba(255, 179, 0, 0.15), rgba(255, 140, 0, 0.1));
        border-left-color: #ffb300;
        color: #ffa726;
    }

    div[data-testid="stAlert"]:has-text("📭") {
        background: linear-gradient(135deg, rgba(0, 163, 224, 0.15), rgba(0, 102, 204, 0.1));
        border-left-color: #00a3e0;
        color: #00d4ff;
    }

    /* Premium Divider */
    hr {
        border: none;
        height: 3px;
        background: linear-gradient(90deg, transparent, #00d4ff, #0066cc, transparent);
        margin: 40px 0;
        border-radius: 2px;
    }

    /* Text styling */
    body, p, label, span, div {
        color: #e2e8f0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Links */
    a {
        color: #00d4ff;
        text-decoration: none;
        transition: all 0.3s ease;
    }

    a:hover {
        color: #00ffff;
        text-decoration: underline;
    }

    /* Markdown text */
    .markdown-text-container {
        color: #e2e8f0;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] button {
        color: #64748b;
        background: transparent;
        border-bottom: 3px solid transparent;
        transition: all 0.3s ease;
    }

    .stTabs [data-baseweb="tab-list"] button:hover {
        color: #00d4ff;
        border-bottom-color: #0066cc;
    }

    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #00d4ff;
        border-bottom-color: #00d4ff;
        box-shadow: 0 2px 10px rgba(0, 212, 255, 0.3);
    }

    /* Select dropdown */
    select {
        background: linear-gradient(135deg, #0d1b2a 0%, #1a2a3a 100%) !important;
        color: #ffffff !important;
        border: 2px solid #00a3e0 !important;
    }

    option {
        background: #0a0e27;
        color: #ffffff;
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }

    ::-webkit-scrollbar-track {
        background: #0a0e27;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #00a3e0 0%, #0066cc 100%);
        border-radius: 6px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #00d4ff 0%, #00a3e0 100%);
    }

    /* Label styling */
    label {
        color: #7dd3fc;
        font-weight: 600;
        font-size: 14px;
        letter-spacing: 0.5px;
    }
</style>
""", unsafe_allow_html=True)

# ================== DATABASE CONNECTION ==================
def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Abcdefgh1*",
        database="carinsurancedb",
        autocommit=False
    )

def run_query(query, params=None, fetch=True):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(query, params or ())
        if fetch:
            data = cur.fetchall()
            df = pd.DataFrame(data)
        else:
            conn.commit()
            df = None
        return df
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

# ================== IMPROVED PREMIUM SIDEBAR ==================
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; margin-bottom: 30px; padding: 20px 0;'>
            <h1 style='margin: 0; font-size: 2.8rem;'>🏛️</h1>
            <h2 style='margin: 15px 0 8px 0; font-size: 1.8rem; border: none; color: #00d4ff;'>CarIns Pro</h2>
            <p style='color: #00a3e0; margin: 0; font-size: 0.9rem; letter-spacing: 1px;'>ENTERPRISE INSURANCE MANAGEMENT</p>
            <div style='margin-top: 15px; padding: 10px 0; border-top: 2px solid #00d4ff; border-bottom: 2px solid #00d4ff;'>
                <p style='color: #7dd3fc; margin: 5px 0; font-size: 0.8rem;'>✨ Enterprise Edition v1.0</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 🎯 MODULE SELECTOR")
    selected = st.selectbox(
        "Navigate to module:",
        ["🏠 Dashboard", "👥 Customers", "🚗 Cars", "📋 Policies", "💰 Claims", "💳 Payments", "🧑‍💼 Agents", "🔗 Assignments"],
        key="module_select",
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### 📊 QUICK ACCESS")

    tabs = st.tabs(["👥 Customers", "🚗 Cars", "📋 Policies", "💰 Claims", "💳 Payments", "🧑‍💼 Agents"])

    with tabs[0]:
        try:
            df = run_query("SELECT customerID, name, phone FROM customer ORDER BY customerID DESC LIMIT 5")
            if df is not None and not df.empty:
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("📭 No data")
        except:
            st.error("Error")

    with tabs[1]:
        try:
            df = run_query("SELECT carID, registrationNumber, model FROM car ORDER BY carID DESC LIMIT 5")
            if df is not None and not df.empty:
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("📭 No data")
        except:
            st.error("Error")

    with tabs[2]:
        try:
            df = run_query("SELECT policyID, policyNumber, premiumAmount FROM policy ORDER BY policyID DESC LIMIT 5")
            if df is not None and not df.empty:
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("📭 No data")
        except:
            st.error("Error")

    with tabs[3]:
        try:
            df = run_query("SELECT claimID, claimAmount, status FROM claim ORDER BY claimID DESC LIMIT 5")
            if df is not None and not df.empty:
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("📭 No data")
        except:
            st.error("Error")

    with tabs[4]:
        try:
            df = run_query("SELECT paymentID, amount, modeOfPayment FROM payment ORDER BY paymentID DESC LIMIT 5")
            if df is not None and not df.empty:
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("📭 No data")
        except:
            st.error("Error")

    with tabs[5]:
        try:
            df = run_query("SELECT agentID, name, phone FROM agent ORDER BY agentID DESC LIMIT 5")
            if df is not None and not df.empty:
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("📭 No data")
        except:
            st.error("Error")

    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #00a3e0; font-size: 0.85rem; margin-top: 30px; padding: 15px 0;'>
            <p style='margin: 5px 0; font-size: 0.75rem;'>🔒 Secure Enterprise System</p>
            <p style='margin: 5px 0; font-size: 0.7rem; color: #64748b;'>Powered by CarIns Pro</p>
        </div>
    """, unsafe_allow_html=True)

# ================== DASHBOARD ==================
if selected == "🏠 Dashboard":
    st.title("📊 Executive Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    try:
        cust_count = run_query("SELECT COUNT(*) as count FROM customer")
        car_count = run_query("SELECT COUNT(*) as count FROM car")
        policy_count = run_query("SELECT COUNT(*) as count FROM policy")
        claim_count = run_query("SELECT COUNT(*) as count FROM claim")

        with col1:
            st.metric("👥 Total Customers", cust_count['count'].values[0] if not cust_count.empty else 0)
        with col2:
            st.metric("🚗 Registered Vehicles", car_count['count'].values[0] if not car_count.empty else 0)
        with col3:
            st.metric("📋 Active Policies", policy_count['count'].values[0] if not policy_count.empty else 0)
        with col4:
            st.metric("💰 Claims Processed", claim_count['count'].values[0] if not claim_count.empty else 0)
    except:
        st.error("Could not load metrics")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📍 Recent Customers")
        try:
            df = run_query("SELECT customerID, name, phone FROM customer ORDER BY customerID DESC LIMIT 8")
            if df is not None and not df.empty:
                st.dataframe(df, use_container_width=True, hide_index=True, height=350)
            else:
                st.info("No customers")
        except Exception as e:
            st.error(f"Error: {e}")

    with col2:
        st.subheader("🚗 Recent Cars")
        try:
            df = run_query("SELECT carID, registrationNumber, model FROM car ORDER BY carID DESC LIMIT 8")
            if df is not None and not df.empty:
                st.dataframe(df, use_container_width=True, hide_index=True, height=350)
            else:
                st.info("No cars")
        except Exception as e:
            st.error(f"Error: {e}")

# ================== CUSTOMERS ==================
elif selected == "👥 Customers":
    st.title("👥 Customer Management System")

    tab1, tab2, tab3 = st.tabs(["📋 View All", "➕ Add New", "🔄 Update/Delete"])

    with tab1:
        st.subheader("Customer Database")
        df = run_query("SELECT * FROM customer ORDER BY customerID DESC")
        if df is not None and not df.empty:
            st.dataframe(df, use_container_width=True, height=500)
        else:
            st.info("📭 No customers in database")

    with tab2:
        st.subheader("Add New Customer")
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("👤 Full Name")
            dob = st.date_input("📅 Date of Birth", date(2000, 1, 1))

        with col2:
            phone = st.text_input("📱 Phone Number")
            email = st.text_input("✉️ Email Address")

        address = st.text_area("📍 Address", height=100)

        if st.button("💾 Add Customer", use_container_width=True):
            if not name or not phone or not email:
                st.error("❌ Please fill all required fields")
            else:
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("""
                        INSERT INTO customer (name, DOB, address, phone, email)
                        VALUES (%s,%s,%s,%s,%s)
                    """, (name, dob, address, phone, email))
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success("✅ Customer added successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")

    with tab3:
        st.subheader("Update or Delete Customer")
        cid = st.number_input("Enter Customer ID", min_value=1)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔍 Load Customer", use_container_width=True):
                try:
                    df = run_query("SELECT * FROM customer WHERE customerID=%s", (cid,))
                    if df is not None and not df.empty:
                        st.session_state.customer_data = df.iloc[0].to_dict()
                        st.success(f"✅ Customer {cid} loaded")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

        with col2:
            if st.button("🗑️ Delete Customer", use_container_width=True, help="This action cannot be undone"):
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("DELETE FROM customer WHERE customerID=%s", (cid,))
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.warning(f"⚠️ Customer {cid} deleted")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")

        if 'customer_data' in st.session_state:
            st.markdown("---")
            st.subheader("Edit Customer Details")
            data = st.session_state.customer_data

            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("👤 Full Name", value=data.get('name', ''))
                dob = st.date_input("📅 Date of Birth", value=data.get('DOB', date(2000, 1, 1)))

            with col2:
                phone = st.text_input("📱 Phone", value=data.get('phone', ''))
                email = st.text_input("✉️ Email", value=data.get('email', ''))

            address = st.text_area("📍 Address", value=data.get('address', ''), height=100)

            if st.button("💾 Save Changes", use_container_width=True):
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("""
                        UPDATE customer
                        SET name=%s, DOB=%s, address=%s, phone=%s, email=%s
                        WHERE customerID=%s
                    """, (name, dob, address, phone, email, cid))
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success("✅ Customer updated successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")

# ================== CARS ==================
elif selected == "🚗 Cars":
    st.title("🚗 Vehicle Management System")

    tab1, tab2, tab3 = st.tabs(["📋 View All", "➕ Add New", "🔄 Update/Delete"])

    with tab1:
        st.subheader("Vehicle Database")
        df = run_query("SELECT * FROM car ORDER BY carID DESC")
        if df is not None and not df.empty:
            st.dataframe(df, use_container_width=True, height=500)
        else:
            st.info("📭 No vehicles in database")

    with tab2:
        st.subheader("Register New Vehicle")
        col1, col2 = st.columns(2)

        with col1:
            registration_number = st.text_input("📋 Registration Number")
            model = st.text_input("🏷️ Model")

        with col2:
            manufacturer = st.text_input("🏢 Manufacturer")
            year = st.number_input("📆 Year", min_value=1900, max_value=2030, value=2024)

        customer_id = st.number_input("👤 Customer ID", min_value=1)

        if st.button("💾 Add Vehicle", use_container_width=True):
            if not registration_number or not model or not manufacturer:
                st.error("❌ Please fill all required fields")
            else:
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("""
                        INSERT INTO car (registrationNumber, model, manufacturer, year, customerID)
                        VALUES (%s,%s,%s,%s,%s)
                    """, (registration_number, model, manufacturer, year, customer_id))
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success("✅ Vehicle added successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")

    with tab3:
        st.subheader("Update or Delete Vehicle")
        car_id = st.number_input("Enter Car ID", min_value=1, key="car_id_update")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔍 Load Vehicle", use_container_width=True):
                try:
                    df = run_query("SELECT * FROM car WHERE carID=%s", (car_id,))
                    if df is not None and not df.empty:
                        st.session_state.car_data = df.iloc[0].to_dict()
                        st.success(f"✅ Vehicle {car_id} loaded")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

        with col2:
            if st.button("🗑️ Delete Vehicle", use_container_width=True):
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("DELETE FROM car WHERE carID=%s", (car_id,))
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.warning(f"⚠️ Vehicle {car_id} deleted")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")

        if 'car_data' in st.session_state:
            st.markdown("---")
            st.subheader("Edit Vehicle Details")
            data = st.session_state.car_data

            col1, col2 = st.columns(2)
            with col1:
                registration_number = st.text_input("📋 Registration", value=data.get('registrationNumber', ''))
                model = st.text_input("🏷️ Model", value=data.get('model', ''))

            with col2:
                manufacturer = st.text_input("🏢 Manufacturer", value=data.get('manufacturer', ''))
                year = st.number_input("📆 Year", value=int(data.get('year', 2024)))

            customer_id = st.number_input("👤 Customer ID", value=int(data.get('customerID', 1)))

            if st.button("💾 Save Changes", use_container_width=True, key="save_car"):
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("""
                        UPDATE car
                        SET registrationNumber=%s, model=%s, manufacturer=%s, year=%s, customerID=%s
                        WHERE carID=%s
                    """, (registration_number, model, manufacturer, year, customer_id, car_id))
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success("✅ Vehicle updated successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")

# ================== POLICIES ==================
elif selected == "📋 Policies":
    st.title("📋 Policy Management System")

    tab1, tab2, tab3, tab4 = st.tabs(["📋 View All", "➕ Add New", "🔄 Update/Delete", "🔍 Get Policy Details"])

    with tab1:
        st.subheader("Policy Database")
        df = run_query("SELECT * FROM policy ORDER BY policyID DESC")
        if df is not None and not df.empty:
            st.dataframe(df, use_container_width=True, height=500)
        else:
            st.info("📭 No policies in database")

    with tab2:
        st.subheader("Create New Policy")
        col1, col2 = st.columns(2)

        with col1:
            policy_number = st.number_input("📝 Policy Number", min_value=1)
            start_date = st.date_input("📅 Start Date", date.today())

        with col2:
            end_date = st.date_input("📅 End Date", date(2026, 11, 4))
            premium_amount = st.number_input("💰 Premium Amount", min_value=0.0, step=100.0)

        coverage_details = st.text_input("📋 Coverage Details (e.g., MINIMUM, COMPREHENSIVE)")

        col3, col4 = st.columns(2)
        with col3:
            customer_id = st.number_input("👤 Customer ID", min_value=1, key="pol_cust")
        with col4:
            car_id = st.number_input("🚗 Car ID", min_value=1, key="pol_car")

        if st.button("💾 Create Policy", use_container_width=True):
            if premium_amount <= 0 or not coverage_details:
                st.error("❌ Please fill all required fields")
            else:
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("""
                        INSERT INTO policy (policyNumber, startDate, endDate, premiumAmount, coverageDetails, customerID, carID)
                        VALUES (%s,%s,%s,%s,%s,%s,%s)
                    """, (policy_number, start_date, end_date, premium_amount, coverage_details, customer_id, car_id))
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success("✅ Policy created successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")

    with tab3:
        st.subheader("Update or Delete Policy")
        pol_id = st.number_input("Enter Policy ID", min_value=1, key="pol_id_update")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔍 Load Policy", use_container_width=True):
                try:
                    df = run_query("SELECT * FROM policy WHERE policyID=%s", (pol_id,))
                    if df is not None and not df.empty:
                        st.session_state.policy_data = df.iloc[0].to_dict()
                        st.success(f"✅ Policy {pol_id} loaded")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

        with col2:
            if st.button("🗑️ Delete Policy", use_container_width=True):
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("DELETE FROM policy WHERE policyID=%s", (pol_id,))
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.warning(f"⚠️ Policy {pol_id} deleted")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")

        if 'policy_data' in st.session_state:
            st.markdown("---")
            st.subheader("Edit Policy Details")
            data = st.session_state.policy_data

            col1, col2 = st.columns(2)
            with col1:
                policy_number = st.number_input("📝 Policy Number", value=int(data.get('policyNumber', 1)))
                start_date = st.date_input("📅 Start Date", value=data.get('startDate', date.today()))

            with col2:
                end_date = st.date_input("📅 End Date", value=data.get('endDate', date(2026, 11, 4)))
                premium_amount = st.number_input("💰 Premium", value=float(data.get('premiumAmount', 0)))

            coverage_details = st.text_input("📋 Coverage", value=data.get('coverageDetails', ''))
            customer_id = st.number_input("👤 Customer ID", value=int(data.get('customerID', 1)))
            car_id = st.number_input("🚗 Car ID", value=int(data.get('carID', 1)))

            if st.button("💾 Save Changes", use_container_width=True, key="save_policy"):
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("""
                        UPDATE policy
                        SET policyNumber=%s, startDate=%s, endDate=%s, premiumAmount=%s, coverageDetails=%s, customerID=%s, carID=%s
                        WHERE policyID=%s
                    """, (policy_number, start_date, end_date, premium_amount, coverage_details, customer_id, car_id, pol_id))
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success("✅ Policy updated successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")

    with tab4:
        st.subheader("🔍 Get Policy Details (Stored Procedure)")
        st.markdown("""
        This section calls the **GetPolicyDetails** stored procedure to retrieve comprehensive 
        policy information including customer and car details.
        """)
        
        policy_id_sp = st.number_input("📋 Enter Policy ID", min_value=1, key="sp_policy_id", 
                                       help="Enter the Policy ID to retrieve complete details")
        
        if st.button("🔍 Execute GetPolicyDetails Procedure", use_container_width=True):
            try:
                conn = get_connection()
                cur = conn.cursor(dictionary=True)
                
                # Call the stored procedure
                cur.callproc('GetPolicyDetails', [policy_id_sp])
                
                # Fetch results
                results = []
                for result in cur.stored_results():
                    results = result.fetchall()
                
                cur.close()
                conn.close()
                
                if results:
                    st.success(f"✅ Policy details retrieved successfully!")
                    
                    # Display results in a nice format
                    df = pd.DataFrame(results)
                    
                    # Show as dataframe
                    st.markdown("### 📊 Policy Information")
                    st.dataframe(df, use_container_width=True)
                    
                    # Also show as detailed card
                    if not df.empty:
                        st.markdown("---")
                        st.markdown("### 📝 Detailed View")
                        data = df.iloc[0].to_dict()
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("#### 📋 Policy Information")
                            st.markdown(f"**Policy ID:** {data.get('policyID', 'N/A')}")
                            st.markdown(f"**Policy Number:** {data.get('policyNumber', 'N/A')}")
                            st.markdown(f"**Start Date:** {data.get('startDate', 'N/A')}")
                            st.markdown(f"**End Date:** {data.get('endDate', 'N/A')}")
                            st.markdown(f"**Premium Amount:** ₹{data.get('premiumAmount', 0):,.2f}")
                        
                        with col2:
                            st.markdown("#### 👤 Customer Information")
                            st.markdown(f"**Customer ID:** {data.get('customerID', 'N/A')}")
                            st.markdown(f"**Customer Name:** {data.get('CustomerName', 'N/A')}")
                            st.markdown(f"**Phone:** {data.get('CustomerPhone', 'N/A')}")
                            
                            st.markdown("#### 🚗 Vehicle Information")
                            st.markdown(f"**Car ID:** {data.get('carID', 'N/A')}")
                            st.markdown(f"**Registration:** {data.get('CarReg', 'N/A')}")
                            st.markdown(f"**Manufacturer:** {data.get('CarManufacturer', 'N/A')}")
                            st.markdown(f"**Model:** {data.get('CarModel', 'N/A')}")
                else:
                    st.warning(f"⚠️ No policy found with ID: {policy_id_sp}")
                    
            except Exception as e:
                st.error(f"❌ Error calling stored procedure: {e}")


# ================== CLAIMS ==================
elif selected == "💰 Claims":
    st.title("💰 Claims Management System")

    tab1, tab2, tab3 = st.tabs(["📋 View All", "➕ Add New", "🔄 Update/Delete"])

    with tab1:
        st.subheader("Claims Database")
        df = run_query("SELECT * FROM claim ORDER BY claimID DESC")
        if df is not None and not df.empty:
            st.dataframe(df, use_container_width=True, height=500)
        else:
            st.info("📭 No claims in database")

    with tab2:
        st.subheader("File New Claim")
        col1, col2 = st.columns(2)

        with col1:
            cdate = st.date_input("📅 Claim Date", date.today())
            camount = st.number_input("💰 Claim Amount", min_value=0.0, step=100.0)

        with col2:
            cstatus = st.selectbox("📊 Status", ["Pending", "Approved", "Rejected", "Closed"])
            pid = st.number_input("📋 Policy ID", min_value=1)

        if st.button("💾 File Claim", use_container_width=True):
            if camount <= 0:
                st.error("❌ Claim amount must be greater than 0")
            else:
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("""
                        INSERT INTO claim (claimDate, claimAmount, status, policyID)
                        VALUES (%s,%s,%s,%s)
                    """, (cdate, camount, cstatus, pid))
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success("✅ Claim filed successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")

    with tab3:
        st.subheader("Update or Delete Claim")
        claim_id = st.number_input("Enter Claim ID", min_value=1, key="claim_id_update")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔍 Load Claim", use_container_width=True):
                try:
                    df = run_query("SELECT * FROM claim WHERE claimID=%s", (claim_id,))
                    if df is not None and not df.empty:
                        st.session_state.claim_data = df.iloc[0].to_dict()
                        st.success(f"✅ Claim {claim_id} loaded")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

        with col2:
            if st.button("🗑️ Delete Claim", use_container_width=True):
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("DELETE FROM claim WHERE claimID=%s", (claim_id,))
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.warning(f"⚠️ Claim {claim_id} deleted")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")

        if 'claim_data' in st.session_state:
            st.markdown("---")
            st.subheader("Edit Claim Details")
            data = st.session_state.claim_data

            col1, col2 = st.columns(2)
            with col1:
                cdate = st.date_input("📅 Date", value=data.get('claimDate', date.today()))
                camount = st.number_input("💰 Amount", value=float(data.get('claimAmount', 0)))

            with col2:
                cstatus = st.selectbox("📊 Status", ["Pending", "Approved", "Rejected", "Closed"], 
                                      index=["Pending", "Approved", "Rejected", "Closed"].index(data.get('status', 'Pending')))
                pid = st.number_input("📋 Policy ID", value=int(data.get('policyID', 1)))

            if st.button("💾 Save Changes", use_container_width=True, key="save_claim"):
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("""
                        UPDATE claim
                        SET claimDate=%s, claimAmount=%s, status=%s, policyID=%s
                        WHERE claimID=%s
                    """, (cdate, camount, cstatus, pid, claim_id))
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success("✅ Claim updated successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")

# ================== PAYMENTS ==================
elif selected == "💳 Payments":
    st.title("💳 Payment Management System")

    tab1, tab2, tab3 = st.tabs(["📋 View All", "➕ Add New", "🔄 Update/Delete"])

    with tab1:
        st.subheader("Payment Records")
        df = run_query("SELECT * FROM payment ORDER BY paymentID DESC")
        if df is not None and not df.empty:
            st.dataframe(df, use_container_width=True, height=500)
        else:
            st.info("📭 No payments in database")

    with tab2:
        st.subheader("Record New Payment")
        col1, col2 = st.columns(2)

        with col1:
            pdate = st.date_input("📅 Payment Date", date.today())
            mode = st.selectbox("💳 Payment Method", ["Cash", "Card", "UPI", "Cheque", "NetBanking"])

        with col2:
            amount = st.number_input("💰 Amount", min_value=0.0, step=100.0)
            polid = st.number_input("📋 Policy ID", min_value=1)

        if st.button("💾 Record Payment", use_container_width=True):
            if amount <= 0:
                st.error("❌ Amount must be greater than 0")
            else:
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("""
                        INSERT INTO payment (paymentDate, modeOfPayment, amount, policyID)
                        VALUES (%s,%s,%s,%s)
                    """, (pdate, mode, amount, polid))
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success("✅ Payment recorded successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")

    with tab3:
        st.subheader("Update or Delete Payment")
        pay_id = st.number_input("Enter Payment ID", min_value=1, key="pay_id_update")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔍 Load Payment", use_container_width=True):
                try:
                    df = run_query("SELECT * FROM payment WHERE paymentID=%s", (pay_id,))
                    if df is not None and not df.empty:
                        st.session_state.payment_data = df.iloc[0].to_dict()
                        st.success(f"✅ Payment {pay_id} loaded")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

        with col2:
            if st.button("🗑️ Delete Payment", use_container_width=True):
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("DELETE FROM payment WHERE paymentID=%s", (pay_id,))
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.warning(f"⚠️ Payment {pay_id} deleted")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")

        if 'payment_data' in st.session_state:
            st.markdown("---")
            st.subheader("Edit Payment Details")
            data = st.session_state.payment_data

            col1, col2 = st.columns(2)
            with col1:
                pdate = st.date_input("📅 Date", value=data.get('paymentDate', date.today()))
                mode = st.selectbox("💳 Method", ["Cash", "Card", "UPI", "Cheque", "NetBanking"],
                                   index=["Cash", "Card", "UPI", "Cheque", "NetBanking"].index(data.get('modeOfPayment', 'Cash')))

            with col2:
                amount = st.number_input("💰 Amount", value=float(data.get('amount', 0)))
                polid = st.number_input("📋 Policy ID", value=int(data.get('policyID', 1)))

            if st.button("💾 Save Changes", use_container_width=True, key="save_payment"):
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("""
                        UPDATE payment
                        SET paymentDate=%s, modeOfPayment=%s, amount=%s, policyID=%s
                        WHERE paymentID=%s
                    """, (pdate, mode, amount, polid, pay_id))
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success("✅ Payment updated successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")

# ================== AGENTS ==================
elif selected == "🧑‍💼 Agents":
    st.title("🧑‍💼 Agent Management System")

    tab1, tab2, tab3 = st.tabs(["📋 View All", "➕ Add New", "🔄 Update/Delete"])

    with tab1:
        st.subheader("Agent Directory")
        df = run_query("SELECT * FROM agent ORDER BY agentID DESC")
        if df is not None and not df.empty:
            st.dataframe(df, use_container_width=True, height=500)
        else:
            st.info("📭 No agents in database")

    with tab2:
        st.subheader("Onboard New Agent")
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("👤 Full Name")
            phone = st.text_input("📱 Phone Number")

        with col2:
            email = st.text_input("✉️ Email Address")
            branch = st.text_input("🏢 Branch")

        if st.button("💾 Add Agent", use_container_width=True):
            if not name or not phone or not email:
                st.error("❌ Please fill all required fields")
            else:
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("""
                        INSERT INTO agent (name, phone, email, branch)
                        VALUES (%s,%s,%s,%s)
                    """, (name, phone, email, branch))
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success("✅ Agent added successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")

    with tab3:
        st.subheader("Update or Delete Agent")
        agent_id = st.number_input("Enter Agent ID", min_value=1, key="agent_id_update")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔍 Load Agent", use_container_width=True):
                try:
                    df = run_query("SELECT * FROM agent WHERE agentID=%s", (agent_id,))
                    if df is not None and not df.empty:
                        st.session_state.agent_data = df.iloc[0].to_dict()
                        st.success(f"✅ Agent {agent_id} loaded")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

        with col2:
            if st.button("🗑️ Delete Agent", use_container_width=True):
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("DELETE FROM agent WHERE agentID=%s", (agent_id,))
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.warning(f"⚠️ Agent {agent_id} deleted")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")

        if 'agent_data' in st.session_state:
            st.markdown("---")
            st.subheader("Edit Agent Details")
            data = st.session_state.agent_data

            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("👤 Name", value=data.get('name', ''))
                phone = st.text_input("📱 Phone", value=data.get('phone', ''))

            with col2:
                email = st.text_input("✉️ Email", value=data.get('email', ''))
                branch = st.text_input("🏢 Branch", value=data.get('branch', ''))

            if st.button("💾 Save Changes", use_container_width=True, key="save_agent"):
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("""
                        UPDATE agent SET name=%s, phone=%s, email=%s, branch=%s WHERE agentID=%s
                    """, (name, phone, email, branch, agent_id))
                    conn.commit()
                    cur.close()
                    conn.close()
                    st.success("✅ Agent updated successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")

# ================== ASSIGNMENTS ==================
elif selected == "🔗 Assignments":
    st.title("🔗 Agent-Customer Assignments")

    tab1, tab2, tab3 = st.tabs(["📋 View All", "➕ Assign New", "🔄 Manage"])

    with tab1:
        st.subheader("Assignment Records")
        df = run_query("SELECT * FROM assignedto")
        if df is not None and not df.empty:
            st.dataframe(df, use_container_width=True, height=500)
        else:
            st.info("📭 No assignments in database")

    with tab2:
        st.subheader("Create New Assignment")
        col1, col2 = st.columns(2)

        with col1:
            agent_id = st.number_input("🧑‍💼 Agent ID", min_value=1, key="new_assign_agent")
        with col2:
            customer_id = st.number_input("👤 Customer ID", min_value=1, key="new_assign_cust")

        if st.button("✅ Assign Agent to Customer", use_container_width=True):
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO assignedto (agentID, customerID) VALUES (%s,%s)
                """, (agent_id, customer_id))
                conn.commit()
                cur.close()
                conn.close()
                st.success("✅ Assignment created successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {e}")

    with tab3:
        st.subheader("Manage Assignments")
        col1, col2 = st.columns(2)

        with col1:
            aid = st.number_input("🧑‍💼 Agent ID to remove", min_value=1, key="remove_assign_agent")
        with col2:
            cid = st.number_input("👤 Customer ID to remove", min_value=1, key="remove_assign_cust")

        if st.button("❌ Remove Assignment", use_container_width=True):
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("""
                    DELETE FROM assignedto WHERE agentID=%s AND customerID=%s
                """, (aid, cid))
                conn.commit()
                cur.close()
                conn.close()
                st.warning("⚠️ Assignment removed")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {e}")