import pandas as pd
import os

# Get the folder where this Python file is located
project_folder = os.path.dirname(os.path.abspath(__file__))

# File paths
waste_file = os.path.join(project_folder, "data", "waste_data.csv")
vehicle_file = os.path.join(project_folder, "data", "vehicle_data.csv")
bin_file = os.path.join(project_folder, "data", "bin_data.csv")

# Check whether files exist
print("Checking files...\n")

print("Waste file:", waste_file)
print("Exists:", os.path.exists(waste_file))

print("\nVehicle file:", vehicle_file)
print("Exists:", os.path.exists(vehicle_file))

print("\nBin file:", bin_file)
print("Exists:", os.path.exists(bin_file))

# Read CSV files
waste_df = pd.read_csv(waste_file)
vehicle_df = pd.read_csv(vehicle_file)
bin_df = pd.read_csv(bin_file)

print("\n========== WASTE DATA ==========")
print("Shape:", waste_df.shape)
print("Columns:")
print(waste_df.columns.tolist())

print("\nFirst 5 rows:")
print(waste_df.head())

print("\n========== VEHICLE DATA ==========")
print("Shape:", vehicle_df.shape)
print("Columns:")
print(vehicle_df.columns.tolist())

print("\nFirst 5 rows:")
print(vehicle_df.head())

print("\n========== BIN DATA ==========")
print("Shape:", bin_df.shape)
print("Columns:")
print(bin_df.columns.tolist())

print("\nFirst 5 rows:")
print(bin_df.head())