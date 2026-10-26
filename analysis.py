"""
Analysis Module for Electric Vehicle (EV) Market Performance Dashboard.

Provides reusable analytical computation functions for:
- Executive KPIs
- Sales trend aggregations
- Category breakdown
- Battery technology benchmarking
- Manufacturer performance and ranking
- Sustainability metrics & carbon offset calculations
- Statistical correlations
"""

from typing import Dict, Any
import numpy as np
import pandas as pd


def calculate_executive_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes high-level Key Performance Indicators (KPIs) dynamically
    from the current filtered dataset.
    """
    if df.empty:
        return {
            "total_sales": 0,
            "total_manufacturers": 0,
            "avg_range_km": 0.0,
            "avg_rating": 0.0,
            "total_vehicles": 0,
            "total_co2_avoided_tonnes": 0.0,
            "avg_price_usd": 0.0,
            "total_revenue_usd": 0.0,
            "avg_capacity_kwh": 0.0,
        }

    total_sales = int(df["Annual Sales"].sum())
    total_manufacturers = int(df["Manufacturer"].nunique())
    avg_range = float(df["Driving Range (km)"].mean())
    avg_rating = float(df["Customer Rating"].mean())
    total_vehicles = len(df)
    total_co2 = float(df["Total Fleet CO2 Avoided (Tonnes)"].sum()) if "Total Fleet CO2 Avoided (Tonnes)" in df.columns else float((df["Annual Sales"] * df["Estimated CO2 Emissions Avoided"]).sum())
    avg_price = float(df["Vehicle Price"].mean())
    total_revenue = float(df["Fleet Revenue ($)"].sum()) if "Fleet Revenue ($)" in df.columns else float((df["Annual Sales"] * df["Vehicle Price"]).sum())
    avg_capacity = float(df["Battery Capacity (kWh)"].mean())

    return {
        "total_sales": total_sales,
        "total_manufacturers": total_manufacturers,
        "avg_range_km": round(avg_range, 1),
        "avg_rating": round(avg_rating, 2),
        "total_vehicles": total_vehicles,
        "total_co2_avoided_tonnes": round(total_co2, 1),
        "avg_price_usd": round(avg_price, 2),
        "total_revenue_usd": total_revenue,
        "avg_capacity_kwh": round(avg_capacity, 1),
    }


def get_sales_trends(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates annual EV sales by Model Year and Vehicle Category.
    """
    if df.empty:
        return pd.DataFrame()

    trend = (
        df.groupby(["Model Year", "Vehicle Category"], as_index=False)
        .agg(
            Total_Sales=("Annual Sales", "sum"),
            Avg_Price=("Vehicle Price", "mean"),
            Vehicle_Count=("Vehicle ID", "count"),
        )
        .sort_values(by="Model Year")
    )
    return trend


def get_annual_sales_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates overall yearly total sales, growth rate, and average price.
    """
    if df.empty:
        return pd.DataFrame()

    yearly = (
        df.groupby("Model Year", as_index=False)
        .agg(
            Total_Sales=("Annual Sales", "sum"),
            Avg_Price=("Vehicle Price", "mean"),
            Total_CO2=("Total Fleet CO2 Avoided (Tonnes)", "sum"),
            Active_Models=("Vehicle Model", "nunique"),
        )
        .sort_values(by="Model Year")
    )
    yearly["YoY_Growth_%"] = yearly["Total_Sales"].pct_change() * 100
    yearly["YoY_Growth_%"] = yearly["YoY_Growth_%"].fillna(0.0).round(1)
    return yearly


def get_category_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyzes market metrics grouped by Vehicle Category.
    """
    if df.empty:
        return pd.DataFrame()

    total_market_sales = df["Annual Sales"].sum()
    cat_df = (
        df.groupby("Vehicle Category", as_index=False)
        .agg(
            Total_Sales=("Annual Sales", "sum"),
            Avg_Price=("Vehicle Price", "mean"),
            Avg_Range=("Driving Range (km)", "mean"),
            Avg_Capacity=("Battery Capacity (kWh)", "mean"),
            Avg_Rating=("Customer Rating", "mean"),
            Model_Count=("Vehicle ID", "count"),
            Total_CO2_Avoided=("Total Fleet CO2 Avoided (Tonnes)", "sum"),
        )
        .sort_values(by="Total_Sales", ascending=False)
    )
    
    cat_df["Market_Share_%"] = (cat_df["Total_Sales"] / total_market_sales * 100).round(2)
    cat_df["Avg_Price"] = cat_df["Avg_Price"].round(0)
    cat_df["Avg_Range"] = cat_df["Avg_Range"].round(1)
    cat_df["Avg_Capacity"] = cat_df["Avg_Capacity"].round(1)
    cat_df["Avg_Rating"] = cat_df["Avg_Rating"].round(2)
    cat_df["Total_CO2_Avoided"] = cat_df["Total_CO2_Avoided"].round(1)
    
    return cat_df


