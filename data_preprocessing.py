import argparse
import pandas as pd
import re


def clean_harga(value, to_numeric=False):
    if pd.isna(value):
        return value
    text = str(value).strip()

    # Remove 'Rp' prefix
    text = text.lstrip('Rp').strip()

    # For Rupiah format, remove dots (thousands separators) and replace comma with dot for decimal
    # Example: "37.050.000,00" -> "37050000.00"
    if ',' in text:
        # Split by comma, take first part, remove dots
        parts = text.split(',')
        if len(parts) >= 2:
            main_part = parts[0].replace('.', '')
            decimal_part = parts[1]
            text = f"{main_part}.{decimal_part}"
        else:
            text = text.replace('.', '').replace(',', '')
    else:
        text = text.replace('.', '')

    # Remove any remaining non-digit characters except dot and minus
    cleaned = re.sub(r"[^0-9.\-]", "", text)
    if cleaned == "":
        return None if to_numeric else text

    if to_numeric:
        return pd.to_numeric(cleaned, errors='coerce')
    return cleaned


def clean_km_driven(value, to_numeric=False):
    if pd.isna(value):
        return value
    text = str(value).strip()

    # Remove 'km' suffix and clean up
    text = text.lower().replace('km', '').strip()

    # Remove commas and spaces
    text = text.replace(',', '').replace(' ', '')

    # Remove any non-digit characters except dot and minus
    cleaned = re.sub(r"[^0-9.\-]", "", text)
    if cleaned == "":
        return None if to_numeric else text

    if to_numeric:
        return pd.to_numeric(cleaned, errors='coerce')
    return cleaned


def clean_askprice(value, to_numeric=False):
    if pd.isna(value):
        return value
    text = str(value).strip()
    text = text.lstrip('?').strip()

    # Remove any non-digit characters except dot and minus
    cleaned = re.sub(r"[^0-9.\-]", "", text)
    if cleaned == "":
        return None if to_numeric else text

    if to_numeric:
        return pd.to_numeric(cleaned, errors='coerce')
    return cleaned


def process_dataset(input_path, output_path, numeric=False, fields=['AskPrice', 'Harga', 'kmDriven'], encoding='latin1', **read_kwargs):
    df = pd.read_csv(input_path, encoding=encoding, **read_kwargs)

    # Map field names to actual column names (case-insensitive)
    columns_lower = {col.lower(): col for col in df.columns}

    for field in fields:
        field_key = field if field in df.columns else columns_lower.get(field.lower())
        if field_key is None:
            print(f"Warning: Field '{field}' not found in dataset columns, skipping...")
            continue

        if field_key.lower() == 'harga':
            df[field_key] = df[field_key].apply(lambda v: clean_harga(v, to_numeric=numeric))
        elif field_key.lower() == 'askprice':
            df[field_key] = df[field_key].apply(lambda v: clean_askprice(v, to_numeric=numeric))
        elif field_key.lower() == 'kmdriven':
            df[field_key] = df[field_key].apply(lambda v: clean_km_driven(v, to_numeric=numeric))
        else:
            # Generic cleaning for other fields
            df[field_key] = df[field_key].apply(lambda v: clean_askprice(v, to_numeric=numeric))

    df.to_csv(output_path, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Clean AskPrice and Harga fields by removing prefixes, trimming whitespace, and optionally converting to numeric.'
    )
    parser.add_argument('input', help='Input CSV file path')
    parser.add_argument('output', help='Output CSV file path')
    parser.add_argument('--numeric', action='store_true', help='Convert price fields to numeric values')
    parser.add_argument('--fields', nargs='*', default=['AskPrice', 'Harga', 'kmDriven'],
                       help='Field names to clean (default: AskPrice Harga kmDriven)')
    parser.add_argument('--delimiter', default=';', help='CSV delimiter (default: ;)')
    parser.add_argument('--encoding', default='latin1', help='CSV encoding (default: latin1)')
    args = parser.parse_args()

    process_dataset(
        args.input,
        args.output,
        numeric=args.numeric,
        fields=args.fields,
        sep=args.delimiter,
        encoding=args.encoding,
    )
