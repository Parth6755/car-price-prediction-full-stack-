from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "cardekho_data (1).csv"
MODEL_PATH = BASE_DIR / "random_forest_model.pkl"
COLS_PATH = BASE_DIR / "feature_columns.pkl"


def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Training dataset not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)
    required = {
        "Car_Name", "Year", "Selling_Price", "Present_Price",
        "Kms_Driven", "Fuel_Type", "Seller_Type", "Transmission", "Owner",
    }
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")

    X = df.drop("Selling_Price", axis=1)
    y = df["Selling_Price"]

    categorical_cols = ["Fuel_Type", "Seller_Type", "Transmission", "Owner", "Car_Name"]
    X_encoded = pd.get_dummies(X, columns=categorical_cols, drop_first=True)

    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(n_estimators=500, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    joblib.dump(model, MODEL_PATH)
    joblib.dump(list(X_train.columns), COLS_PATH)

    print(f"Model saved to: {MODEL_PATH}")
    print(f"Feature columns saved to: {COLS_PATH}")
    print(f"Training rows: {len(X_train)} | Test rows: {len(X_test)}")
    print(f"Training columns: {len(X_train.columns)}")


if __name__ == "__main__":
    main()
