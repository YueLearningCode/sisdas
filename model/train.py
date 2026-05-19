import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


DEFAULT_TRAIN_PATH = Path("dataset/processed/train_processed.csv")
DEFAULT_TEST_PATH = Path("dataset/processed/test_processed.csv")
DEFAULT_TARGET_COLUMN = "price_rp"
DEFAULT_OUTPUT_DIR = Path("model/artifacts")
DEFAULT_MODEL_NAME = "car_price_model.pkl"


def load_training_data(train_path, test_path, target_column):
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    if target_column not in train_df.columns:
        raise ValueError(f"Target column '{target_column}' tidak ada di train dataset.")

    if target_column not in test_df.columns:
        raise ValueError(f"Target column '{target_column}' tidak ada di test dataset.")

    X_train = train_df.drop(columns=[target_column])
    y_train = train_df[target_column]
    X_test = test_df.drop(columns=[target_column])
    y_test = test_df[target_column]

    return X_train, X_test, y_train, y_test


def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred) ** 0.5
    r2 = r2_score(y_test, y_pred)

    return {
        "mae": round(float(mae), 2),
        "rmse": round(float(rmse), 2),
        "r2_score": round(float(r2), 4),
    }


def train_random_forest(
    train_path=DEFAULT_TRAIN_PATH,
    test_path=DEFAULT_TEST_PATH,
    target_column=DEFAULT_TARGET_COLUMN,
    output_dir=DEFAULT_OUTPUT_DIR,
    model_name=DEFAULT_MODEL_NAME,
    n_estimators=300,
    max_depth=None,
    random_state=42,
):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    X_train, X_test, y_train, y_test = load_training_data(
        train_path=train_path,
        test_path=test_path,
        target_column=target_column,
    )

    model = RandomForestRegressor(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=random_state,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    metrics = evaluate_model(model, X_test, y_test)

    model_path = output_dir / model_name
    metrics_path = output_dir / "training_metrics.json"
    feature_importance_path = output_dir / "feature_importance.csv"

    joblib.dump(model, model_path)

    metadata = {
        "algorithm": "RandomForestRegressor",
        "model_path": str(model_path),
        "train_path": str(train_path),
        "test_path": str(test_path),
        "target_column": target_column,
        "train_rows": len(X_train),
        "test_rows": len(X_test),
        "feature_count": X_train.shape[1],
        "n_estimators": n_estimators,
        "max_depth": max_depth,
        "random_state": random_state,
        "metrics": metrics,
        "target_note": "R2 > 0.80 sudah bagus untuk project mahasiswa.",
    }

    with metrics_path.open("w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=2)

    feature_importance = pd.DataFrame(
        {
            "feature": X_train.columns,
            "importance": model.feature_importances_,
        }
    ).sort_values(by="importance", ascending=False)
    feature_importance.to_csv(feature_importance_path, index=False)

    return model, metrics, model_path


def parse_args():
    parser = argparse.ArgumentParser(description="Train Random Forest model untuk prediksi harga mobil.")
    parser.add_argument("--train", default=DEFAULT_TRAIN_PATH, help="Path data train hasil preprocessing.")
    parser.add_argument("--test", default=DEFAULT_TEST_PATH, help="Path data test hasil preprocessing.")
    parser.add_argument("--target", default=DEFAULT_TARGET_COLUMN, help="Nama kolom target.")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, help="Folder untuk menyimpan model dan metrik.")
    parser.add_argument("--model-name", default=DEFAULT_MODEL_NAME, help="Nama file model .pkl.")
    parser.add_argument("--n-estimators", type=int, default=300, help="Jumlah tree Random Forest.")
    parser.add_argument("--max-depth", type=int, default=None, help="Batas kedalaman tree.")
    parser.add_argument("--random-state", type=int, default=42, help="Seed training.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    _, metrics, model_path = train_random_forest(
        train_path=args.train,
        test_path=args.test,
        target_column=args.target,
        output_dir=args.output_dir,
        model_name=args.model_name,
        n_estimators=args.n_estimators,
        max_depth=args.max_depth,
        random_state=args.random_state,
    )

    print("Training selesai.")
    print(f"Model disimpan ke: {model_path}")
    print(f"MAE: Rp {metrics['mae']:,.2f}")
    print(f"RMSE: Rp {metrics['rmse']:,.2f}")
    print(f"R2 Score: {metrics['r2_score']:.4f}")
