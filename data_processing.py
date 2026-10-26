"""
Data Processing Module for Electric Vehicle (EV) Market Performance Analysis.

This module provides end-to-end data ingestion, validation, cleaning, imputation,
and feature engineering pipelines. It handles duplicates, missing values,
and prepares analytic-ready dataframes with full audit reporting.
"""

import os
from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd


# Required columns and expected data types
EXPECTED_COLUMNS = [
    "Vehicle ID",
    "Vehicle Model",
    "Manufacturer",
    "Vehicle Category",
    "Manufacturing Country",
    "Model Year",
    "Annual Sales",
    "Battery Technology",
    "Battery Capacity (kWh)",
    "Driving Range (km)",
    "Charging Time (hours)",
    "Vehicle Price",
    "Customer Rating",
    "Estimated CO2 Emissions Avoided",
]

NUMERIC_COLUMNS = [
    "Model Year",
    "Annual Sales",
    "Battery Capacity (kWh)",
    "Driving Range (km)",
    "Charging Time (hours)",
    "Vehicle Price",
    "Customer Rating",
    "Estimated CO2 Emissions Avoided",
]


def load_raw_data(file_path: str = "data/ev_market_data.csv") -> pd.DataFrame:
    """
    Load the raw EV market dataset from CSV or Excel.
    
    Args:
        file_path: Path to dataset file.
        
    Returns:
        pd.DataFrame containing raw data.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset not found at path: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()
    if ext in [".xlsx", ".xls"]:
        df = pd.read_excel(file_path)
    else:
        df = pd.read_csv(file_path)
        
    return df


def validate_schema(df: pd.DataFrame) -> Tuple[bool, list]:
    """
    Verify that all expected columns exist in the dataframe.
    
    Returns:
        Tuple of (is_valid, missing_columns)
    """
    missing_cols = [col for col in EXPECTED_COLUMNS if col not in df.columns]
    return (len(missing_cols) == 0, missing_cols)


def clean_and_transform_data(df_raw: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Cleans raw dataset, imputes missing values, validates numeric ranges,
    removes duplicates, and adds engineered analytical features.
    
    Returns:
        Tuple of (cleaned_df, quality_audit_dict)
    """
    df = df_raw.copy()
    
    # 1. Audit initial stats
    initial_rows = len(df)
    initial_nulls = df.isnull().sum().to_dict()
    initial_duplicates = int(df.duplicated(subset=["Vehicle ID"]).sum())
    
    # 2. Schema check
    is_valid, missing = validate_schema(df)
    if not is_valid:
        raise ValueError(f"Schema validation failed. Missing required columns: {missing}")

    # 3. Deduplication: drop exact duplicates and duplicate Vehicle IDs (keep first occurrence)
    df = df.drop_duplicates(subset=["Vehicle ID"], keep="first")
    duplicates_removed = initial_rows - len(df)
    
    # 4. Impute Missing Values
    # Impute Charging Time using median by Vehicle Category (or overall median if category is missing)
    if df["Charging Time (hours)"].isnull().any():
        cat_median_charge = df.groupby("Vehicle Category")["Charging Time (hours)"].transform("median")
        df["Charging Time (hours)"] = df["Charging Time (hours)"].fillna(cat_median_charge)
        df["Charging Time (hours)"] = df["Charging Time (hours)"].fillna(df["Charging Time (hours)"].median())
        df["Charging Time (hours)"] = df["Charging Time (hours)"].round(2)
        
    # Impute Customer Rating using mean by Manufacturer (or overall mean)
    if df["Customer Rating"].isnull().any():
        mfr_mean_rating = df.groupby("Manufacturer")["Customer Rating"].transform("mean")
        df["Customer Rating"] = df["Customer Rating"].fillna(mfr_mean_rating)
        df["Customer Rating"] = df["Customer Rating"].fillna(df["Customer Rating"].mean())
        df["Customer Rating"] = df["Customer Rating"].round(1)

    # Fallback fill for any other numeric columns with median
    for col in NUMERIC_COLUMNS:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].median())

    # 5. Data Type Coercion & Range Validation
    df["Model Year"] = pd.to_numeric(df["Model Year"], errors="coerce").fillna(2023).astype(int)
    df["Annual Sales"] = pd.to_numeric(df["Annual Sales"], errors="coerce").fillna(0).astype(int)
    df["Battery Capacity (kWh)"] = pd.to_numeric(df["Battery Capacity (kWh)"], errors="coerce").clip(lower=1.0)
    df["Driving Range (km)"] = pd.to_numeric(df["Driving Range (km)"], errors="coerce").clip(lower=10.0)
    df["Charging Time (hours)"] = pd.to_numeric(df["Charging Time (hours)"], errors="coerce").clip(lower=0.1)
    df["Vehicle Price"] = pd.to_numeric(df["Vehicle Price"], errors="coerce").clip(lower=500.0)
    df["Customer Rating"] = pd.to_numeric(df["Customer Rating"], errors="coerce").clip(1.0, 5.0)
    df["Estimated CO2 Emissions Avoided"] = pd.to_numeric(df["Estimated CO2 Emissions Avoided"], errors="coerce").clip(lower=0.1)

    # Clean text columns
    text_cols = ["Vehicle Model", "Manufacturer", "Vehicle Category", "Manufacturing Country", "Battery Technology"]
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip()

    # 6. Feature Engineering
    # Energy Efficiency (km per kWh)
    df["Energy Efficiency (km/kWh)"] = (df["Driving Range (km)"] / df["Battery Capacity (kWh)"]).round(2)
    
    # Consumption (kWh per 100km)
    df["Consumption (kWh/100km)"] = ((df["Battery Capacity (kWh)"] / df["Driving Range (km)"]) * 100).round(2)
    
    # Price per km of range ($/km)
    df["Price per Range ($/km)"] = (df["Vehicle Price"] / df["Driving Range (km)"]).round(2)
    
    # Annual Fleet Revenue ($ USD)
    df["Fleet Revenue ($)"] = (df["Annual Sales"] * df["Vehicle Price"]).astype(np.int64)
    
    # Total Fleet CO2 Emissions Avoided (Tonnes/year) = Annual Sales * Per Vehicle CO2 Avoidance
    df["Total Fleet CO2 Avoided (Tonnes)"] = (df["Annual Sales"] * df["Estimated CO2 Emissions Avoided"]).round(1)

    # 7. Compile Quality Audit
    post_nulls = df.isnull().sum().to_dict()
    total_cells = len(df) * len(df.columns)
    total_nulls_post = sum(post_nulls.values())
    health_score = round(((total_cells - total_nulls_post) / total_cells) * 100, 2)
    
    audit_report = {
        "initial_rows": initial_rows,
        "cleaned_rows": len(df),
        "duplicates_removed": duplicates_removed,
        "initial_duplicates_count": initial_duplicates,
        "initial_nulls": initial_nulls,
        "post_cleaning_nulls": post_nulls,
        "health_score": health_score,
        "total_columns": len(df.columns),
    }

    return df, audit_report


def filter_dataset(
    df: pd.DataFrame,
    year_range: Tuple[int, int] = None,
    manufacturers: list = None,
    categories: list = None,
    battery_techs: list = None,
    price_range: Tuple[float, float] = None,
) -> pd.DataFrame:
    """
    Applies multi-dimensional filters safely to dataset.
    """
    filtered = df.copy()

    if year_range:
        filtered = filtered[(filtered["Model Year"] >= year_range[0]) & (filtered["Model Year"] <= year_range[1])]

    if manufacturers and len(manufacturers) > 0:
        filtered = filtered[filtered["Manufacturer"].isin(manufacturers)]

    if categories and len(categories) > 0:
        filtered = filtered[filtered["Vehicle Category"].isin(categories)]

    if battery_techs and len(battery_techs) > 0:
        filtered = filtered[filtered["Battery Technology"].isin(battery_techs)]

    if price_range:
        filtered = filtered[(filtered["Vehicle Price"] >= price_range[0]) & (filtered["Vehicle Price"] <= price_range[1])]

    return filtered
