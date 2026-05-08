# =========================================================
# AI JOB ALERT PLATFORM
# MODERN + ERROR FREE STREAMLIT UI
# =========================================================

import streamlit as st
import sqlite3
import pandas as pd
from datetime import time, datetime
import re

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Job Alert Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# DATABASE
# =========================================================

DB_PATH = "platform.db"

# =========================================================
# DATABASE INITIALIZATION
# =========================================================

def init_db():

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        categories TEXT,
        delivery_time TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

init_db()

# =========================================================
# DATABASE FUNCTIONS
# =========================================================

def add_user(email, categories, delivery_time):

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    try:

        c.execute("""
        INSERT OR REPLACE INTO users
        (email, categories, delivery_time)
        VALUES (?, ?, ?)
        """, (
            email,
            ", ".join(categories),
            delivery_time
        ))

        conn.commit()

        return True

    except Exception as e:

        st.error(f"Database Error: {e}")

        return False

    finally:

        conn.close()


def get_all_users():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        email,
        categories,
        delivery_time
    FROM users
    ORDER BY created_at DESC
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


# =========================================================
# EMAIL VALIDATION
# =========================================================

def validate_email(email):

    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    return re.match(pattern, email)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* ===================================================== */
/* GLOBAL */
/* ===================================================== */

html, body, [class*="css"] {

    font-family: 'Segoe UI', sans-serif;

    color: white;
}

/* ===================================================== */
/* MAIN BACKGROUND */
/* ===================================================== */

.stApp {

    background:
    radial-gradient(circle at top left,
    rgba(14,165,233,0.15),
    transparent 25%),

    radial-gradient(circle at bottom right,
    rgba(37,99,235,0.18),
    transparent 30%),

    linear-gradient(
    135deg,
    #020617 0%,
    #021126 45%,
    #031933 100%
    );

    background-attachment: fixed;
}

/* ===================================================== */
/* ANIMATED GLOW */
/* ===================================================== */

.stApp::before {

    content: "";

    position: fixed;

    width: 700px;
    height: 700px;

    top: -200px;
    left: -200px;

    background:
    radial-gradient(circle,
    rgba(56,189,248,0.12),
    transparent 70%);

    animation: pulseGlow 10s infinite alternate;

    z-index: 0;
}

@keyframes pulseGlow {

    0% {
        transform: scale(1) translate(0px,0px);
    }

    100% {
        transform: scale(1.3) translate(120px,90px);
    }
}

/* ===================================================== */
/* REMOVE STREAMLIT DEFAULTS */
/* ===================================================== */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* ===================================================== */
/* HERO SECTION */
/* ===================================================== */

.hero-container {

    text-align: center;

    padding-top: 40px;
    padding-bottom: 20px;
}

.hero-badge {

    display: inline-block;

    padding: 10px 22px;

    border-radius: 999px;

    background:
    rgba(56,189,248,0.12);

    border:
    1px solid rgba(56,189,248,0.25);

    color: #7dd3fc;

    font-size: 14px;

    margin-bottom: 25px;
}

.hero-title {

    font-size: 72px;

    font-weight: 800;

    line-height: 1.1;

    color: white;

    margin-bottom: 15px;
}

.hero-highlight {

    color: #38bdf8;
}

.hero-subtitle {

    font-size: 24px;

    color: #cbd5e1;

    margin-bottom: 50px;
}

/* ===================================================== */
/* GLASS CARDS */
/* ===================================================== */

.glass-card {

    background:
    rgba(15,23,42,0.72);

    border:
    1px solid rgba(255,255,255,0.08);

    border-radius: 24px;

    padding: 32px;

    backdrop-filter: blur(12px);

    box-shadow:
    0 8px 32px rgba(0,0,0,0.35);

    transition: 0.3s ease;

    height: 100%;
}

.glass-card:hover {

    transform: translateY(-4px);

    border:
    1px solid rgba(56,189,248,0.25);
}

/* ===================================================== */
/* METRICS */
/* ===================================================== */

.metric-title {

    color: #94a3b8;

    font-size: 18px;

    margin-bottom: 15px;

    text-align: center;
}

.metric-value {

    color: white;

    font-size: 44px;

    font-weight: 800;

    text-align: center;
}

/* ===================================================== */
/* SECTION SPACING */
/* ===================================================== */

.section-gap {

    margin-top: 35px;
}

/* ===================================================== */
/* INPUTS */
/* ===================================================== */

.stTextInput input,
.stTimeInput input,
.stMultiSelect div {

    background:
    rgba(15,23,42,0.92) !important;

    border:
    1px solid rgba(255,255,255,0.08) !important;

    border-radius: 14px !important;

    color: white !important;

    padding: 12px !important;
}

