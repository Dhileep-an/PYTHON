"""
=====================================================================================
 EARTHQUAKE DAMAGE PREDICTION - RANDOM FOREST CLASSIFIER
=====================================================================================
Student Name : Dhileepan Alagiri
Register No  : 44110156
Department   : Computer Science and Engineering (Section A3)
College      : Sathyabama Institute of Science and Technology
Dataset      : ML Olympiad - Predicting Earthquake Damage (Kaggle)
Model        : Random Forest Classifier
=====================================================================================
"""

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
from imblearn.over_sampling import SMOTE

RANDOM_STATE = 42

# STEP 0: LOAD DATA
def load_data(values_path="train_values.csv", labels_path="train_labels.csv"):
    values = pd.read_csv(values_path)
    if "damage_grade" in values.columns:
        df = values.copy()
    else:
        labels = pd.read_csv(labels_path)
        df = values.merge(labels, on="building_id", how="inner")
    return df

# STEP 1: HANDLING MISSING VALUES
def handle_missing_values(df):
    target_col, id_col = "damage_grade", "building_id"
    feature_cols = [c for c in df.columns if c not in (target_col, id_col)]
    
    numeric_cols = [c for c in feature_cols if pd.api.types.is_numeric_dtype(df[c])]
    categorical_cols = [c for c in feature_cols if c not in numeric_cols]

    # Median Imputation for Numeric
    for col in numeric_cols:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].median())

    # Mode Imputation for Categorical
    for col in categorical_cols:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].mode()[0])

    return df, numeric_cols, categorical_cols

# STEP 2: ENCODING CATEGORICAL VARIABLES
def encode_categorical_variables(df, categorical_cols):
    if not categorical_cols:
        return df, []
    df_encoded = pd.get_dummies(df, columns=categorical_cols, prefix=categorical_cols)
    return df_encoded

# STEP 3: HANDLING OUTLIERS
def handle_outliers(df, numeric_cols):
    continuous_cols = [c for c in ["age", "area_percentage", "height_percentage", 
                                   "count_floors_pre_eq", "count_families"] if c in numeric_cols]
    for col in continuous_cols:
        q1, q3 = df[col].quantile(0.25), df[col].quantile(0.75)
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        df[col] = df[col].clip(lower=lower, upper=upper)
    return df

# STEP 4: FEATURE SCALING
def feature_scaling(X_train, X_test, numeric_cols):
    scale_cols = [c for c in ["age", "area_percentage", "height_percentage", 
                              "count_floors_pre_eq", "count_families", 
                              "geo_level_1_id", "geo_level_2_id", "geo_level_3_id"] if c in numeric_cols]
    scaler = StandardScaler()
    X_train = X_train.copy()
    X_test = X_test.copy()
    X_train[scale_cols] = scaler.fit_transform(X_train[scale_cols])
    X_test[scale_cols] = scaler.transform(X_test[scale_cols])
    return X_train, X_test, scaler

# STEP 5: HANDLING IMBALANCED DATASET
def handle_imbalance(X_train, y_train):
    smote = SMOTE(random_state=RANDOM_STATE)
    X_res, y_res = smote.fit_resample(X_train, y_train)
    return X_res, y_res

# MODEL BUILDING & MAIN EXECUTION PIPELINE
def main():
    df = load_data()
    df, numeric_cols, categorical_cols = handle_missing_values(df)
    df = handle_outliers(df, numeric_cols)
    df_encoded = encode_categorical_variables(df, categorical_cols)

    feature_cols = [c for c in df_encoded.columns if c not in ("damage_grade", "building_id")]
    X, y = df_encoded[feature_cols], df_encoded["damage_grade"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )

    X_train, X_test, scaler = feature_scaling(X_train, X_test, numeric_cols)
    X_train_bal, y_train_bal = handle_imbalance(X_train, y_train)

    # Train Random Forest Model
    model = RandomForestClassifier(n_estimators=300, min_samples_leaf=2, random_state=RANDOM_STATE, n_jobs=-1)
    model.fit(X_train_bal, y_train_bal)

    # Evaluation
    y_pred = model.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(f"Weighted F1: {f1_score(y_test, y_pred, average='weighted'):.4f}")
    print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    main()