import pandas as pd
import os

# ============================================================
# 1. FILE PATHS
# ============================================================

project_folder = os.path.dirname(os.path.abspath(__file__))
data_folder = os.path.join(project_folder, "data")

waste_file = os.path.join(data_folder, "waste_data.csv")
vehicle_file = os.path.join(data_folder, "vehicle_data.csv")
bin_file = os.path.join(data_folder, "bin_data.csv")

# ============================================================
# 2. READ DATASETS
# ============================================================

waste_df = pd.read_csv(waste_file)
vehicle_df = pd.read_csv(vehicle_file)
bin_df = pd.read_csv(bin_file)

print("All datasets loaded successfully.")

# ============================================================
# 3. CLEAN VEHICLE DATA
# ============================================================

# Remove completely empty columns
vehicle_df = vehicle_df.dropna(axis=1, how="all")

# Fill ward name downward only
vehicle_df["Ward name"] = vehicle_df["Ward name"].ffill()

# Convert vehicle count to numeric
vehicle_df["Collection Vehicle details-Nos of Vehicle"] = pd.to_numeric(
    vehicle_df["Collection Vehicle details-Nos of Vehicle"],
    errors="coerce"
)

# Convert Ward No to string for cleaning
vehicle_df["Ward No."] = (
    vehicle_df["Ward No."]
    .astype(str)
    .str.strip()
)

# ============================================================
# 4. REMOVE COMBINED WARD RECORD
# ============================================================

vehicle_df = vehicle_df[
    ~vehicle_df["Ward No."].str.contains(
        "42\\(",
        na=False
    )
].copy()

# Keep only proper numeric ward numbers
vehicle_df["Ward_No_Clean"] = pd.to_numeric(
    vehicle_df["Ward No."],
    errors="coerce"
)

vehicle_df = vehicle_df[
    vehicle_df["Ward_No_Clean"].notna()
].copy()

vehicle_df["Ward_No_Clean"] = (
    vehicle_df["Ward_No_Clean"].astype(int)
)

# ============================================================
# 5. VEHICLE SUMMARY
# ============================================================

# Get the first non-empty vehicle count for each ward
vehicle_summary = (
    vehicle_df
    .groupby("Ward_No_Clean")
    .agg(
        Ward_name=("Ward name", "first"),
        Total_Vehicles=(
            "Collection Vehicle details-Nos of Vehicle",
            "first"
        )
    )
    .reset_index()
)

# Replace missing vehicle count with 0
vehicle_summary["Total_Vehicles"] = (
    vehicle_summary["Total_Vehicles"]
    .fillna(0)
)

print("\n========== VEHICLE SUMMARY ==========")
print(
    vehicle_summary.to_string(index=False)
)

# ============================================================
# 6. CLEAN BIN DATA
# ============================================================

bin_df["Ward No"] = pd.to_numeric(
    bin_df["Ward No"],
    errors="coerce"
)

bin_df["Bins-No of street bins"] = pd.to_numeric(
    bin_df["Bins-No of street bins"],
    errors="coerce"
).fillna(0)

bin_df["Bins-Size of street bins (in litres)"] = pd.to_numeric(
    bin_df["Bins-Size of street bins (in litres)"],
    errors="coerce"
).fillna(0)

bin_summary = bin_df[
    [
        "Ward No",
        "Ward name",
        "Bins-Street sweeping waste (TPD)",
        "Bins-Size of street bins (in litres)",
        "Bins-No of street bins"
    ]
].copy()

# ============================================================
# 7. CLEAN WASTE DATA
# ============================================================

waste_df["Number of HH"] = pd.to_numeric(
    waste_df["Number of HH"],
    errors="coerce"
)

waste_df["Waste quantity (Tonnes Per Day)"] = pd.to_numeric(
    waste_df["Waste quantity (Tonnes Per Day)"],
    errors="coerce"
)

waste_df["No. of Households with waste segregation"] = pd.to_numeric(
    waste_df["No. of Households with waste segregation"],
    errors="coerce"
)

# ============================================================
# 8. MAP WASTE WARDS TO WARD NUMBERS
# ============================================================

