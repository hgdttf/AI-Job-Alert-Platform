import sys
import os
import re

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import streamlit as st
import pandas as pd

from database.db import cursor, conn
from backend.scheduler import scheduler


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI Job Alert Platform",
    page_icon="📧",
    layout="wide"
)


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown(
    """
    <style>

    /* ==============================
       MAIN BACKGROUND
    ============================== */

    .stApp {
        background-color: #0E1117;
        color: white;
    }

    /* ==============================
       MAIN TITLE
    ============================== */

    .main-title {
        font-size: 42px;
        font-weight: bold;
        color: #4CAF50;
        margin-bottom: 5px;
    }

    /* ==============================
       SUBTEXT
    ============================== */

    .sub-text {
        font-size: 18px;
        color: #B0B0B0;
        margin-bottom: 20px;
    }

    /* ==============================
       SIDEBAR
    ============================== */

    section[data-testid="stSidebar"] {
        background-color: #161B22;
    }

    /* ==============================
       BUTTONS
    ============================== */

    div.stButton > button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 18px;
        font-weight: bold;
    }

    div.stButton > button:hover {
        background-color: #45A049;
        color: white;
    }

    /* ==============================
       FORM BUTTON
    ============================== */

    div.stForm button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        border: none;
        font-weight: bold;
    }

    /* ==============================
       METRIC CARDS
    ============================== */

    div[data-testid="metric-container"] {
        background-color: #161B22;
        border-radius: 12px;
        padding: 15px;
        border: 1px solid #262730;
    }

    /* ==============================
       DATAFRAME
    ============================== */

    div[data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
    }

    /* ==============================
       INPUT BOXES
    ============================== */

    input, textarea {
        border-radius: 8px !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# EMAIL VALIDATION FUNCTION
# ==========================================

def is_valid_email(email):

    pattern = (
        r"^[a-zA-Z0-9_.+-]+"
        r"@[a-zA-Z0-9-]+"
        r"\.[a-zA-Z0-9-.]+$"
    )

    return re.match(
        pattern,
        email
    ) is not None


# ==========================================
# HEADER
# ==========================================

st.markdown(
    """
    <div class="main-title">
    AI-Powered Job Alert Platform
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="sub-text">
    Automated daily fresher jobs,
    internships, and research opportunities
    delivered every 24 hours.
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()


# ==========================================
# LOAD USERS
# ==========================================

try:

    users_df = pd.read_sql_query(
        """
        SELECT * FROM users
        """,
        conn
    )

except Exception:

    users_df = pd.DataFrame()


# ==========================================
# DASHBOARD METRICS
# ==========================================

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Registered Users",
        len(users_df)
    )

with col2:

    st.metric(
        "Scheduler Status",
        "Active"
    )

with col3:

    st.metric(
        "Sources",
        "LinkedIn + Internshala + GitHub"
    )

st.divider()


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title(
    "Platform Status"
)

st.sidebar.success(
    "Scheduler Running"
)

st.sidebar.info(
    "Emails are sent every 24 hours"
)

st.sidebar.markdown(
    "### Active Sources"
)

st.sidebar.write(
    "• LinkedIn"
)

st.sidebar.write(
    "• Internshala"
)

st.sidebar.write(
    "• GitHub Internship Repo"
)

st.sidebar.divider()

st.sidebar.caption(
    "AI Automated Job Aggregation System"
)


# ==========================================
# REGISTRATION FORM
# ==========================================

st.subheader(
    "Register for Daily Alerts"
)

with st.form("job_form"):

    col1, col2 = st.columns(2)

    with col1:

        email = st.text_input(
            "Email Address"
        )

    with col2:

        send_time = st.time_input(
            "Daily Delivery Time"
        )

    st.markdown(
        "### Select Categories"
    )

    col3, col4 = st.columns(2)

    with col3:

        btech = st.checkbox(
            "BTech Jobs"
        )

        mtech = st.checkbox(
            "MTech Jobs"
        )

    with col4:

        life_science = st.checkbox(
            "Life Science Jobs"
        )

        ms_research = st.checkbox(
            "MS Research Internships"
        )

    submitted = st.form_submit_button(
        "Start Daily Alerts"
    )

    if submitted:

        try:

            # ==============================
            # EMAIL VALIDATION
            # ==============================

            if not is_valid_email(email):

                st.error(
                    "Please enter a valid email address."
                )

            # ==============================
            # CATEGORY VALIDATION
            # ==============================

            elif not (
                btech
                or mtech
                or life_science
                or ms_research
            ):

                st.error(
                    "Please select at least one category."
                )

            else:

                # ==========================
                # CHECK DUPLICATE USER
                # ==========================

                cursor.execute(
                    """
                    SELECT * FROM users
                    WHERE email=?
                    """,
                    (email,)
                )

                existing_user = (
                    cursor.fetchone()
                )

                if existing_user:

                    st.warning(
                        "This email is already registered."
                    )

                else:

                    # ======================
                    # INSERT USER
                    # ======================

                    cursor.execute(
                        """
                        INSERT INTO users (
                            email,
                            send_time,
                            btech,
                            mtech,
                            life_science,
                            ms_research
                        )
                        VALUES (?, ?, ?, ?, ?, ?)
                        """,
                        (
                            email,
                            send_time.strftime(
                                "%H:%M:%S"
                            ),
                            int(btech),
                            int(mtech),
                            int(life_science),
                            int(ms_research)
                        )
                    )

                    conn.commit()

                    st.success(
                        """
                        Daily alerts activated successfully.

                        You will now receive:
                        • fresher jobs
                        • internships
                        • research opportunities

                        every 24 hours
                        at your selected time.
                        """
                    )

        except Exception as e:

            st.error(
                f"Registration error: {e}"
            )

st.divider()


# ==========================================
# REGISTERED USERS TABLE
# ==========================================

st.subheader(
    "Registered Users"
)

try:

    users_table = pd.read_sql_query(
        """
        SELECT
            email,
            send_time
        FROM users
        """,
        conn
    )

    st.dataframe(
        users_table,
        width="stretch"
    )

except Exception as e:

    st.error(
        f"Database display error: {e}"
    )

st.divider()


# ==========================================
# REMOVE USER ALERTS
# ==========================================

st.subheader(
    "Remove User Alerts"
)

try:

    cursor.execute(
        "SELECT email FROM users"
    )

    emails = [
        row[0]
        for row in cursor.fetchall()
    ]

    if emails:

        selected_email = st.selectbox(
            "Select User",
            emails
        )

        if st.button(
            "Remove Alerts"
        ):

            try:

                cursor.execute(
                    """
                    DELETE FROM users
                    WHERE email=?
                    """,
                    (selected_email,)
                )

                conn.commit()

                st.success(
                    f"Removed alerts for "
                    f"{selected_email}"
                )

                st.rerun()

            except Exception as e:

                st.error(
                    f"Delete error: {e}"
                )

    else:

        st.info(
            "No registered users found."
        )

except Exception as e:

    st.error(
        f"User management error: {e}"
    )

st.divider()


# ==========================================
# FOOTER
# ==========================================

st.caption(
    """
    AI-Powered Automated Job Aggregation Platform
    | Built with Streamlit, APScheduler,
    SQLite, and Python
    """
)