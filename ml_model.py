import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# ============================================================
# RANDOM FOREST COLLECTION PRIORITY PREDICTION
# ============================================================

file_path = r"C:\Users\madha\OneDrive\Desktop\Smart_Garbage_Project\data\collection_predictions.csv"

df = pd.read_csv(file_path)

print("\n==============================================")
print(" RANDOM FOREST COLLECTION PRIORITY MODEL")
print("==============================================\n")


# ------------------------------------------------------------
# 1. FEATURES
# ------------------------------------------------------------

features = [
    "Waste quantity (Tonnes Per Day)",
    "Bins-No of street bins",
    "Total_Bin_Capacity_Litres",
    "Waste_Per_Bin_TPD",
    "Waste_Per_Household_TPD",
    "Segregation_Rate_Percent"
]

X = df[features]

y = df["Collection_Priority"]


# ------------------------------------------------------------
# 2. TRAIN / TEST SPLIT
# ------------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)


print("Training records:", len(X_train))
print("Testing records :", len(X_test))


# ------------------------------------------------------------
# 3. RANDOM FOREST MODEL
# ------------------------------------------------------------

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    max_depth=5
)

model.fit(X_train, y_train)


# ------------------------------------------------------------
# 4. PREDICTION
# ------------------------------------------------------------

y_pred = model.predict(X_test)


# ------------------------------------------------------------
# 5. MODEL ACCURACY
# ------------------------------------------------------------

accuracy = accuracy_score(y_test, y_pred)

print("\n==============================================")
print(" MODEL PERFORMANCE")
print("==============================================")

print(f"\nAccuracy: {accuracy * 100:.2f}%")


print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)


# ------------------------------------------------------------
# 6. CONFUSION MATRIX
# ------------------------------------------------------------

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# ------------------------------------------------------------
# 7. FEATURE IMPORTANCE
# ------------------------------------------------------------

importance = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

print("\n==============================================")
print(" FEATURE IMPORTANCE")
print("==============================================\n")

print(importance.to_string(index=False))


# ------------------------------------------------------------
# 8. PREDICT ALL WARDS
# ------------------------------------------------------------

df["ML_Predicted_Priority"] = model.predict(X)


# ------------------------------------------------------------
# 9. SAVE ML RESULTS
# ------------------------------------------------------------

output_file = r"C:\Users\madha\OneDrive\Desktop\Smart_Garbage_Project\data\ml_predictions.csv"

df.to_csv(
    output_file,
    index=False
)


print("\n==============================================")
print(" ML PREDICTIONS")
print("==============================================\n")

print(
    df[
        [
            "Ward No",
            "Ward name",
            "Collection_Priority",
            "ML_Predicted_Priority"
        ]
    ].to_string(index=False)
)


print("\n==============================================")
print(" ML MODEL COMPLETED")
print("==============================================")

print("\nResults saved to:")
print(output_file)