ward_mapping = dict(
    zip(
        bin_summary["Ward name"]
        .astype(str)
        .str.strip()
        .str.lower(),

        bin_summary["Ward No"]
    )
)

waste_df["ward_key"] = (
    waste_df["Ward name"]
    .astype(str)
    .str.strip()
    .str.lower()
)

waste_df["Ward No"] = waste_df["ward_key"].map(
    ward_mapping
)

# ============================================================
# 9. REMOVE COMBINED WASTE RECORD
# ============================================================

unmatched = waste_df[
    waste_df["Ward No"].isna()
]

if len(unmatched) > 0:

    print("\n========== EXCLUDED WASTE RECORD ==========")

    print(
        unmatched[
            [
                "Ward name",
                "Waste quantity (Tonnes Per Day)"
            ]
        ].to_string(index=False)
    )

    waste_df = waste_df[
        waste_df["Ward No"].notna()
    ].copy()

# Convert ward number to integer
waste_df["Ward No"] = (
    waste_df["Ward No"].astype(int)
)

# ============================================================
# 10. MERGE BIN + WASTE
# ============================================================

master_df = pd.merge(
    bin_summary,
    waste_df[
        [
            "Ward No",
            "Number of HH",
            "Waste quantity (Tonnes Per Day)",
            "No. of Households with waste segregation"
        ]
    ],
    on="Ward No",
    how="inner"
)

print("\nRows after Bin + Waste merge:", len(master_df))

# ============================================================
# 11. MERGE VEHICLE DATA
# ============================================================

master_df = pd.merge(
    master_df,
    vehicle_summary[
        [
            "Ward_No_Clean",
            "Total_Vehicles"
        ]
    ],
    left_on="Ward No",
    right_on="Ward_No_Clean",
    how="left"
)

master_df.drop(
    columns=["Ward_No_Clean"],
    inplace=True
)

# Missing vehicle counts
master_df["Total_Vehicles"] = (
    master_df["Total_Vehicles"]
    .fillna(0)
)

# ============================================================
# 12. FEATURE ENGINEERING
# ============================================================

# Total street-bin capacity
master_df["Total_Bin_Capacity_Litres"] = (
    master_df["Bins-No of street bins"]
    *
    master_df["Bins-Size of street bins (in litres)"]
)

# Waste per bin
master_df["Waste_Per_Bin_TPD"] = (
    master_df["Waste quantity (Tonnes Per Day)"]
    /
    master_df["Bins-No of street bins"].replace(0, pd.NA)
)

# Waste per household
master_df["Waste_Per_Household_TPD"] = (
    master_df["Waste quantity (Tonnes Per Day)"]
    /
    master_df["Number of HH"].replace(0, pd.NA)
)

# Segregation percentage
master_df["Segregation_Rate_Percent"] = (
    master_df["No. of Households with waste segregation"]
    /
    master_df["Number of HH"].replace(0, pd.NA)
) * 100

# Waste per vehicle
master_df["Waste_Per_Vehicle_TPD"] = (
    master_df["Waste quantity (Tonnes Per Day)"]
    /
    master_df["Total_Vehicles"].replace(0, pd.NA)
)

# ============================================================
# 13. ROUND NUMERIC VALUES
# ============================================================

numeric_columns = master_df.select_dtypes(
    include=["float64", "float32"]
).columns

master_df[numeric_columns] = (
    master_df[numeric_columns].round(3)
)

# ============================================================
# 14. SAVE MASTER DATASET
# ============================================================

output_file = os.path.join(
    data_folder,
    "master_dataset.csv"
)

master_df.to_csv(
    output_file,
    index=False
)

# ============================================================
# 15. FINAL CHECK
# ============================================================

print("\n==========================================")
print("MASTER DATASET CREATED SUCCESSFULLY")
print("==========================================")

print("\nFinal shape:", master_df.shape)

print("\nNumber of unique wards:",
      master_df["Ward No"].nunique())

print("\nVehicle values:")
print(
    master_df[
        ["Ward No", "Ward name", "Total_Vehicles"]
    ].to_string(index=False)
)

print("\nMissing values:")
print(
    master_df.isnull().sum()
)

print("\nSaved at:")
print(output_file)