def get_top_manufacturers(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Ranks top manufacturers by total sales, market share, and average rating.
    """
    if df.empty:
        return pd.DataFrame()

    total_market_sales = df["Annual Sales"].sum()
    mfr_df = (
        df.groupby(["Manufacturer", "Manufacturing Country"], as_index=False)
        .agg(
            Total_Sales=("Annual Sales", "sum"),
            Total_Revenue=("Fleet Revenue ($)", "sum"),
            Avg_Rating=("Customer Rating", "mean"),
            Avg_Price=("Vehicle Price", "mean"),
            Avg_Range=("Driving Range (km)", "mean"),
            Models_Count=("Vehicle ID", "count"),
        )
        .sort_values(by="Total_Sales", ascending=False)
    )

    mfr_df["Market_Share_%"] = ((mfr_df["Total_Sales"] / total_market_sales) * 100).round(2)
    mfr_df["Avg_Rating"] = mfr_df["Avg_Rating"].round(2)
    mfr_df["Avg_Price"] = mfr_df["Avg_Price"].round(0)
    mfr_df["Avg_Range"] = mfr_df["Avg_Range"].round(1)
    mfr_df["Rank"] = range(1, len(mfr_df) + 1)
    
    return mfr_df.head(top_n)


def get_battery_analysis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes battery technology benchmarks including capacity, range,
    charging speed, and energy efficiency.
    """
    if df.empty:
        return {"summary": pd.DataFrame(), "distribution": pd.DataFrame()}

    summary = (
        df.groupby("Battery Technology", as_index=False)
        .agg(
            Model_Count=("Vehicle ID", "count"),
            Total_Sales=("Annual Sales", "sum"),
            Avg_Capacity_kWh=("Battery Capacity (kWh)", "mean"),
            Median_Capacity_kWh=("Battery Capacity (kWh)", "median"),
            Avg_Range_km=("Driving Range (km)", "mean"),
            Avg_Charging_Time_hrs=("Charging Time (hours)", "mean"),
            Avg_Efficiency_km_per_kWh=("Energy Efficiency (km/kWh)", "mean"),
            Avg_Rating=("Customer Rating", "mean"),
        )
        .sort_values(by="Total_Sales", ascending=False)
    )

    summary["Avg_Capacity_kWh"] = summary["Avg_Capacity_kWh"].round(1)
    summary["Median_Capacity_kWh"] = summary["Median_Capacity_kWh"].round(1)
    summary["Avg_Range_km"] = summary["Avg_Range_km"].round(1)
    summary["Avg_Charging_Time_hrs"] = summary["Avg_Charging_Time_hrs"].round(2)
    summary["Avg_Efficiency_km_per_kWh"] = summary["Avg_Efficiency_km_per_kWh"].round(2)
    summary["Avg_Rating"] = summary["Avg_Rating"].round(2)
    
    # Distribution of battery technologies
    dist = (
        df["Battery Technology"]
        .value_counts(normalize=True)
        .reset_index()
    )
    dist.columns = ["Battery Technology", "Proportion"]
    dist["Percentage"] = (dist["Proportion"] * 100).round(2)

    return {"summary": summary, "distribution": dist}


def get_country_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates manufacturing countries by total sales, vehicle offerings,
    and average customer ratings.
    """
    if df.empty:
        return pd.DataFrame()

    total_market_sales = df["Annual Sales"].sum()
    country_df = (
        df.groupby("Manufacturing Country", as_index=False)
        .agg(
            Total_Sales=("Annual Sales", "sum"),
            Total_Revenue=("Fleet Revenue ($)", "sum"),
            Unique_Manufacturers=("Manufacturer", "nunique"),
            Total_Models=("Vehicle ID", "count"),
            Avg_Rating=("Customer Rating", "mean"),
            Avg_Price=("Vehicle Price", "mean"),
        )
        .sort_values(by="Total_Sales", ascending=False)
    )

    country_df["Market_Share_%"] = ((country_df["Total_Sales"] / total_market_sales) * 100).round(2)
    country_df["Avg_Rating"] = country_df["Avg_Rating"].round(2)
    country_df["Avg_Price"] = country_df["Avg_Price"].round(0)
    
    return country_df


def calculate_sustainability_impact(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Performs comprehensive sustainability and carbon avoidance calculations
    with environmental equivalencies and transparent methodology notes.
    """
    if df.empty:
        return {
            "total_co2_tonnes": 0.0,
            "trees_equivalent": 0,
            "gasoline_liters_saved": 0.0,
            "gasoline_gallons_saved": 0.0,
            "coal_kg_avoided": 0.0,
            "category_co2": pd.DataFrame(),
            "tech_co2": pd.DataFrame(),
            "assumptions": get_sustainability_assumptions(),
        }

    total_co2 = float(df["Total Fleet CO2 Avoided (Tonnes)"].sum())

    # Environmental Equivalencies:
    # 1. Trees: 1 mature tree absorbs ~21.77 kg of CO2/year => ~45.93 trees per metric tonne of CO2
    trees_equivalent = int(total_co2 * 45.93)

    # 2. Gasoline liters: Combustion of 1 liter of gasoline emits ~2.31 kg CO2 => ~432.9 liters per metric tonne
    gasoline_liters_saved = total_co2 * 432.9

    # 3. Gasoline gallons: 1 US gallon = 8.887 kg CO2 => ~112.5 gallons per metric tonne
    gasoline_gallons_saved = total_co2 * 112.5

    # 4. Coal: 1 kg of bituminous coal combustion produces ~2.42 kg CO2 => ~413.2 kg coal per metric tonne
    coal_kg_avoided = total_co2 * 413.2

    # Grouped by category
    category_co2 = (
        df.groupby("Vehicle Category", as_index=False)
        .agg(
            Total_CO2_Avoided_Tonnes=("Total Fleet CO2 Avoided (Tonnes)", "sum"),
            Total_Sales=("Annual Sales", "sum"),
            Avg_Per_Vehicle_CO2=("Estimated CO2 Emissions Avoided", "mean"),
        )
        .sort_values(by="Total_CO2_Avoided_Tonnes", ascending=False)
    )
    category_co2["Avg_Per_Vehicle_CO2"] = category_co2["Avg_Per_Vehicle_CO2"].round(2)
    category_co2["Total_CO2_Avoided_Tonnes"] = category_co2["Total_CO2_Avoided_Tonnes"].round(1)

    # Grouped by battery technology
    tech_co2 = (
        df.groupby("Battery Technology", as_index=False)
        .agg(
            Total_CO2_Avoided_Tonnes=("Total Fleet CO2 Avoided (Tonnes)", "sum"),
            Total_Sales=("Annual Sales", "sum"),
            Avg_Per_Vehicle_CO2=("Estimated CO2 Emissions Avoided", "mean"),
        )
        .sort_values(by="Total_CO2_Avoided_Tonnes", ascending=False)
    )
    tech_co2["Avg_Per_Vehicle_CO2"] = tech_co2["Avg_Per_Vehicle_CO2"].round(2)
    tech_co2["Total_CO2_Avoided_Tonnes"] = tech_co2["Total_CO2_Avoided_Tonnes"].round(1)

    return {
        "total_co2_tonnes": round(total_co2, 1),
        "trees_equivalent": trees_equivalent,
        "gasoline_liters_saved": round(gasoline_liters_saved, 1),
        "gasoline_gallons_saved": round(gasoline_gallons_saved, 1),
        "coal_kg_avoided": round(coal_kg_avoided, 1),
        "category_co2": category_co2,
        "tech_co2": tech_co2,
        "assumptions": get_sustainability_assumptions(),
    }


def get_sustainability_assumptions() -> Dict[str, str]:
    """
    Returns verified, clear explanations of methodology and carbon accounting assumptions.
    """
    return {
        "Baseline ICE Emissions": (
            "Internal Combustion Engine (ICE) baseline emissions assume standard regulatory factors: "
            "Passenger cars ~150-190 g CO2/km; SUVs/Light Trucks ~220-310 g CO2/km; Heavy Duty Transit Buses ~1,200-1,450 g CO2/km; "
            "Two-Wheelers ~45-60 g CO2/km."
        ),
        "Average Driving Distance": (
            "Annual distance traveled assumed per category: Two-Wheelers ~6,000 km/year; "
            "Passenger Sedans/SUVs ~15,000 km/year; Commercial Trucks ~35,000 km/year; Urban Transit Buses ~55,000 km/year."
        ),
        "Electric Grid Carbon Intensity": (
            "EV operational emissions incorporate average global electricity generation grid intensity "
            "of ~430 g CO2/kWh, accounting for transmission losses (7%) and charging efficiency (88%)."
        ),
        "Net Avoided Emissions Formula": (
            "Estimated CO2 Avoided (Tonnes/yr/veh) = [ (ICE Baseline g/km - EV Grid Equivalent g/km) * Annual km ] / 1,000,000."
        ),
        "Environmental Equivalency Factors": (
            "Tree offset factor: 1 mature tree sequestering 21.77 kg CO2/yr (US EPA standard). "
            "Gasoline factor: 1 liter gasoline = 2.31 kg CO2 avoided (1 US gallon = 8.887 kg CO2)."
        ),
    }


def get_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates Pearson correlation matrix for numeric features.
    """
    if df.empty:
        return pd.DataFrame()

    cols = [
        "Battery Capacity (kWh)",
        "Driving Range (km)",
        "Charging Time (hours)",
        "Vehicle Price",
        "Customer Rating",
        "Annual Sales",
        "Estimated CO2 Emissions Avoided",
    ]
    existing = [c for c in cols if c in df.columns]
    corr = df[existing].corr().round(2)
    return corr
