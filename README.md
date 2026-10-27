# Smart Garbage Collection Predictor

## Overview
Smart Garbage Collection Predictor is a Python-based decision-support system that analyzes ward-level waste generation, bin availability, and capacity-related data to prioritize garbage collection.

The project uses a weighted risk-scoring approach and a Random Forest classification model to categorize wards into High, Medium, and Low collection priorities.

## Features
- Ward-wise waste data analysis
- Integration of waste, bin, and vehicle datasets
- Garbage collection priority prediction
- Machine learning using Random Forest
- Interactive dashboard built with Streamlit
- Visualization of collection priorities

## Technologies Used
- Python
- Pandas
- Scikit-learn
- Streamlit
- CSV datasets
- Machine Learning

## Project Structure
```text
Smart_Garbage_Project/
├── app.py
├── analyze_data.py
├── check_data.py
├── check_vehicle.py
├── merge_data.py
├── ml_model.py
├── predict_collection.py
├── data/
│   ├── bin_data.csv
│   ├── collection_predictions.csv
│   ├── master_dataset.csv
│   ├── ml_predictions.csv
│   ├── vehicle_data.csv
│   └── waste_data.csv
├── .gitignore
└── README.md
```

## How to Run

### 1. Install dependencies
```bash
pip install pandas scikit-learn streamlit
```

### 2. Run the data preparation script
```bash
python merge_data.py
```

### 3. Generate collection predictions
```bash
python predict_collection.py
```

### 4. Train the machine learning model
```bash
python ml_model.py
```

### 5. Launch the dashboard
```bash
streamlit run app.py
```

Run the scripts from the project directory.

## Project Objective
The objective is to support better waste collection planning by helping identify wards that may require higher collection priority based on the available dataset.

## Disclaimer
This project is an academic prototype. Its predictions depend on the supplied data and scoring methodology and should not be interpreted as verified real-time waste overflow predictions.
