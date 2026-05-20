from pathlib import Path
import json

import joblib
import pandas as pd
from flask import Flask, jsonify, request


BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "model" / "artifacts" / "car_price_model.pkl"
PREPROCESSOR_PATH = BASE_DIR / "dataset" / "processed" / "preprocessor.joblib"
METRICS_PATH = BASE_DIR / "model" / "artifacts" / "training_metrics.json"
FEATURE_IMPORTANCE_PATH = BASE_DIR / "model" / "artifacts" / "feature_importance.csv"
DATASET_PATH = BASE_DIR / "dataset" / "used_car_realistic_marketstyle.csv"

NUMERIC_FEATURES = [
    "year",
    "mileage_km",
    "engine_size_cc",
    "owner_count",
]

CATEGORICAL_FEATURES = [
    "car_name",
    "brand",
    "transmission",
    "fuel_type",
    "condition",
    "location",
    "color",
]

ALL_FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES

FEATURE_LABELS = {
    "car_name": "Nama Mobil",
    "brand": "Brand",
    "year": "Tahun",
    "mileage_km": "Kilometer",
    "engine_size_cc": "Mesin",
    "owner_count": "Jumlah Pemilik",
    "transmission": "Transmisi",
    "fuel_type": "Bahan Bakar",
    "condition": "Kondisi",
    "location": "Lokasi",
    "color": "Warna",
}


app = Flask(__name__)


def load_artifacts():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model tidak ditemukan: {MODEL_PATH}")

    if not PREPROCESSOR_PATH.exists():
        raise FileNotFoundError(f"Preprocessor tidak ditemukan: {PREPROCESSOR_PATH}")

    model = joblib.load(MODEL_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)
    return model, preprocessor


def load_metrics():
    if not METRICS_PATH.exists():
        return {"metrics": {"rmse": 0, "r2_score": 0}}

    with METRICS_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_market_data():
    if not DATASET_PATH.exists():
        return pd.DataFrame()

    return pd.read_csv(DATASET_PATH)


model, preprocessor = load_artifacts()
training_metadata = load_metrics()
market_df = load_market_data()


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


def build_input_dataframe(payload):
    row = {feature: payload.get(feature) for feature in ALL_FEATURES}
    input_df = pd.DataFrame([row], columns=ALL_FEATURES)

    for feature in NUMERIC_FEATURES:
        input_df[feature] = pd.to_numeric(input_df[feature], errors="coerce")

    return input_df


def estimate_confidence(predicted_price):
    metrics = training_metadata.get("metrics", {})
    rmse = float(metrics.get("rmse", 0))
    r2_score = float(metrics.get("r2_score", 0))

    lower_bound = max(0, predicted_price - rmse)
    upper_bound = predicted_price + rmse

    if r2_score >= 0.9:
        label = "Tinggi"
    elif r2_score >= 0.8:
        label = "Cukup"
    else:
        label = "Rendah"

    return {
        "label": label,
        "r2_score": round(r2_score, 4),
        "estimated_error_rmse": int(round(rmse)),
        "price_range": {
            "min": int(round(lower_bound)),
            "max": int(round(upper_bound)),
        },
    }


def compare_market_price(payload, predicted_price):
    if market_df.empty:
        return {
            "status": "unavailable",
            "message": "Dataset pasar tidak tersedia.",
        }

    comparable = market_df.copy()
    car_name = payload.get("car_name")
    brand = payload.get("brand")
    year = pd.to_numeric(payload.get("year"), errors="coerce")

    if car_name:
        comparable = comparable[comparable["car_name"] == car_name]

    if brand:
        comparable = comparable[comparable["brand"] == brand]

    if pd.notna(year):
        comparable = comparable[
            comparable["year"].between(int(year) - 2, int(year) + 2)
        ]

    if comparable.empty:
        comparable = market_df

    average_price = float(comparable["price_rp"].mean())
    difference = float(predicted_price - average_price)
    difference_percent = (difference / average_price) * 100 if average_price else 0

    if difference_percent > 8:
        category = "Di atas rata-rata pasar"
    elif difference_percent < -8:
        category = "Di bawah rata-rata pasar"
    else:
        category = "Dekat rata-rata pasar"

    return {
        "status": "available",
        "category": category,
        "sample_count": int(len(comparable)),
        "average_price": int(round(average_price)),
        "difference": int(round(difference)),
        "difference_percent": round(float(difference_percent), 2),
    }


def get_price_distribution():
    if market_df.empty:
        return []

    bins = [
        (0, 100_000_000, "< 100 jt"),
        (100_000_000, 150_000_000, "100-150 jt"),
        (150_000_000, 200_000_000, "150-200 jt"),
        (200_000_000, 250_000_000, "200-250 jt"),
        (250_000_000, 300_000_000, "250-300 jt"),
        (300_000_000, float("inf"), "> 300 jt"),
    ]

    distribution = []
    for lower_bound, upper_bound, label in bins:
        if upper_bound == float("inf"):
            count = int((market_df["price_rp"] >= lower_bound).sum())
        else:
            count = int(
                ((market_df["price_rp"] >= lower_bound) & (market_df["price_rp"] < upper_bound)).sum()
            )

        distribution.append({"label": label, "count": count})

    return distribution


def get_feature_importance(limit=6):
    if not FEATURE_IMPORTANCE_PATH.exists():
        return []

    feature_importance = pd.read_csv(FEATURE_IMPORTANCE_PATH)
    grouped_importance = {feature: 0.0 for feature in ALL_FEATURES}

    for _, row in feature_importance.iterrows():
        raw_feature = row["feature"]
        importance = float(row["importance"])

        if raw_feature.startswith("numeric__"):
            feature_name = raw_feature.replace("numeric__", "", 1)
            grouped_importance[feature_name] = grouped_importance.get(feature_name, 0.0) + importance
            continue

        if raw_feature.startswith("categorical__"):
            encoded_feature = raw_feature.replace("categorical__", "", 1)
            for original_feature in CATEGORICAL_FEATURES:
                if encoded_feature.startswith(f"{original_feature}_"):
                    grouped_importance[original_feature] += importance
                    break

    sorted_importance = sorted(
        grouped_importance.items(),
        key=lambda item: item[1],
        reverse=True,
    )[:limit]

    return [
        {
            "feature": FEATURE_LABELS.get(feature, feature),
            "importance": round(float(importance), 4),
            "percentage": round(float(importance) * 100, 1),
        }
        for feature, importance in sorted_importance
    ]


@app.route("/health", methods=["GET"])
def health():
    return jsonify(
        {
            "status": "ok",
            "model_loaded": True,
            "preprocessor_loaded": True,
        }
    )


@app.route("/stats", methods=["GET"])
def stats():
    metrics = training_metadata.get("metrics", {})
    return jsonify(
        {
            "dataset_rows": int(len(market_df)) if not market_df.empty else 0,
            "metrics": metrics,
            "price_distribution": get_price_distribution(),
            "feature_importance": get_feature_importance(),
        }
    )


@app.route("/predict", methods=["POST", "OPTIONS"])
def predict():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"})

    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "Request body harus berupa JSON object."}), 400

    try:
        input_df = build_input_dataframe(payload)
        processed_input = preprocessor.transform(input_df)
        processed_input = pd.DataFrame(
            processed_input,
            columns=preprocessor.get_feature_names_out(),
        )
        predicted_price = model.predict(processed_input)[0]
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400

    rounded_price = int(round(predicted_price))
    return jsonify(
        {
            "predicted_price": rounded_price,
            "confidence": estimate_confidence(rounded_price),
            "market_comparison": compare_market_price(payload, rounded_price),
        }
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
