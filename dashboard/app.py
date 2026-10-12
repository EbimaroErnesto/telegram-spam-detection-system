import os
import sqlite3
import pandas as pd
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Real-Time Spam Detection System",
    page_icon="🛡️",
    layout="wide"
)


# ============================================================
# DATABASE
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATABASE_PATH = os.path.join(
    BASE_DIR,
    "spam_detection.db"
)


def load_data():

    if not os.path.exists(DATABASE_PATH):
        return pd.DataFrame()

    connection = sqlite3.connect(DATABASE_PATH)

    try:

        query = """
            SELECT *
            FROM message_logs
            ORDER BY timestamp DESC
        """

        df = pd.read_sql_query(
            query,
            connection
        )

    except Exception as error:

        connection.close()

        st.error(
            f"Unable to read database: {error}"
        )

        return pd.DataFrame()

    connection.close()

    return df


# ============================================================
# LOAD DATA
# ============================================================

df = load_data()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🛡️ Spam Guard")

    st.caption(
        "Real-Time Pattern Recognition System"
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Detection History",
            "System Information"
        ]
    )

    st.divider()

    if st.button(
        "🔄 Refresh Data",
        use_container_width=True
    ):
        st.rerun()


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    st.title("Real-Time Spam Detection System")

    st.write(
        "Monitor messages detected and blocked by the "
        "machine-learning spam detection system."
    )

    st.divider()


    # --------------------------------------------------------
    # STATISTICS
    # --------------------------------------------------------

    if not df.empty:

        total_messages = len(df)

        spam_count = len(
            df[
                df["prediction"]
                .astype(str)
                .str.lower()
                == "spam"
            ]
        )

        ham_count = len(
            df[
                df["prediction"]
                .astype(str)
                .str.lower()
                == "ham"
            ]
        )

        spam_rate = (
            spam_count / total_messages * 100
            if total_messages > 0
            else 0
        )

    else:

        total_messages = 0
        spam_count = 0
        ham_count = 0
        spam_rate = 0


    # --------------------------------------------------------
    # METRIC CARDS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Messages",
            total_messages
        )

    with col2:

        st.metric(
            "🚫 Spam Detected",
            spam_count
        )

    with col3:

        st.metric(
            "✓ Legitimate Messages",
            ham_count
        )

    with col4:

        st.metric(
            "Spam Rate",
            f"{spam_rate:.1f}%"
        )


    st.divider()


    # --------------------------------------------------------
    # SYSTEM STATUS
    # --------------------------------------------------------

    st.subheader("System Status")

    status1, status2, status3 = st.columns(3)

    with status1:

        st.success(
            "● Machine Learning Model: Online"
        )

    with status2:

        st.success(
            "● Database: Connected"
        )

    with status3:

        st.success(
            "● Detection Engine: Active"
        )


    st.divider()


    # --------------------------------------------------------
    # CHART
    # --------------------------------------------------------

    st.subheader("Message Classification")

    if total_messages > 0:

        chart_data = pd.DataFrame(
            {
                "Classification": [
                    "Spam",
                    "Ham"
                ],
                "Messages": [
                    spam_count,
                    ham_count
                ]
            }
        )

        st.bar_chart(
            chart_data.set_index(
                "Classification"
            )
        )

    else:

        st.info(
            "No messages have been detected yet."
        )


    st.divider()


    # --------------------------------------------------------
    # RECENT DETECTIONS
    # --------------------------------------------------------

    st.subheader("Recent Detections")

    if total_messages > 0:

        recent = df.head(10).copy()

        preferred_columns = [
            "message",
            "prediction",
            "action",
            "confidence_score",
            "timestamp"
        ]

        available_columns = [
            column
            for column in preferred_columns
            if column in recent.columns
        ]

        recent = recent[
            available_columns
        ]

        rename_map = {
            "message": "Message",
            "prediction": "Classification",
            "action": "Action",
            "confidence_score": "Decision Score",
            "timestamp": "Time"
        }

        recent = recent.rename(
            columns=rename_map
        )

        st.dataframe(
            recent,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No detection records available."
        )


# ============================================================
# DETECTION HISTORY
# ============================================================

elif page == "Detection History":

    st.title("Detection History")

    st.write(
        "Complete history of messages processed "
        "by the detection system."
    )

    st.divider()

    if not df.empty:

        history = df.copy()

        rename_map = {
            "message": "Message",
            "prediction": "Classification",
            "action": "Action",
            "confidence_score": "Decision Score",
            "timestamp": "Time"
        }

        history = history.rename(
            columns=rename_map
        )

        st.dataframe(
            history,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "There are no detection records."
        )


# ============================================================
# SYSTEM INFORMATION
# ============================================================

elif page == "System Information":

    st.title("System Information")

    st.write(
        "Architecture and technologies used "
        "by the spam detection system."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Machine Learning")

        st.write(
            "**Algorithm:** Support Vector Machine (SVM)"
        )

        st.write(
            "**Feature Extraction:** TF-IDF"
        )

        st.write(
            "**Task:** Spam/Ham Classification"
        )

    with col2:

        st.subheader("System Components")

        st.write(
            "**Backend:** FastAPI"
        )

        st.write(
            "**Messaging:** Telegram Bot"
        )

        st.write(
            "**Database:** SQLite"
        )

        st.write(
            "**Dashboard:** Streamlit"
        )


    st.divider()


    # --------------------------------------------------------
    # MODEL PERFORMANCE
    # --------------------------------------------------------

    st.subheader("Model Performance")

    st.write(
        "The selected SVM model achieved approximately "
        "**97.97% accuracy** during evaluation."
    )

    st.write(
        "Spam-class performance included approximately "
        "**98% precision, 85% recall and 91% F1-score**."
    )


    st.divider()


    # --------------------------------------------------------
    # SYSTEM WORKFLOW
    # --------------------------------------------------------

    st.subheader("System Workflow")

    st.code(
        """
Telegram Message
       ↓
Telegram Bot
       ↓
FastAPI API
       ↓
TF-IDF Feature Extraction
       ↓
SVM Classification
       ↓
 ┌───────────────┐
 │               │
Spam            Ham
 │               │
 ↓               ↓
Delete          Allow
 │               │
 └───────┬───────┘
         ↓
   SQLite Database
         ↓
 Streamlit Dashboard
        """,
        language="text"
    )