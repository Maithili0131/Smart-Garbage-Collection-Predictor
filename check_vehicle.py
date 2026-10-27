import pandas as pd
import os

project_folder = os.path.dirname(os.path.abspath(__file__))
file = os.path.join(project_folder, "data", "vehicle_data.csv")

df = pd.read_csv(file)

# Remove completely empty columns
df = df.dropna(axis=1, how="all")

print("\n========== VEHICLE DATA CHECK ==========")

print("\nShape:", df.shape)

print("\nVehicle number values:")
print(
    df[
        [
            "Ward No.",
            "Ward name",
            "Collection Vehicle details-Type of Waste collection vehicle",
            "Collection Vehicle details-Capacity (in cubic meters)",
            "Collection Vehicle details-Nos of Vehicle",
            "Collection Vehicle details-Frequency of trips (Daily, Biweekly, Fortnightly, Monthly)"
        ]
    ].head(30).to_string(index=False)
)

print("\n========== DATA TYPES ==========")

print(
    df[
        [
            "Ward No.",
            "Collection Vehicle details-Nos of Vehicle"
        ]
    ].dtypes
)

print("\n========== UNIQUE VEHICLE NUMBER VALUES ==========")

print(
    df["Collection Vehicle details-Nos of Vehicle"]
    .value_counts(dropna=False)
    .head(30)
)

print("\n========== UNIQUE WARD NUMBERS ==========")

print(
    df["Ward No."]
    .value_counts(dropna=False)
    .sort_index()
)