import argparse
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


def clean_askprice(text):
    if pd.isna(text):
        return np.nan
    text = str(text).strip()
    text = text.lstrip('?').strip()
    text = text.replace('.', '').replace(',', '')
    return pd.to_numeric(text, errors='coerce')


def clean_harga(text):
    if pd.isna(text):
        return np.nan
    text = str(text).strip()
    text = text.lstrip('Rp').strip()
    text = text.replace('.', '').replace(',', '.')
    return pd.to_numeric(text, errors='coerce')


def clean_kmdriven(text):
    if pd.isna(text):
        return np.nan
    text = str(text).strip().lower()
    text = text.replace('km', '').replace(',', '').replace(' ', '').strip()
    return pd.to_numeric(text, errors='coerce')


def load_dataset(path='cleaned.csv'):
    df = pd.read_csv(path, sep=None, engine='python', encoding='latin1', na_filter=True)
    df['AskPrice'] = df['AskPrice'].apply(clean_askprice)
    df['Harga'] = df['Harga'].apply(clean_harga)
    df['kmDriven'] = df['kmDriven'].apply(clean_kmdriven)

    df = df.dropna(subset=['Brand', 'model', 'Year', 'Age', 'kmDriven', 'Transmission', 'Owner', 'FuelType', 'Harga'])
    df['Brand'] = df['Brand'].astype(str)
    df['model'] = df['model'].astype(str)
    df['Transmission'] = df['Transmission'].astype(str)
    df['Owner'] = df['Owner'].astype(str)
    df['FuelType'] = df['FuelType'].astype(str)

    return df


def build_model(X, y):
    categorical_features = ['Brand', 'model', 'Transmission', 'Owner', 'FuelType']
    numeric_features = ['Year', 'Age', 'kmDriven']

    transformer = ColumnTransformer([
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features),
    ], remainder='passthrough')

    pipeline = Pipeline([
        ('preprocessor', transformer),
        ('regressor', RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)),
    ])

    pipeline.fit(X, y)
    return pipeline


def prepare_features(df):
    X = df[['Brand', 'model', 'Year', 'Age', 'kmDriven', 'Transmission', 'Owner', 'FuelType']].copy()
    y = df['Harga']
    return X, y


def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f'Model evaluation: MAE={mae:,.0f}, R2={r2:.4f}')


def predict_future_price(model, feature_dict, years_ahead):
    sample_current = pd.DataFrame([feature_dict])
    sample_future = sample_current.copy()
    sample_future['Age'] = sample_future['Age'] + years_ahead

    current_price = model.predict(sample_current)[0]
    future_price = model.predict(sample_future)[0]
    return current_price, future_price


def select_option(prompt, options):
    options = sorted(list(options))
    if len(options) > 20:
        return select_option_with_search(prompt, options)

    while True:
        print(f"\nPilih {prompt}:")
        for idx, option in enumerate(options, 1):
            print(f"  {idx}. {option}")
        choice = input(f"Masukkan nomor pilihan {prompt} (1-{len(options)}): ").strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                return options[idx]
        print('Pilihan tidak valid, silakan coba lagi.')


def select_option_with_search(prompt, options):
    options = sorted(list(options))
    while True:
        search = input(f"\nMasukkan teks untuk mencari {prompt} atau tekan Enter untuk menampilkan semua: ").strip().lower()
        filtered = [opt for opt in options if search in opt.lower()]
        if not filtered:
            print('Tidak ditemukan hasil. Silakan coba kata lain.')
            continue
        print(f"\nHasil pencarian {prompt} ({len(filtered)}):")
        for idx, option in enumerate(filtered[:20], 1):
            print(f"  {idx}. {option}")
        if len(filtered) > 20:
            print('Menampilkan 20 hasil pertama. Ketik kata lain untuk mempersempit.')
        choice = input(f"Pilih nomor hasil {prompt} (1-{min(len(filtered), 20)}): ").strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < min(len(filtered), 20):
                return filtered[idx]
        print('Pilihan tidak valid, silakan coba lagi.')


def input_year(prompt, available_years):
    years = sorted(set(int(y) for y in available_years if not pd.isna(y)), reverse=True)
    print(f"\nAvailable {prompt} values: {years[:20]}{' ...' if len(years) > 20 else ''}")
    while True:
        value = input(f"Masukkan {prompt} (contoh: {years[0]}): ").strip()
        if value.isdigit() and int(value) in years:
            return int(value)
        print('Tahun tidak valid atau tidak tersedia dalam dataset.')


def input_positive_int(prompt, max_value=None):
    while True:
        value = input(f"Masukkan {prompt} (angka positif){' maks ' + str(max_value) if max_value else ''}: ").strip()
        if value.isdigit():
            number = int(value)
            if number > 0 and (max_value is None or number <= max_value):
                return number
        print('Nilai harus berupa angka positif yang valid. Silakan coba lagi.')


def input_float(prompt, default=None):
    while True:
        value = input(f"Masukkan {prompt} (angka): ").strip()
        try:
            return float(value)
        except ValueError:
            print('Nilai harus berupa angka. Silakan coba lagi.')


def parse_args():
    parser = argparse.ArgumentParser(
        description='Predict car price using Random Forest and dataset features.'
    )
    parser.add_argument('--csv', type=str, default='cleaned.csv', help='Path to dataset CSV')
    return parser.parse_args()


def main():
    args = parse_args()
    print('Loading dataset and training model...')
    df = load_dataset(args.csv)

    X, y = prepare_features(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = build_model(X_train, y_train)

    print(f'Training data size: {len(X_train)}, test size: {len(X_test)}')
    evaluate_model(model, X_test, y_test)

    print('\nGood predictor variables for price:')
    print('- Age / Year of manufacture')
    print('- kmDriven (mileage)')
    print('- Brand and model')
    print('- Transmission type')
    print('- Owner category')
    print('- FuelType')

    brand = select_option('Brand', df['Brand'].unique())
    brand_models = df[df['Brand'] == brand]['model'].unique()
    model_name = select_option('Model', brand_models)
    transmission = select_option('Transmission', df['Transmission'].unique())
    owner = select_option('Owner', df['Owner'].unique())
    fueltype = select_option('FuelType', df['FuelType'].unique())
    year = input_year('Year', df['Year'].unique())
    age = pd.Timestamp.now().year - year
    km = input_float('kmDriven')
    years_ahead = input_positive_int('berapa tahun ke depan untuk prediksi', max_value=20)

    feature_dict = {
        'Brand': brand,
        'model': model_name,
        'Year': year,
        'Age': age,
        'kmDriven': km,
        'Transmission': transmission,
        'Owner': owner,
        'FuelType': fueltype,
    }

    current_price, future_price = predict_future_price(model, feature_dict, years_ahead)
    print(f"\nPrediksi harga saat ini: Rp {current_price:,.0f}")
    print(f"Prediksi harga dalam {years_ahead} tahun: Rp {future_price:,.0f}")


if __name__ == '__main__':
    main()