/* ===================================================== */
/* BUTTONS */
/* ===================================================== */

.stButton > button {

    width: 100%;

    background:
    linear-gradient(
    90deg,
    #0ea5e9,
    #2563eb
    );

    color: white;

    border: none;

    border-radius: 14px;

    padding: 16px;

    font-size: 18px;

    font-weight: 700;

    transition: 0.3s ease;
}

.stButton > button:hover {

    transform: scale(1.02);

    background:
    linear-gradient(
    90deg,
    #38bdf8,
    #2563eb
    );
}

/* ===================================================== */
/* CLOCK DISPLAY */
/* ===================================================== */

.clock-card {

    background:
    rgba(15,23,42,0.85);

    border:
    1px solid rgba(255,255,255,0.08);

    border-radius: 20px;

    padding: 25px;

    text-align: center;

    margin-top: 15px;

    margin-bottom: 20px;
}

.clock-time {

    font-size: 46px;

    font-weight: 800;

    color: #38bdf8;
}

.clock-sub {

    color: #94a3b8;

    font-size: 14px;

    margin-top: 8px;
}

/* ===================================================== */
/* DATAFRAME */
/* ===================================================== */

[data-testid="stDataFrame"] {

    border-radius: 18px;

    overflow: hidden;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HERO SECTION
# =========================================================

st.markdown("""
<div class="hero-container">

<div class="hero-badge">
⚡ Smart AI Automation Platform
</div>

<div class="hero-title">
AI-Powered
<span class="hero-highlight">
Job Alert
</span>
Platform
</div>

<div class="hero-subtitle">
Daily fresher jobs, internships, and research opportunities delivered automatically.
</div>

</div>
""", unsafe_allow_html=True)

# =========================================================
# USERS
# =========================================================

users_df = get_all_users()

total_users = len(users_df)

# =========================================================
# METRIC CARD FUNCTION
# =========================================================

def metric_card(title, value):

    st.markdown(
        f"""
        <div class="glass-card">

            <div class="metric-title">
                {title}
            </div>

            <div class="metric-value">
                {value}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# METRIC CARDS
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:
    metric_card("Registered Users", total_users)

with col2:
    metric_card("Scheduler Status", "Active")

with col3:
    metric_card("Active Sources", "3")

# =========================================================
# FORM SECTION
# =========================================================

st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="glass-card">

<h1 style="
font-size:48px;
margin-bottom:25px;
">
📬 Register For Daily Alerts
</h1>

</div>
""", unsafe_allow_html=True)

# =========================================================
# EMAIL INPUT
# =========================================================

email = st.text_input(
    "Email Address",
    placeholder="Enter your email address"
)

# =========================================================
# TIME PICKER
# =========================================================

st.markdown("## ⏰ Select Delivery Time")

selected_time = st.time_input(
    "Choose preferred alert time",
    value=time(21, 0)
)

formatted_time = selected_time.strftime("%I:%M %p")

# =========================================================
# DYNAMIC CLOCK DISPLAY
# =========================================================

st.markdown(
    f"""
    <div class="clock-card">

        <div class="clock-time">
            {formatted_time}
        </div>

        <div class="clock-sub">
            Daily Job Alert Delivery Time
        </div>

    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# CATEGORIES
# =========================================================

categories = st.multiselect(
    "Select Categories",
    [
        "BTech Jobs",
        "MTech Jobs",
        "Life Science Jobs",
        "MS Research Internships"
    ]
)

# =========================================================
# REGISTER BUTTON
# =========================================================

if st.button("🚀 Activate Daily Alerts"):

    if not email:

        st.error("Please enter email address")

    elif not validate_email(email):

        st.error("Please enter valid email address")

    elif not categories:

        st.error("Please select at least one category")

    else:

        success = add_user(
            email,
            categories,
            formatted_time
        )

        if success:

            st.success(
                "Daily alerts activated successfully!"
            )

            st.rerun()

# =========================================================
# USERS TABLE
# =========================================================

st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)

st.markdown("## 👥 Registered Users")

updated_df = get_all_users()

if len(updated_df) > 0:

    st.dataframe(
        updated_df,
        use_container_width=True
    )

else:

    st.info("No registered users yet.")

# =========================================================
# SECURITY INFO
# =========================================================

st.markdown("""
<div style="
margin-top:30px;
padding:18px;
border-radius:16px;
background:rgba(15,23,42,0.75);
border:1px solid rgba(255,255,255,0.08);
color:#94a3b8;
text-align:center;
">

🔒 Public users cannot access Azure admin controls or backend infrastructure.

</div>
""", unsafe_allow_html=True)