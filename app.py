import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Project Status Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize data storage directory
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
DATA_FILE = DATA_DIR / "project_data.csv"

# Custom CSS for better styling
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""",
    unsafe_allow_html=True,
)


# Helper functions
def load_data():
    """Load data from CSV file"""
    if DATA_FILE.exists():
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame()


def save_data(df):
    """Save data to CSV file"""
    df.to_csv(DATA_FILE, index=False)
    return True


def upload_excel_file():
    """Handle Excel file upload"""
    uploaded_file = st.file_uploader(
        "Upload Excel File",
        type=["xlsx", "xls"],
        help="Upload your project status Excel file",
    )

    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            st.success(f"✅ File uploaded successfully! {len(df)} rows loaded.")
            return df
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
            return None
    return None


# Sidebar navigation
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio(
    "Go to", ["📤 Upload Data", "✏️ Edit Data", "📈 Dashboard", "📋 View All Data"]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 **Tip**: Start by uploading your Excel file in the Upload Data section."
)

# ==================== PAGE: UPLOAD DATA ====================
if page == "📤 Upload Data":
    st.markdown(
        '<div class="main-header">📤 Upload Project Data</div>', unsafe_allow_html=True
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        st.write("### Upload Excel File")
        df_uploaded = upload_excel_file()

        if df_uploaded is not None:
            st.write("### Preview of Uploaded Data")
            st.dataframe(df_uploaded, use_container_width=True)

            col_a, col_b = st.columns(2)
            with col_a:
                if st.button(
                    "💾 Save to Database", type="primary", use_container_width=True
                ):
                    save_data(df_uploaded)
                    st.success("✅ Data saved successfully!")
                    st.balloons()

            with col_b:
                if st.button("➕ Append to Existing Data", use_container_width=True):
                    existing_df = load_data()
                    if not existing_df.empty:
                        combined_df = pd.concat(
                            [existing_df, df_uploaded], ignore_index=True
                        )
                        save_data(combined_df)
                        st.success(f"✅ Data appended! Total rows: {len(combined_df)}")
                    else:
                        save_data(df_uploaded)
                        st.success("✅ Data saved as new database!")

    with col2:
        st.write("### Current Database Info")
        current_df = load_data()
        if not current_df.empty:
            st.metric("Total Records", len(current_df))
            st.metric("Columns", len(current_df.columns))
            st.write("**Columns:**")
            for col in current_df.columns:
                st.write(f"- {col}")
        else:
            st.info("No data in database yet.")

# ==================== PAGE: EDIT DATA ====================
elif page == "✏️ Edit Data":
    st.markdown(
        '<div class="main-header">✏️ Edit Project Data</div>', unsafe_allow_html=True
    )

    df = load_data()

    if df.empty:
        st.warning("⚠️ No data found. Please upload data first.")
    else:
        st.write(f"### Editing {len(df)} records")

        # Data editor with add/delete functionality
        edited_df = st.data_editor(
            df, num_rows="dynamic", use_container_width=True, key="data_editor"
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("💾 Save Changes", type="primary", use_container_width=True):
                save_data(edited_df)
                st.success("✅ Changes saved successfully!")
                st.rerun()

        with col2:
            if st.button("🔄 Reload Data", use_container_width=True):
                st.rerun()

        with col3:
            if st.button("🗑️ Clear All Data", use_container_width=True):
                if st.session_state.get("confirm_delete", False):
                    DATA_FILE.unlink()
                    st.success("✅ All data deleted!")
                    st.session_state["confirm_delete"] = False
                    st.rerun()
                else:
                    st.session_state["confirm_delete"] = True
                    st.warning("⚠️ Click again to confirm deletion!")

# ==================== PAGE: DASHBOARD ====================
elif page == "📈 Dashboard":
    st.markdown(
        '<div class="main-header">📈 Management Dashboard</div>', unsafe_allow_html=True
    )

    df = load_data()

    if df.empty:
        st.warning("⚠️ No data available. Please upload data first.")
    else:
        # Automatically detect status/progress columns
        status_col = None
        for col in df.columns:
            if any(
                keyword in col.lower()
                for keyword in ["status", "state", "progress", "stage"]
            ):
                status_col = col
                break

        # Key Metrics Row
        st.write("### 📊 Key Metrics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Records", len(df))

        with col2:
            if status_col:
                completed = len(
                    df[
                        df[status_col]
                        .astype(str)
                        .str.contains("complete|done|finished", case=False, na=False)
                    ]
                )
                st.metric("Completed", completed)
            else:
                st.metric("Columns", len(df.columns))

        with col3:
            if status_col:
                in_progress = len(
                    df[
                        df[status_col]
                        .astype(str)
                        .str.contains("progress|ongoing|active", case=False, na=False)
                    ]
                )
                st.metric("In Progress", in_progress)
            else:
                st.metric(
                    "Numeric Columns", len(df.select_dtypes(include=["number"]).columns)
                )

        with col4:
            if status_col:
                pending = len(
                    df[
                        df[status_col]
                        .astype(str)
                        .str.contains("pending|not started|new", case=False, na=False)
                    ]
                )
                st.metric("Pending", pending)
            else:
                st.metric(
                    "Text Columns", len(df.select_dtypes(include=["object"]).columns)
                )

        st.markdown("---")

        # Charts Row
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.write("### 📊 Status Distribution")
            if status_col:
                status_counts = df[status_col].value_counts()
                fig1 = px.pie(
                    values=status_counts.values,
                    names=status_counts.index,
                    title=f"Distribution by {status_col}",
                    hole=0.4,
                )
                st.plotly_chart(fig1, use_container_width=True)
            else:
                # Show column types distribution
                col_types = df.dtypes.value_counts()
                fig1 = px.bar(
                    x=col_types.index.astype(str),
                    y=col_types.values,
                    title="Column Types Distribution",
                )
                st.plotly_chart(fig1, use_container_width=True)

        with chart_col2:
            st.write("### 📈 Trends Over Time")
            # Try to find date column
            date_col = None
            for col in df.columns:
                if any(
                    keyword in col.lower()
                    for keyword in ["date", "time", "created", "updated"]
                ):
                    date_col = col
                    break

            if date_col and status_col:
                try:
                    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
                    trend_df = (
                        df.groupby([date_col, status_col])
                        .size()
                        .reset_index(name="count")
                    )
                    fig2 = px.line(
                        trend_df,
                        x=date_col,
                        y="count",
                        color=status_col,
                        title=f"Trends by {status_col}",
                    )
                    st.plotly_chart(fig2, use_container_width=True)
                except:
                    st.info(
                        "Could not create trend chart. Date column format may need adjustment."
                    )
            else:
                # Show numeric column distribution
                numeric_cols = df.select_dtypes(include=["number"]).columns
                if len(numeric_cols) > 0:
                    selected_col = st.selectbox(
                        "Select column to visualize", numeric_cols
                    )
                    fig2 = px.histogram(
                        df, x=selected_col, title=f"Distribution of {selected_col}"
                    )
                    st.plotly_chart(fig2, use_container_width=True)
                else:
                    st.info("No numeric columns found for visualization.")

        # Additional Analysis
        st.markdown("---")
        st.write("### 📋 Detailed Breakdown")

        # Allow filtering
        filter_col1, filter_col2 = st.columns(2)

        with filter_col1:
            if status_col:
                status_filter = st.multiselect(
                    f"Filter by {status_col}",
                    options=df[status_col].unique(),
                    default=df[status_col].unique(),
                )
                filtered_df = df[df[status_col].isin(status_filter)]
            else:
                filtered_df = df

        with filter_col2:
            st.metric("Filtered Records", len(filtered_df))

        st.dataframe(filtered_df, use_container_width=True)

        # Export filtered data
        if st.button("📥 Download Filtered Data as Excel"):
            output_file = (
                DATA_DIR
                / f"filtered_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            )
            filtered_df.to_excel(output_file, index=False)
            st.success(f"✅ Data exported to {output_file}")

# ==================== PAGE: VIEW ALL DATA ====================
elif page == "📋 View All Data":
    st.markdown(
        '<div class="main-header">📋 View All Data</div>', unsafe_allow_html=True
    )

    df = load_data()

    if df.empty:
        st.warning("⚠️ No data found. Please upload data first.")
    else:
        st.write(f"### Total Records: {len(df)}")

        # Column selection
        all_columns = df.columns.tolist()
        selected_columns = st.multiselect(
            "Select columns to display", options=all_columns, default=all_columns
        )

        if selected_columns:
            display_df = df[selected_columns]
        else:
            display_df = df

        # Search functionality
        search_term = st.text_input("🔍 Search in data", "")
        if search_term:
            mask = (
                display_df.astype(str)
                .apply(lambda x: x.str.contains(search_term, case=False, na=False))
                .any(axis=1)
            )
            display_df = display_df[mask]
            st.info(f"Found {len(display_df)} matching records")

        # Display data
        st.dataframe(display_df, use_container_width=True, height=600)

        # Summary statistics
        with st.expander("📊 View Summary Statistics"):
            st.write(df.describe(include="all"))

        # Data info
        with st.expander("ℹ️ Data Information"):
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Column Names and Types:**")
                for col in df.columns:
                    st.write(f"- {col}: {df[col].dtype}")
            with col2:
                st.write("**Missing Values:**")
                missing = df.isnull().sum()
                for col, count in missing.items():
                    if count > 0:
                        st.write(f"- {col}: {count} ({count/len(df)*100:.1f}%)")
                if missing.sum() == 0:
                    st.write("No missing values! ✅")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### 📝 About")
st.sidebar.info(
    """
**Project Status Dashboard**

Upload, edit, and visualize your project data with ease.

Features:
- Excel file upload
- Interactive data editing
- Real-time dashboard
- Data persistence
"""
)
