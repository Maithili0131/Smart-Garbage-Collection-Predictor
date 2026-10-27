import pandas as pd

# Load master dataset
file_path = r"C:\Users\madha\OneDrive\Desktop\Smart_Garbage_Project\data\master_dataset.csv"

df = pd.read_csv(file_path)

print("\n========== TOP WARDS BY WASTE PER BIN ==========\n")

top_bins = df[
    [
        "Ward No",
        "Ward name",
        "Waste quantity (Tonnes Per Day)",
        "Bins-No of street bins",
        "Total_Bin_Capacity_Litres",
        "Waste_Per_Bin_TPD"
    ]
].sort_values(
    by="Waste_Per_Bin_TPD",
    ascending=False
)

print(top_bins.to_string(index=False))


print("\n========== TOP WARDS BY TOTAL WASTE ==========\n")

top_waste = df[
    [
        "Ward No",
        "Ward name",
        "Waste quantity (Tonnes Per Day)",
        "Bins-No of street bins",
        "Waste_Per_Bin_TPD"
    ]
].sort_values(
    by="Waste quantity (Tonnes Per Day)",
    ascending=False
)

print(top_waste.to_string(index=False))


print("\n========== TOP WARDS BY BIN CAPACITY PRESSURE ==========\n")

capacity_pressure = df[
    [
        "Ward No",
        "Ward name",
        "Waste quantity (Tonnes Per Day)",
        "Total_Bin_Capacity_Litres",
        "Waste_Per_Bin_TPD"
    ]
].sort_values(
    by="Waste_Per_Bin_TPD",
    ascending=False
)

print(capacity_pressure.head(10).to_string(index=False))