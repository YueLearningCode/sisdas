import argparse
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


DEFAULT_INPUT_PATH = Path("dataset/used_car_realistic_marketstyle.csv")
DEFAULT_OUTPUT_DIR = Path("dataset/processed")
DEFAULT_TARGET_COLUMN = "price_rp"

CATEGORICAL_COLUMNS = [
    "brand",
    "transmission",
    "fuel_type",
    "condition",
    "location",
    "color",
]

DEFAULT_DROP_COLUMNS = [
    "car_name",
    "instalment_rp_monthly",
]


def make_one_hot_encoder():
    try:
        return OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        return OneHotEncoder(handle_unknown="ignore", sparse=False)


def check_outliers_iqr(df, numeric_columns):
    outlier_rows = set()
    summary = []

    for column in numeric_columns:
        series = df[column].dropna()
        if series.empty:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        mask = (df[column] < lower_bound) | (df[column] > upper_bound)
        indexes = df.index[mask].tolist()
        outlier_rows.update(indexes)

        summary.append(
            {
                "column": column,
                "lower_bound": lower_bound,
                "upper_bound": upper_bound,
                "outlier_count": int(mask.sum()),
                "outlier_percent": round(float(mask.mean() * 100), 2),
            }
        )

    return pd.DataFrame(summary), sorted(outlier_rows)


def build_preprocessor(categorical_columns, numeric_columns, scale_numeric=False):
    numeric_steps = [("imputer", SimpleImputer(strategy="median"))]
    if scale_numeric:
        numeric_steps.append(("scaler", StandardScaler()))

    numeric_pipeline = Pipeline(numeric_steps)
    categorical_pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", make_one_hot_encoder()),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, numeric_columns),
            ("categorical", categorical_pipeline, categorical_columns),
        ],
        remainder="drop",
    )


def preprocess_dataset(
    input_path=DEFAULT_INPUT_PATH,
    output_dir=DEFAULT_OUTPUT_DIR,
    target_column=DEFAULT_TARGET_COLUMN,
    test_size=0.2,
    random_state=42,
    scale_numeric=False,
    remove_outliers=False,
):
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)

    if target_column not in df.columns:
        raise ValueError(f"Target column '{target_column}' tidak ditemukan di dataset.")

    existing_drop_columns = [
        column for column in DEFAULT_DROP_COLUMNS if column in df.columns and column != target_column
    ]
    df = df.drop(columns=existing_drop_columns)

    categorical_columns = [column for column in CATEGORICAL_COLUMNS if column in df.columns]
    numeric_columns = [
        column
        for column in df.select_dtypes(include=["number"]).columns
        if column != target_column
    ]

    outlier_summary, outlier_indexes = check_outliers_iqr(
        df,
        numeric_columns + [target_column],
    )
    outlier_summary.to_csv(output_dir / "outlier_summary.csv", index=False)

    if remove_outliers and outlier_indexes:
        df = df.drop(index=outlier_indexes).reset_index(drop=True)

    X = df.drop(columns=[target_column])
    y = df[target_column]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
    )

    preprocessor = build_preprocessor(
        categorical_columns=categorical_columns,
        numeric_columns=numeric_columns,
        scale_numeric=scale_numeric,
    )

    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)

    feature_names = preprocessor.get_feature_names_out()
    X_train_processed = pd.DataFrame(
        X_train_processed,
        columns=feature_names,
        index=X_train.index,
    )
    X_test_processed = pd.DataFrame(
        X_test_processed,
        columns=feature_names,
        index=X_test.index,
    )

    train_processed = X_train_processed.copy()
    train_processed[target_column] = y_train.values

    test_processed = X_test_processed.copy()
    test_processed[target_column] = y_test.values

    train_processed.to_csv(output_dir / "train_processed.csv", index=False)
    test_processed.to_csv(output_dir / "test_processed.csv", index=False)
    joblib.dump(preprocessor, output_dir / "preprocessor.joblib")

    metadata = {
        "input_path": str(input_path),
        "target_column": target_column,
        "test_size": test_size,
        "random_state": random_state,
        "scale_numeric": scale_numeric,
        "remove_outliers": remove_outliers,
        "rows_before_outlier_removal": len(pd.read_csv(input_path)),
        "rows_after_preprocessing": len(df),
        "train_rows": len(train_processed),
        "test_rows": len(test_processed),
        "numeric_columns": numeric_columns,
        "categorical_columns": categorical_columns,
        "dropped_columns": existing_drop_columns,
        "output_files": [
            "train_processed.csv",
            "test_processed.csv",
            "outlier_summary.csv",
            "preprocessor.joblib",
        ],
    }

    pd.Series(metadata).to_json(output_dir / "preprocess_metadata.json", indent=2)
    return train_processed, test_processed, preprocessor, outlier_summary


def parse_args():
    parser = argparse.ArgumentParser(description="Preprocess used car CSV for model training.")
    parser.add_argument("--input", default=DEFAULT_INPUT_PATH, help="Path CSV input.")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, help="Folder output hasil preprocessing.")
    parser.add_argument("--target", default=DEFAULT_TARGET_COLUMN, help="Kolom target prediksi.")
    parser.add_argument("--test-size", type=float, default=0.2, help="Proporsi data test.")
    parser.add_argument("--random-state", type=int, default=42, help="Seed train/test split.")
    parser.add_argument(
        "--scale",
        action="store_true",
        help="Aktifkan StandardScaler untuk fitur numeric. Optional untuk Random Forest.",
    )
    parser.add_argument(
        "--remove-outliers",
        action="store_true",
        help="Hapus baris outlier berdasarkan metode IQR.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    train_df, test_df, _, outliers = preprocess_dataset(
        input_path=args.input,
        output_dir=args.output_dir,
        target_column=args.target,
        test_size=args.test_size,
        random_state=args.random_state,
        scale_numeric=args.scale,
        remove_outliers=args.remove_outliers,
    )

    print("Preprocessing selesai.")
    print(f"Train shape: {train_df.shape}")
    print(f"Test shape: {test_df.shape}")
    print("Ringkasan outlier:")
    print(outliers.to_string(index=False))
