"""
Comprehensive Test Suite for EV Market Analysis Dashboard.
Tests:
1. Data loading and schema validation
2. Data cleaning, deduplication, imputation, feature engineering
3. Edge case filtering (empty filters, extreme ranges)
4. KPI calculations
5. Sales analysis aggregations
6. Battery analysis aggregations
7. Manufacturer analysis and rankings
8. Sustainability calculations & carbon equivalencies
9. Correlation matrix
10. Excel and CSV export generation
"""

import io
import data_processing as dp
import analysis as an
import pandas as pd
import numpy as np

def run_tests():
    print("--- 1. Testing Raw Ingestion & Schema Validation ---")
    raw_df = dp.load_raw_data("data/ev_market_data.csv")
    assert len(raw_df) > 500, f"Expected >500 records, got {len(raw_df)}"
    is_valid, missing = dp.validate_schema(raw_df)
    assert is_valid, f"Missing columns: {missing}"
    print(f"PASS: Raw dataset loaded with {len(raw_df)} records.")

    print("\n--- 2. Testing Data Cleaning & Quality Audit ---")
    clean_df, audit = dp.clean_and_transform_data(raw_df)
    assert audit["duplicates_removed"] > 0, "Expected duplicates to be detected and removed"
    assert clean_df.isnull().sum().sum() == 0, "No nulls should remain after cleaning"
    assert audit["health_score"] == 100.0, f"Expected 100% health score, got {audit['health_score']}"
    assert "Energy Efficiency (km/kWh)" in clean_df.columns
    assert "Price per Range ($/km)" in clean_df.columns
    assert "Fleet Revenue ($)" in clean_df.columns
    assert "Total Fleet CO2 Avoided (Tonnes)" in clean_df.columns
    print(f"PASS: Cleaned to {len(clean_df)} records. Quality score: {audit['health_score']}%.")

    print("\n--- 3. Testing Dynamic Filtering ---")
    # Test 3a: Standard filter
    filtered_1 = dp.filter_dataset(
        clean_df,
        year_range=(2021, 2024),
        categories=["SUV", "Sedan"],
        manufacturers=["Tesla", "BYD"],
    )
    assert len(filtered_1) > 0, "Filtered subset should contain records"
    print(f"PASS: Standard filter returned {len(filtered_1)} matching records.")

    # Test 3b: Empty filter edge case
    filtered_empty = dp.filter_dataset(
        clean_df,
        year_range=(2010, 2011),  # None exist
    )
    assert len(filtered_empty) == 0, "Empty filter should return 0 records"
    kpis_empty = an.calculate_executive_kpis(filtered_empty)
    assert kpis_empty["total_sales"] == 0
    assert kpis_empty["total_vehicles"] == 0
    print("PASS: Empty filter handled safely without exception.")

    print("\n--- 4. Testing Executive KPIs ---")
    kpis = an.calculate_executive_kpis(clean_df)
    assert kpis["total_sales"] > 0
    assert kpis["total_manufacturers"] > 5
    assert kpis["avg_range_km"] > 100
    assert 1.0 <= kpis["avg_rating"] <= 5.0
    print(f"PASS: KPIs computed - Sales: {kpis['total_sales']:,}, Mfrs: {kpis['total_manufacturers']}, Range: {kpis['avg_range_km']} km, Rating: {kpis['avg_rating']}/5.0")

    print("\n--- 5. Testing EV Sales Analysis Aggregations ---")
    trends = an.get_sales_trends(clean_df)
    assert not trends.empty
    yearly = an.get_annual_sales_summary(clean_df)
    assert not yearly.empty
    cat_analysis = an.get_category_analysis(clean_df)
    assert len(cat_analysis) == clean_df["Vehicle Category"].nunique()
    top_10 = an.get_top_manufacturers(clean_df, top_n=10)
    assert len(top_10) == 10
    print(f"PASS: Sales trends, category breakdown ({len(cat_analysis)} categories), and Top 10 manufacturers verified.")

    print("\n--- 6. Testing Battery Technology Analysis ---")
    b_analysis = an.get_battery_analysis(clean_df)
    assert not b_analysis["summary"].empty
    assert not b_analysis["distribution"].empty
    assert np.isclose(b_analysis["distribution"]["Percentage"].sum(), 100.0, atol=0.5)
    print(f"PASS: Battery chemistries analyzed: {b_analysis['summary']['Battery Technology'].tolist()}.")

    print("\n--- 7. Testing Manufacturer & Country Performance ---")
    countries = an.get_country_distribution(clean_df)
    assert not countries.empty
    assert np.isclose(countries["Market_Share_%"].sum(), 100.0, atol=0.5)
    print(f"PASS: Country distribution analyzed: {countries['Manufacturing Country'].tolist()}.")

    print("\n--- 8. Testing Sustainability Analysis ---")
    sust = an.calculate_sustainability_impact(clean_df)
    assert sust["total_co2_tonnes"] > 0
    assert sust["trees_equivalent"] > 0
    assert sust["gasoline_liters_saved"] > 0
    assert len(sust["assumptions"]) >= 4
    print(f"PASS: Sustainability verified - Avoided CO2: {sust['total_co2_tonnes']:,.1f} Tonnes, Trees: {sust['trees_equivalent']:,}.")

    print("\n--- 9. Testing Correlations ---")
    corr = an.get_correlation_matrix(clean_df)
    assert not corr.empty
    assert "Battery Capacity (kWh)" in corr.columns
    print(f"PASS: Correlation matrix computed with dimensions {corr.shape}.")

    print("\n--- 10. Testing CSV and Excel Export Generators ---")
    csv_bytes = clean_df.to_csv(index=False).encode("utf-8")
    assert len(csv_bytes) > 1000
    excel_buf = io.BytesIO()
    with pd.ExcelWriter(excel_buf, engine="openpyxl") as writer:
        clean_df.to_excel(writer, index=False)
    assert len(excel_buf.getvalue()) > 1000
    print("PASS: CSV and Excel export generation verified successfully.")

    print("\n[SUCCESS] ALL 10 TEST SUITES PASSED FLAWLESSLY!")

if __name__ == "__main__":
    run_tests()
