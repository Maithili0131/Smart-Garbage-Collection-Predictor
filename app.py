import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# SMART GARBAGE COLLECTION PREDICTOR
# ============================================================

st.set_page_config(
    page_title="Smart Garbage Collection Predictor",
    page_icon="🗑️",
    layout="wide"
)

# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

file_path = r"C:\Users\madha\OneDrive\Desktop\Smart_Garbage_Project\data\ml_predictions.csv"

df = pd.read_csv(file_path)

# Remove unnecessary index column if present
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]


# ------------------------------------------------------------
# TITLE
# ------------------------------------------------------------

st.title("🗑️ Smart Garbage Collection Predictor")

st.markdown(
    """
    **An intelligent decision-support system for prioritizing garbage collection
    using waste generation, bin availability, bin capacity and machine learning.**
    """
)

st.divider()


# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------

total_wards = len(df)

high_count = len(
    df[df["ML_Predicted_Priority"] == "HIGH"]
)

medium_count = len(
    df[df["ML_Predicted_Priority"] == "MEDIUM"]
)

low_count = len(
    df[df["ML_Predicted_Priority"] == "LOW"]
)


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Wards",
        total_wards
    )

with col2:
    st.metric(
        "🔴 High Priority",
        high_count
    )

with col3:
    st.metric(
        "🟠 Medium Priority",
        medium_count
    )

with col4:
    st.metric(
        "🟢 Low Priority",
        low_count
    )


st.divider()


# ------------------------------------------------------------
# WARD SELECTION
# ------------------------------------------------------------

st.subheader("🔎 Check Collection Priority")

ward_options = df["Ward name"].tolist()

selected_ward = st.selectbox(
    "Select a Ward",
    ward_options
)

ward = df[
    df["Ward name"] == selected_ward
].iloc[0]


# ------------------------------------------------------------
# WARD DETAILS
# ------------------------------------------------------------

st.subheader("Ward Analysis")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Ward Number",
        int(ward["Ward No"])
    )

with col2:
    st.metric(
        "Waste Generation",
        f"{ward['Waste quantity (Tonnes Per Day)']:.2f} TPD"
    )

with col3:
    st.metric(
        "Number of Bins",
        int(ward["Bins-No of street bins"])
    )

with col4:
    st.metric(
        "Waste per Bin",
        f"{ward['Waste_Per_Bin_TPD']:.3f}"
    )


# ------------------------------------------------------------
# PRIORITY
# ------------------------------------------------------------

priority = ward["ML_Predicted_Priority"]

st.subheader("Collection Priority")

if priority == "HIGH":

    st.error(
        "🔴 HIGH PRIORITY — Schedule garbage collection immediately."
    )

elif priority == "MEDIUM":

    st.warning(
        "🟠 MEDIUM PRIORITY — Schedule garbage collection soon."
    )

else:

    st.success(
        "🟢 LOW PRIORITY — Normal monitoring is sufficient."
    )


# ------------------------------------------------------------
# RISK SCORE
# ------------------------------------------------------------

st.metric(
    "Collection Risk Score",
    f"{ward['Collection_Risk_Percent']:.2f}%"
)


st.divider()


# ------------------------------------------------------------
# TOP PRIORITY WARDS
# ------------------------------------------------------------

st.subheader("🚨 Highest Collection Priority Areas")

top_wards = df.sort_values(
    by="Collection_Risk_Percent",
    ascending=False
).head(10)

chart_data = top_wards[
    [
        "Ward name",
        "Collection_Risk_Percent"
    ]
].copy()

chart_data = chart_data.set_index(
    "Ward name"
)

st.bar_chart(
    chart_data
)


# ------------------------------------------------------------
# TOP 10 TABLE
# ------------------------------------------------------------

st.subheader("Top 10 Collection Priority Wards")

display_columns = [
    "Ward No",
    "Ward name",
    "Waste quantity (Tonnes Per Day)",
    "Bins-No of street bins",
    "Waste_Per_Bin_TPD",
    "Collection_Risk_Percent",
    "ML_Predicted_Priority"
]

st.dataframe(
    top_wards[display_columns],
    use_container_width=True,
    hide_index=True
)


st.divider()


# ------------------------------------------------------------
# ALL WARDS
# ------------------------------------------------------------

st.subheader("📊 Complete Collection Priority Table")

all_columns = [
    "Ward No",
    "Ward name",
    "Waste quantity (Tonnes Per Day)",
    "Bins-No of street bins",
    "Total_Bin_Capacity_Litres",
    "Waste_Per_Bin_TPD",
    "Collection_Risk_Percent",
    "ML_Predicted_Priority"
]

st.dataframe(
    df.sort_values(
        by="Collection_Risk_Percent",
        ascending=False
    )[all_columns],
    use_container_width=True,
    hide_index=True
)


# ------------------------------------------------------------
# MUNICIPAL ALERT
# ------------------------------------------------------------

st.divider()

st.subheader("📢 Municipal Collection Alerts")

high_priority = df[
    df["ML_Predicted_Priority"] == "HIGH"
].sort_values(
    by="Collection_Risk_Percent",
    ascending=False
)

if len(high_priority) > 0:

    for _, row in high_priority.iterrows():

        st.error(
            f"⚠️ Ward {int(row['Ward No'])} - "
            f"{row['Ward name']} | "
            f"Risk: {row['Collection_Risk_Percent']:.2f}% | "
            f"Schedule garbage collection immediately."
        )

else:

    st.success(
        "No high-priority collection alerts."
    )


# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------

st.divider()

st.caption(
    "Smart Garbage Collection Predictor | "
    "Machine Learning Based Decision-Support System"
)