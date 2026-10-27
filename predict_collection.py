import pandas as pd

# ============================================================
# SMART GARBAGE COLLECTION PREDICTOR
# Pune Municipal Wards
# ============================================================

# Load master dataset
file_path = r"C:\Users\madha\OneDrive\Desktop\Smart_Garbage_Project\data\master_dataset.csv"

df = pd.read_csv(file_path)

print("\n==============================================")
print(" SMART GARBAGE COLLECTION PREDICTOR - PUNE")
print("==============================================\n")


# ------------------------------------------------------------
# 1. NORMALIZE FEATURES
# ------------------------------------------------------------

# Waste per bin
df["Waste_Per_Bin_Score"] = (
    df["Waste_Per_Bin_TPD"] /
    df["Waste_Per_Bin_TPD"].max()
)

# Total waste
df["Total_Waste_Score"] = (
    df["Waste quantity (Tonnes Per Day)"] /
    df["Waste quantity (Tonnes Per Day)"].max()
)

# Bin capacity pressure
# Lower total capacity with higher waste means higher pressure
df["Capacity_Pressure_Score"] = (
    df["Waste quantity (Tonnes Per Day)"] /
    df["Total_Bin_Capacity_Litres"]
)

df["Capacity_Pressure_Score"] = (
    df["Capacity_Pressure_Score"] /
    df["Capacity_Pressure_Score"].max()
)


# ------------------------------------------------------------
# 2. CALCULATE COLLECTION RISK SCORE
# ------------------------------------------------------------

df["Collection_Risk_Score"] = (
    0.50 * df["Waste_Per_Bin_Score"]
    + 0.30 * df["Total_Waste_Score"]
    + 0.20 * df["Capacity_Pressure_Score"]
)


# Convert to percentage
df["Collection_Risk_Percent"] = (
    df["Collection_Risk_Score"] * 100
).round(2)


# ------------------------------------------------------------
# 3. CLASSIFY COLLECTION PRIORITY
# ------------------------------------------------------------

def classify_risk(score):

    if score >= 0.60:
        return "HIGH"

    elif score >= 0.35:
        return "MEDIUM"

    else:
        return "LOW"


df["Collection_Priority"] = (
    df["Collection_Risk_Score"]
    .apply(classify_risk)
)


# ------------------------------------------------------------
# 4. SORT BY PRIORITY
# ------------------------------------------------------------

df = df.sort_values(
    by="Collection_Risk_Score",
    ascending=False
)


# ------------------------------------------------------------
# 5. DISPLAY RESULTS
# ------------------------------------------------------------

result_columns = [
    "Ward No",
    "Ward name",
    "Waste quantity (Tonnes Per Day)",
    "Bins-No of street bins",
    "Waste_Per_Bin_TPD",
    "Collection_Risk_Percent",
    "Collection_Priority"
]

print("========== COLLECTION PRIORITY ==========\n")

print(
    df[result_columns].to_string(index=False)
)


# ------------------------------------------------------------
# 6. SUMMARY
# ------------------------------------------------------------

print("\n==============================================")
print(" COLLECTION PRIORITY SUMMARY")
print("==============================================")

print(
    "\nHIGH PRIORITY:",
    len(df[df["Collection_Priority"] == "HIGH"])
)

print(
    "MEDIUM PRIORITY:",
    len(df[df["Collection_Priority"] == "MEDIUM"])
)

print(
    "LOW PRIORITY:",
    len(df[df["Collection_Priority"] == "LOW"])
)


# ------------------------------------------------------------
# 7. MUNICIPAL ALERTS
# ------------------------------------------------------------

print("\n==============================================")
print(" MUNICIPAL COLLECTION ALERTS")
print("==============================================\n")

high_priority = df[
    df["Collection_Priority"] == "HIGH"
]

for _, row in high_priority.iterrows():

    print(
        f"ALERT: Ward {int(row['Ward No'])} - "
        f"{row['Ward name']} -> HIGH PRIORITY. "
        f"Schedule garbage collection."
    )


# ------------------------------------------------------------
# 8. SAVE PREDICTION DATASET
# ------------------------------------------------------------

output_file = r"C:\Users\madha\OneDrive\Desktop\Smart_Garbage_Project\data\collection_predictions.csv"

df.to_csv(output_file, index=False)

print("\n==============================================")
print("Prediction dataset saved successfully.")
print("==============================================")

print(output_file)