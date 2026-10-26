"""
Electric Vehicle (EV) Market Analysis Dashboard
================================================
A production-ready, interactive analytics application for transportation domain analysis,
market strategy, executive reporting, and sustainability assessment.

Author: Transportation Domain Individual Project Submission
Technology Stack: Python, Streamlit, Plotly, Pandas, NumPy
"""

import io
from typing import Tuple
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import data_processing as dp
import analysis as an


# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & THEME STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="EV Market Intelligence Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom High-Contrast, EV-Themed CSS
st.markdown(
    """
    <style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2.5rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 1400px;
    }

    /* Header Banner */
    .hero-banner {
        background: linear-gradient(135deg, #0A192F 0%, #0E1B2E 50%, #172A45 100%);
        border: 1px solid rgba(0, 210, 106, 0.25);
        border-radius: 14px;
        padding: 24px 28px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        color: #FFFFFF;
    }
    
    .hero-title {
        font-size: 1.95rem;
        font-weight: 800;
        color: #FFFFFF;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .hero-badge {
        background: #00D26A;
        color: #0A192F;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .hero-subtitle {
        color: #94A3B8;
        font-size: 0.95rem;
        margin-top: 6px;
        margin-bottom: 0;
        line-height: 1.5;
    }

    /* KPI Cards */
    .kpi-container {
        background: #FFFFFF;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        border-left: 5px solid #00D26A;
        padding: 16px 20px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
        margin-bottom: 12px;
    }

    .kpi-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 14px rgba(15, 23, 42, 0.08);
    }

    .kpi-label {
        font-size: 0.82rem;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 4px;
    }

    .kpi-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.2;
    }

    .kpi-subtext {
        font-size: 0.8rem;
        color: #059669;
        font-weight: 500;
        margin-top: 4px;
    }

    /* Section Subheaders */
    .section-header {
        font-size: 1.35rem;
        font-weight: 700;
        color: #0F172A;
        border-bottom: 2px solid #E2E8F0;
        padding-bottom: 8px;
        margin-top: 12px;
        margin-bottom: 18px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Card Containers */
    .content-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 18px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
    }

    /* Sample Disclaimer Banner */
    .sample-disclaimer {
        background: #FEF3C7;
        border-left: 4px solid #D97706;
        color: #92400E;
        padding: 10px 16px;
        border-radius: 8px;
        font-size: 0.86rem;
        margin-bottom: 20px;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0E1B2E !important;
        border-right: 1px solid #1E293B;
    }

    section[data-testid="stSidebar"] * {
        color: #F1F5F9 !important;
    }

    section[data-testid="stSidebar"] .stSelectbox label, 
    section[data-testid="stSidebar"] .stMultiSelect label,
    section[data-testid="stSidebar"] .stSlider label {
        color: #E2E8F0 !important;
        font-weight: 600 !important;
    }
    
    /* Footer */
    .custom-footer {
        text-align: center;
        padding: 20px;
        font-size: 0.85rem;
        color: #64748B;
        border-top: 1px solid #E2E8F0;
        margin-top: 40px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Plotly Theme Colors
PALETTE = {
    "primary": "#00D26A",
    "navy": "#0E1B2E",
    "blue": "#2563EB",
    "cyan": "#06B6D4",
    "purple": "#8B5CF6",
    "amber": "#F59E0B",
    "coral": "#EF4444",
    "gray": "#64748B",
    "sequence": ["#00D26A", "#2563EB", "#06B6D4", "#F59E0B", "#8B5CF6", "#EC4899", "#10B981"],
}


# -----------------------------------------------------------------------------
# 2. DATA INGESTION & CACHED PIPELINE
# -----------------------------------------------------------------------------
@st.cache_data(show_spinner="Ingesting and cleaning EV market dataset...")
def get_clean_data_and_audit():
    raw_df = dp.load_raw_data("data/ev_market_data.csv")
    clean_df, audit = dp.clean_and_transform_data(raw_df)
    return clean_df, audit


try:
    df_clean, data_audit = get_clean_data_and_audit()
except Exception as e:
    st.error(f"❌ Failed to load dataset: {e}")
    st.stop()


# -----------------------------------------------------------------------------
# 3. SIDEBAR NAVIGATION & MULTI-DIMENSIONAL FILTERS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚡ **EV Intelligence**")
    st.caption("Transportation Analytics Platform")
    st.markdown("---")

    # Section Navigation
    st.markdown("#### **🧭 Navigation**")
    selected_section = st.radio(
        label="Select Dashboard View",
        options=[
            "📌 Executive Overview",
            "📈 EV Sales Analysis",
            "🔋 Battery Technology",
            "🏭 Manufacturer Performance",
            "🌱 Sustainability Analysis",
            "🔍 Data Explorer & Quality",
        ],
        index=0,
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("#### **🎛️ Global Data Filters**")

    # Reset Filter Button
    if st.button("🔄 Reset All Filters", use_container_width=True):
        st.session_state["filter_years"] = (int(df_clean["Model Year"].min()), int(df_clean["Model Year"].max()))
        st.session_state["filter_cats"] = []
        st.session_state["filter_mfrs"] = []
        st.session_state["filter_techs"] = []
        st.session_state["filter_price"] = (int(df_clean["Vehicle Price"].min()), int(df_clean["Vehicle Price"].max()))
        st.rerun()

    # Filter 1: Model Year Range Slider
    min_year = int(df_clean["Model Year"].min())
    max_year = int(df_clean["Model Year"].max())
    default_years = st.session_state.get("filter_years", (min_year, max_year))
    selected_year_range = st.slider(
        "Model Year Range",
        min_value=min_year,
        max_value=max_year,
        value=default_years,
        step=1,
        key="filter_years",
    )

    # Filter 2: Vehicle Category Multiselect
    all_categories = sorted(df_clean["Vehicle Category"].unique().tolist())
    default_cats = st.session_state.get("filter_cats", [])
    selected_categories = st.multiselect(
        "Vehicle Category",
        options=all_categories,
        default=default_cats,
        placeholder="All Categories (Default)",
        key="filter_cats",
    )

    # Filter 3: Manufacturer Multiselect
    all_manufacturers = sorted(df_clean["Manufacturer"].unique().tolist())
    default_mfrs = st.session_state.get("filter_mfrs", [])
    selected_manufacturers = st.multiselect(
        "Manufacturer",
        options=all_manufacturers,
        default=default_mfrs,
        placeholder="All Manufacturers (Default)",
        key="filter_mfrs",
    )

    # Filter 4: Battery Technology Multiselect
    all_battery_techs = sorted(df_clean["Battery Technology"].unique().tolist())
    default_techs = st.session_state.get("filter_techs", [])
    selected_techs = st.multiselect(
        "Battery Technology",
        options=all_battery_techs,
        default=default_techs,
        placeholder="All Technologies (Default)",
        key="filter_techs",
    )

    # Filter 5: Price Range Slider
    min_price = int(df_clean["Vehicle Price"].min())
    max_price = int(df_clean["Vehicle Price"].max())
    default_price = st.session_state.get("filter_price", (min_price, max_price))
    selected_price_range = st.slider(
        "Vehicle Price ($ USD)",
        min_value=min_price,
        max_value=max_price,
        value=default_price,
        step=1000,
        format="$%d",
        key="filter_price",
    )

    # Apply filters dynamically
    df_filtered = dp.filter_dataset(
        df_clean,
        year_range=selected_year_range,
        categories=selected_categories,
        manufacturers=selected_manufacturers,
        battery_techs=selected_techs,
        price_range=selected_price_range,
    )

    st.markdown("---")
    st.markdown(
        f"""
        <div style="background: rgba(255,255,255,0.06); padding: 12px; border-radius: 8px; text-align: center;">
            <div style="font-size: 0.75rem; color: #94A3B8;">FILTER STATUS</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #00D26A;">
                {len(df_filtered)} / {len(df_clean)} Models
            </div>
            <div style="font-size: 0.75rem; color: #CBD5E1;">
                {round((len(df_filtered) / len(df_clean)) * 100, 1)}% of Catalog
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------------------------------------------------------
# 4. HEADER HERO BANNER & SAMPLE DATA DISCLAIMER
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero-banner">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
            <h1 class="hero-title">
                ⚡ Electric Vehicle Market Performance Dashboard
            </h1>
            <span class="hero-badge">Transportation Analytics</span>
        </div>
        <p class="hero-subtitle">
            Comprehensive market intelligence platform tracking EV sales, battery chemistry evolution, 
            manufacturer rankings, driving range benchmarks, and carbon displacement across global markets.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Academic / Synthetic Data Disclaimer
st.markdown(
    """
    <div class="sample-disclaimer">
        <strong>⚠️ Sample Data Notice:</strong> This dashboard operates on a carefully synthesized and validated sample dataset 
        (679 cleaned records across 2019–2025) designed to model real-world EV engineering attributes and market distributions. 
        It is provided for individual academic and analytical demonstration and is not certified corporate filing data.
    </div>
    """,
    unsafe_allow_html=True,
)

# Check if filters returned empty dataset
if df_filtered.empty:
    st.warning("⚠️ No vehicle models match your current filter criteria. Please loosen your filters in the sidebar to view analytical insights.")
    st.stop()

# Compute dynamic KPIs for current filter view
kpis = an.calculate_executive_kpis(df_filtered)


# -----------------------------------------------------------------------------
# 5. VIEW A: EXECUTIVE OVERVIEW
# -----------------------------------------------------------------------------
if selected_section == "📌 Executive Overview":
    st.markdown('<div class="section-header">📌 Executive Performance Overview</div>', unsafe_allow_html=True)

    # Primary KPI Row
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(
            f"""
            <div class="kpi-container">
                <div class="kpi-label">Total EV Sales</div>
                <div class="kpi-value">{kpis['total_sales'] / 1e6:.2f}M</div>
                <div class="kpi-subtext">Units Delivered</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
            <div class="kpi-container">
                <div class="kpi-label">Active Manufacturers</div>
                <div class="kpi-value">{kpis['total_manufacturers']}</div>
                <div class="kpi-subtext">Global Automakers</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f"""
            <div class="kpi-container">
                <div class="kpi-label">Avg Driving Range</div>
                <div class="kpi-value">{kpis['avg_range_km']} <span style="font-size:1rem; font-weight:600;">km</span></div>
                <div class="kpi-subtext">Per Full Charge</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            f"""
            <div class="kpi-container">
                <div class="kpi-label">Avg Customer Rating</div>
                <div class="kpi-value">{kpis['avg_rating']} <span style="font-size:1rem; color:#F59E0B;">★</span></div>
                <div class="kpi-subtext">Out of 5.0 Stars</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col5:
        st.markdown(
            f"""
            <div class="kpi-container">
                <div class="kpi-label">Vehicles Analyzed</div>
                <div class="kpi-value">{kpis['total_vehicles']}</div>
                <div class="kpi-subtext">Catalog Offerings</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Secondary Metric Highlights Row
    mcol1, mcol2, mcol3 = st.columns(3)
    with mcol1:
        st.metric(
            label="🌍 Estimated Fleet CO2 Avoided",
            value=f"{kpis['total_co2_avoided_tonnes'] / 1e6:.2f} Million Tonnes",
            help="Cumulative annual carbon displacement compared against internal combustion counterparts.",
        )
    with mcol2:
        st.metric(
            label="💰 Estimated Market Fleet Revenue",
            value=f"${kpis['total_revenue_usd'] / 1e9:.2f} Billion USD",
            help="Gross market revenue estimated from annual sales multiplied by average vehicle retail prices.",
        )
    with mcol3:
        st.metric(
            label="🔋 Average Battery Capacity",
            value=f"{kpis['avg_capacity_kwh']} kWh",
            help="Mean nominal usable battery pack capacity across filtered vehicles.",
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Executive Charts Grid
    chart_col1, chart_col2 = st.columns([1.4, 1.0])

    with chart_col1:
        st.markdown("##### 📈 Annual EV Sales Growth Trajectory (2019–2025)")
        annual_summary = an.get_annual_sales_summary(df_filtered)
        if not annual_summary.empty:
            fig_trend = go.Figure()
            fig_trend.add_trace(
                go.Bar(
                    x=annual_summary["Model Year"],
                    y=annual_summary["Total_Sales"],
                    name="Annual Sales",
                    marker_color=PALETTE["primary"],
                    opacity=0.85,
                    hovertemplate="<b>Year %{x}</b><br>Sales: %{y:,.0f} units<extra></extra>",
                )
            )
            fig_trend.add_trace(
                go.Scatter(
                    x=annual_summary["Model Year"],
                    y=annual_summary["Total_Sales"],
                    mode="lines+markers",
                    name="Growth Curve",
                    line=dict(color=PALETTE["navy"], width=3),
                    marker=dict(size=8, color=PALETTE["navy"]),
                    yaxis="y",
                    hovertemplate="<b>Trend %{x}</b><br>%{y:,.0f}<extra></extra>",
                )
            )
            fig_trend.update_layout(
                template="plotly_white",
                height=360,
                margin=dict(l=20, r=20, t=20, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                xaxis=dict(title="Model Year", tickmode="linear", dtick=1),
                yaxis=dict(title="Annual Sales (Units)", showgrid=True, gridcolor="#F1F5F9"),
            )
            st.plotly_chart(fig_trend, use_container_width=True)

    with chart_col2:
        st.markdown("##### 🚗 Sales Share by Vehicle Category")
        cat_data = an.get_category_analysis(df_filtered)
        if not cat_data.empty:
            fig_cat = px.pie(
                cat_data,
                names="Vehicle Category",
                values="Total_Sales",
                hole=0.55,
                color_discrete_sequence=PALETTE["sequence"],
            )
            fig_cat.update_traces(
                textposition="inside",
                textinfo="percent+label",
                hovertemplate="<b>%{label}</b><br>Sales: %{value:,.0f}<br>Share: %{percent}<extra></extra>",
            )
            fig_cat.update_layout(
                template="plotly_white",
                height=360,
                margin=dict(l=10, r=10, t=20, b=20),
                showlegend=False,
            )
            st.plotly_chart(fig_cat, use_container_width=True)

    # Executive Strategic Insights Card
    st.markdown("##### 💡 Strategic Market Observations")
    top_mfrs = an.get_top_manufacturers(df_filtered, top_n=3)
    top_mfr_name = top_mfrs.iloc[0]["Manufacturer"] if not top_mfrs.empty else "N/A"
    top_mfr_share = top_mfrs.iloc[0]["Market_Share_%"] if not top_mfrs.empty else 0.0

    st.markdown(
        f"""
        <div class="content-card">
            <ul style="margin: 0; padding-left: 20px; line-height: 1.8; color: #334155;">
                <li><strong>Rapid Market Expansion:</strong> Annual sales volumes have expanded significantly between 2019 and 2025, driven by expanding model availability, fast-charging infrastructure rollouts, and favorable cost parity curves.</li>
                <li><strong>Segment Dynamics:</strong> <strong>SUVs and Sedans</strong> command the majority of passenger retail deliveries, while <strong>Two-Wheelers</strong> drive massive unit volumes in emerging urban corridors.</li>
                <li><strong>Leadership Concentration:</strong> <strong>{top_mfr_name}</strong> currently holds the leading market share ({top_mfr_share}%), accompanied by intensifying competition from Chinese and European legacy OEMs.</li>
                <li><strong>Range & Chemistry Synergy:</strong> LFP battery technology has achieved rapid dominance in price-sensitive segments, while NMC and emerging Solid-State solutions maintain leadership in high-range luxury applications.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------------------------------------------------------
# 6. VIEW B: EV SALES ANALYSIS
# -----------------------------------------------------------------------------
elif selected_section == "📈 EV Sales Analysis":
    st.markdown('<div class="section-header">📈 EV Sales & Market Trends Analysis</div>', unsafe_allow_html=True)

    # Sales Overview KPIs
    cat_df = an.get_category_analysis(df_filtered)
    top_category = cat_df.iloc[0]["Vehicle Category"] if not cat_df.empty else "N/A"
    top_cat_sales = cat_df.iloc[0]["Total_Sales"] if not cat_df.empty else 0

    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.metric("Total Sales Volume", f"{kpis['total_sales']:,} units")
    with s2:
        st.metric("Top Selling Category", f"{top_category}", f"{top_cat_sales:,} units")
    with s3:
        st.metric("Average Vehicle Price", f"${kpis['avg_price_usd']:,.0f}")
    with s4:
        st.metric("Total Market Revenue", f"${kpis['total_revenue_usd'] / 1e9:.2f} B")

    st.markdown("<br>", unsafe_allow_html=True)

    # 1. Annual Sales Trends by Vehicle Category
    st.markdown("##### 📅 Annual Sales Progression by Category")
    sales_trends = an.get_sales_trends(df_filtered)
    if not sales_trends.empty:
        fig_cat_trend = px.bar(
            sales_trends,
            x="Model Year",
            y="Total_Sales",
            color="Vehicle Category",
            barmode="stack",
            color_discrete_sequence=PALETTE["sequence"],
            title="Annual Sales Composition by Vehicle Category",
        )
        fig_cat_trend.update_layout(
            template="plotly_white",
            height=400,
            xaxis=dict(title="Model Year", dtick=1),
            yaxis=dict(title="Annual Sales (Units)", showgrid=True),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        st.plotly_chart(fig_cat_trend, use_container_width=True)

    # 2. Sales by Category & Top 10 Manufacturers
    col_c1, col_c2 = st.columns([1, 1.2])

    with col_c1:
        st.markdown("##### 🚘 Sales & Price Analysis by Category")
        if not cat_df.empty:
            fig_cat_bar = px.bar(
                cat_df,
                x="Vehicle Category",
                y="Total_Sales",
                color="Avg_Price",
                color_continuous_scale="Viridis",
                text="Total_Sales",
                labels={"Total_Sales": "Annual Sales", "Avg_Price": "Avg Price ($)"},
            )
            fig_cat_bar.update_traces(texttemplate="%{text:,.0s}", textposition="outside")
            fig_cat_bar.update_layout(
                template="plotly_white",
                height=380,
                xaxis_title="Category",
                yaxis_title="Sales Volume",
            )
            st.plotly_chart(fig_cat_bar, use_container_width=True)

    with col_c2:
        st.markdown("##### 🏆 Top 10 Manufacturers by Total Sales")
        top_10_mfrs = an.get_top_manufacturers(df_filtered, top_n=10)
        if not top_10_mfrs.empty:
            fig_mfr_bar = px.bar(
                top_10_mfrs.sort_values(by="Total_Sales", ascending=True),
                x="Total_Sales",
                y="Manufacturer",
                orientation="h",
                color="Market_Share_%",
                color_continuous_scale="Teal",
                text="Total_Sales",
                labels={"Total_Sales": "Sales Units", "Market_Share_%": "Share (%)"},
            )
            fig_mfr_bar.update_traces(texttemplate="%{text:,.0s}", textposition="outside")
            fig_mfr_bar.update_layout(
                template="plotly_white",
                height=380,
                xaxis_title="Total Sales (Units)",
                yaxis_title="",
            )
            st.plotly_chart(fig_mfr_bar, use_container_width=True)

    # 3. Category Breakdown Data Table
    st.markdown("##### 📋 Segment Breakdown Summary Table")
    if not cat_df.empty:
        display_cat = cat_df[[
            "Vehicle Category",
            "Total_Sales",
            "Market_Share_%",
            "Avg_Price",
            "Avg_Range",
            "Avg_Capacity",
            "Avg_Rating",
            "Model_Count",
        ]].rename(
            columns={
                "Total_Sales": "Sales Units",
                "Market_Share_%": "Market Share (%)",
                "Avg_Price": "Avg Price ($)",
                "Avg_Range": "Avg Range (km)",
                "Avg_Capacity": "Avg Battery (kWh)",
                "Avg_Rating": "Avg Rating",
                "Model_Count": "Model Trims",
            }
        )
        st.dataframe(
            display_cat.style.format({
                "Sales Units": "{:,.0f}",
                "Market Share (%)": "{:.2f}%",
                "Avg Price ($)": "${:,.0f}",
                "Avg Range (km)": "{:.1f}",
                "Avg Battery (kWh)": "{:.1f}",
                "Avg Rating": "{:.2f}",
                "Model Trims": "{:d}",
            }),
            use_container_width=True,
            hide_index=True,
        )


# -----------------------------------------------------------------------------
# 7. VIEW C: BATTERY TECHNOLOGY ANALYSIS
# -----------------------------------------------------------------------------
elif selected_section == "🔋 Battery Technology":
    st.markdown('<div class="section-header">🔋 Battery Chemistry & Technical Performance</div>', unsafe_allow_html=True)

    battery_analysis = an.get_battery_analysis(df_filtered)
    b_summary = battery_analysis["summary"]
    b_dist = battery_analysis["distribution"]

    # Chemistry KPI Cards
    bcol1, bcol2, bcol3, bcol4 = st.columns(4)
    dominant_chem = b_dist.iloc[0]["Battery Technology"] if not b_dist.empty else "N/A"
    dominant_pct = b_dist.iloc[0]["Percentage"] if not b_dist.empty else 0.0
    highest_range_chem = b_summary.sort_values(by="Avg_Range_km", ascending=False).iloc[0]["Battery Technology"] if not b_summary.empty else "N/A"
    max_avg_range = b_summary.sort_values(by="Avg_Range_km", ascending=False).iloc[0]["Avg_Range_km"] if not b_summary.empty else 0.0

    with bcol1:
        st.metric("Dominant Chemistry", f"{dominant_chem}", f"{dominant_pct}% share")
    with bcol2:
        st.metric("Highest Range Chemistry", f"{highest_range_chem}", f"{max_avg_range} km avg")
    with bcol3:
        st.metric("Avg Capacity Across Fleet", f"{kpis['avg_capacity_kwh']} kWh")
    with bcol4:
        st.metric("Avg Charging Time", f"{df_filtered['Charging Time (hours)'].mean():.1f} hrs", "Standard Full Cycle")

    st.markdown("<br>", unsafe_allow_html=True)

    # Battery Chemistries: Distribution & Capacity Comparison
    row1_c1, row1_c2 = st.columns(2)
    with row1_c1:
        st.markdown("##### 🔬 Battery Chemistry Distribution")
        if not b_dist.empty:
            fig_chem_pie = px.pie(
                b_dist,
                names="Battery Technology",
                values="Proportion",
                hole=0.45,
                color_discrete_sequence=PALETTE["sequence"],
            )
            fig_chem_pie.update_traces(textposition="inside", textinfo="percent+label")
            fig_chem_pie.update_layout(template="plotly_white", height=350, margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig_chem_pie, use_container_width=True)

    with row1_c2:
        st.markdown("##### ⚡ Average Battery Capacity (kWh) by Technology")
        if not b_summary.empty:
            fig_cap_bar = px.bar(
                b_summary,
                x="Battery Technology",
                y="Avg_Capacity_kWh",
                color="Battery Technology",
                color_discrete_sequence=PALETTE["sequence"],
                text="Avg_Capacity_kWh",
                labels={"Avg_Capacity_kWh": "Capacity (kWh)"},
            )
            fig_cap_bar.update_traces(texttemplate="%{text:.1f} kWh", textposition="outside")
            fig_cap_bar.update_layout(
                template="plotly_white",
                height=350,
                showlegend=False,
                yaxis=dict(title="Average Usable Capacity (kWh)"),
            )
            st.plotly_chart(fig_cap_bar, use_container_width=True)

    # Driving Range & Charging Time Comparisons
    row2_c1, row2_c2 = st.columns(2)
    with row2_c1:
        st.markdown("##### 🛣️ Driving Range (km) Distribution Across Chemistries")
        fig_range_box = px.box(
            df_filtered,
            x="Battery Technology",
            y="Driving Range (km)",
            color="Battery Technology",
            color_discrete_sequence=PALETTE["sequence"],
            points="outliers",
        )
        fig_range_box.update_layout(
            template="plotly_white",
            height=360,
            showlegend=False,
            yaxis_title="Driving Range (km)",
            xaxis_title="Battery Chemistry",
        )
        st.plotly_chart(fig_range_box, use_container_width=True)

    with row2_c2:
        st.markdown("##### ⏱️ Charging Time (Hours) Comparison")
        fig_charge_box = px.box(
            df_filtered,
            x="Battery Technology",
            y="Charging Time (hours)",
            color="Battery Technology",
            color_discrete_sequence=PALETTE["sequence"],
            points="outliers",
        )
        fig_charge_box.update_layout(
            template="plotly_white",
            height=360,
            showlegend=False,
            yaxis_title="Charging Time (Hours)",
            xaxis_title="Battery Chemistry",
        )
        st.plotly_chart(fig_charge_box, use_container_width=True)

    # Interactive Scatter: Capacity vs Range Correlation
    st.markdown("##### 🔍 Battery Capacity vs. Driving Range Relationship")
    fig_scatter = px.scatter(
        df_filtered,
        x="Battery Capacity (kWh)",
        y="Driving Range (km)",
        color="Battery Technology",
        size="Annual Sales",
        hover_name="Vehicle Model",
        hover_data={
            "Manufacturer": True,
            "Vehicle Category": True,
            "Vehicle Price": ":$,.0f",
            "Energy Efficiency (km/kWh)": ":.2f",
            "Charging Time (hours)": ":.2f",
            "Annual Sales": ":,",
        },
        color_discrete_sequence=PALETTE["sequence"],
        title="Capacity (kWh) vs Driving Range (km) (Bubble Size = Annual Sales)",
    )
    fig_scatter.update_layout(
        template="plotly_white",
        height=450,
        xaxis_title="Battery Capacity (kWh)",
        yaxis_title="Driving Range (km)",
    )
    st.plotly_chart(fig_scatter, use_container_width=True)


# -----------------------------------------------------------------------------
# 8. VIEW D: MANUFACTURER PERFORMANCE
# -----------------------------------------------------------------------------
elif selected_section == "🏭 Manufacturer Performance":
    st.markdown('<div class="section-header">🏭 Automaker & Manufacturer Intelligence</div>', unsafe_allow_html=True)

    top_mfrs = an.get_top_manufacturers(df_filtered, top_n=15)
    country_data = an.get_country_distribution(df_filtered)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Automakers", f"{kpis['total_manufacturers']}")
    with m2:
        top_name = top_mfrs.iloc[0]["Manufacturer"] if not top_mfrs.empty else "N/A"
        top_share = top_mfrs.iloc[0]["Market_Share_%"] if not top_mfrs.empty else 0.0
        st.metric("Market Leader", f"{top_name}", f"{top_share}% share")
    with m3:
        st.metric("Leading Manufacturing Country", f"{country_data.iloc[0]['Manufacturing Country'] if not country_data.empty else 'N/A'}")
    with m4:
        st.metric("Average Satisfaction", f"{kpis['avg_rating']} ★")

    st.markdown("<br>", unsafe_allow_html=True)

    # Manufacturer Market Share Treemap
    st.markdown("##### 🗺️ Global Manufacturer Market Share Treemap")
    if not top_mfrs.empty:
        fig_treemap = px.treemap(
            top_mfrs,
            path=["Manufacturing Country", "Manufacturer"],
            values="Total_Sales",
            color="Avg_Rating",
            color_continuous_scale="Greens",
            hover_data={"Total_Sales": ":,", "Market_Share_%": ":.2f%", "Avg_Price": ":$,.0f"},
        )
        fig_treemap.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            height=380,
        )
        st.plotly_chart(fig_treemap, use_container_width=True)

    # Manufacturer Comparison Columns
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown("##### 🌐 Country-Wise Manufacturing Production")
        if not country_data.empty:
            fig_country = px.bar(
                country_data,
                x="Manufacturing Country",
                y="Total_Sales",
                color="Total_Sales",
                color_continuous_scale="Blues",
                text="Total_Sales",
                labels={"Total_Sales": "Units Sold"},
            )
            fig_country.update_traces(texttemplate="%{text:,.0s}", textposition="outside")
            fig_country.update_layout(
                template="plotly_white",
                height=380,
                xaxis_title="",
                yaxis_title="Total Units Sold",
            )
            st.plotly_chart(fig_country, use_container_width=True)

    with col_m2:
        st.markdown("##### ⭐ Customer Satisfaction vs. Average Vehicle Price")
        if not top_mfrs.empty:
            fig_bubble = px.scatter(
                top_mfrs,
                x="Avg_Price",
                y="Avg_Rating",
                size="Total_Sales",
                color="Manufacturing Country",
                hover_name="Manufacturer",
                hover_data={"Total_Sales": ":,", "Avg_Price": ":$,.0f", "Avg_Rating": ":.2f"},
                color_discrete_sequence=PALETTE["sequence"],
            )
            fig_bubble.update_layout(
                template="plotly_white",
                height=380,
                xaxis_title="Average Vehicle Price ($ USD)",
                yaxis_title="Customer Rating (out of 5.0)",
            )
            st.plotly_chart(fig_bubble, use_container_width=True)

    # Full Manufacturer Rankings Table
    st.markdown("##### 🏆 Complete Automaker Performance League Table")
    if not top_mfrs.empty:
        display_mfrs = top_mfrs[[
            "Rank",
            "Manufacturer",
            "Manufacturing Country",
            "Total_Sales",
            "Market_Share_%",
            "Total_Revenue",
            "Avg_Price",
            "Avg_Range",
            "Avg_Rating",
            "Models_Count",
        ]].rename(
            columns={
                "Manufacturing Country": "HQ Country",
                "Total_Sales": "Sales Units",
                "Market_Share_%": "Share (%)",
                "Total_Revenue": "Est Revenue ($)",
                "Avg_Price": "Avg Price ($)",
                "Avg_Range": "Avg Range (km)",
                "Avg_Rating": "Rating",
                "Models_Count": "Model Trims",
            }
        )
        st.dataframe(
            display_mfrs.style.format({
                "Sales Units": "{:,.0f}",
                "Share (%)": "{:.2f}%",
                "Est Revenue ($)": "${:,.0f}",
                "Avg Price ($)": "${:,.0f}",
                "Avg Range (km)": "{:.1f}",
                "Rating": "{:.2f} ★",
                "Model Trims": "{:d}",
            }),
            use_container_width=True,
            hide_index=True,
        )


# -----------------------------------------------------------------------------
# 9. VIEW E: SUSTAINABILITY ANALYSIS
# -----------------------------------------------------------------------------
elif selected_section == "🌱 Sustainability Analysis":
    st.markdown('<div class="section-header">🌱 Environmental Impact & Decarbonization Analysis</div>', unsafe_allow_html=True)

    sust_impact = an.calculate_sustainability_impact(df_filtered)

    # High Impact Environmental Equivalencies
    e1, e2, e3, e4 = st.columns(4)
    with e1:
        st.markdown(
            f"""
            <div class="kpi-container" style="border-left-color: #10B981;">
                <div class="kpi-label">CO2 Avoided Annually</div>
                <div class="kpi-value">{sust_impact['total_co2_tonnes'] / 1e6:.2f}M <span style="font-size:0.9rem;">Tonnes</span></div>
                <div class="kpi-subtext">Direct tailpipe displacement</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with e2:
        st.markdown(
            f"""
            <div class="kpi-container" style="border-left-color: #059669;">
                <div class="kpi-label">Tree Offset Equivalent</div>
                <div class="kpi-value">{sust_impact['trees_equivalent'] / 1e6:.1f}M <span style="font-size:0.9rem;">Trees</span></div>
                <div class="kpi-subtext">Annual tree carbon absorption</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with e3:
        st.markdown(
            f"""
            <div class="kpi-container" style="border-left-color: #0284C7;">
                <div class="kpi-label">Fuel Saved Equivalent</div>
                <div class="kpi-value">{sust_impact['gasoline_liters_saved'] / 1e9:.2f}B <span style="font-size:0.9rem;">Liters</span></div>
                <div class="kpi-subtext">Displaced fossil gasoline</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with e4:
        st.markdown(
            f"""
            <div class="kpi-container" style="border-left-color: #6366F1;">
                <div class="kpi-label">Avoided Coal Burning</div>
                <div class="kpi-value">{sust_impact['coal_kg_avoided'] / 1e9:.2f}B <span style="font-size:0.9rem;">kg</span></div>
                <div class="kpi-subtext">Equivalent coal generation saved</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Emissions Avoided by Category and Battery Tech
    scol1, scol2 = st.columns(2)
    with scol1:
        st.markdown("##### 🚗 Total Avoided CO2 Emissions by Vehicle Category")
        cat_co2 = sust_impact["category_co2"]
        if not cat_co2.empty:
            fig_co2_cat = px.bar(
                cat_co2,
                x="Vehicle Category",
                y="Total_CO2_Avoided_Tonnes",
                color="Avg_Per_Vehicle_CO2",
                color_continuous_scale="Greens",
                text="Total_CO2_Avoided_Tonnes",
                labels={
                    "Total_CO2_Avoided_Tonnes": "Fleet CO2 Avoided (Tonnes)",
                    "Avg_Per_Vehicle_CO2": "Per-Vehicle Avoidance (Tonnes/yr)",
                },
            )
            fig_co2_cat.update_traces(texttemplate="%{text:,.0s} T", textposition="outside")
            fig_co2_cat.update_layout(
                template="plotly_white",
                height=380,
                yaxis_title="Avoided CO2 (Tonnes/yr)",
                xaxis_title="",
            )
            st.plotly_chart(fig_co2_cat, use_container_width=True)

    with scol2:
        st.markdown("##### 🔋 CO2 Avoidance Impact Across Battery Chemistries")
        tech_co2 = sust_impact["tech_co2"]
        if not tech_co2.empty:
            fig_co2_tech = px.pie(
                tech_co2,
                names="Battery Technology",
                values="Total_CO2_Avoided_Tonnes",
                hole=0.45,
                color_discrete_sequence=PALETTE["sequence"],
            )
            fig_co2_tech.update_traces(textposition="inside", textinfo="percent+label")
            fig_co2_tech.update_layout(
                template="plotly_white",
                height=380,
                margin=dict(l=10, r=10, t=10, b=10),
            )
            st.plotly_chart(fig_co2_tech, use_container_width=True)

    # Interactive Fleet Sustainability What-If Simulator
    st.markdown("##### 🧮 Interactive 'What-If' EV Fleet Transition Simulator")
    st.markdown(
        """
        Simulate future fleet decarbonization by scaling current electric vehicle delivery targets:
        """
    )
    sim_col1, sim_col2 = st.columns([1, 1.5])
    with sim_col1:
        sim_multiplier = st.slider(
            "Fleet Adoption Scale Multiplier",
            min_value=0.5,
            max_value=5.0,
            value=1.5,
            step=0.1,
            help="Simulates scaling current sales volumes by a growth factor.",
        )
        sim_co2 = sust_impact["total_co2_tonnes"] * sim_multiplier
        sim_trees = sust_impact["trees_equivalent"] * sim_multiplier
        sim_gas = sust_impact["gasoline_liters_saved"] * sim_multiplier

        st.info(
            f"""
            **Simulated Impact Results ({sim_multiplier}x Fleet Scale):**
            - **Estimated Annual CO2 Avoided:** `{sim_co2 / 1e6:.2f} Million Tonnes`
            - **Equivalent Trees Sequestered:** `{sim_trees / 1e6:.1f} Million Mature Trees`
            - **Fossil Gasoline Displaced:** `{sim_gas / 1e9:.2f} Billion Liters`
            """
        )

    with sim_col2:
        # Comparison bar chart of Baseline vs Simulated
        sim_comparison = pd.DataFrame({
            "Scenario": ["Current Filtered Baseline", f"Simulated Scenario ({sim_multiplier}x)"],
            "CO2_Avoided_Million_Tonnes": [sust_impact["total_co2_tonnes"] / 1e6, sim_co2 / 1e6],
        })
        fig_sim = px.bar(
            sim_comparison,
            x="Scenario",
            y="CO2_Avoided_Million_Tonnes",
            color="Scenario",
            color_discrete_sequence=[PALETTE["navy"], PALETTE["primary"]],
            text="CO2_Avoided_Million_Tonnes",
        )
        fig_sim.update_traces(texttemplate="%{text:.2f}M Tonnes", textposition="outside")
        fig_sim.update_layout(
            template="plotly_white",
            height=280,
            showlegend=False,
            yaxis_title="Million Tonnes CO2 Avoided",
        )
        st.plotly_chart(fig_sim, use_container_width=True)

    # Detailed Assumptions & Methodology Accordion
    st.markdown("##### 📖 Carbon Accounting Methodology & Engineering Assumptions")
    with st.expander("Click to view full scientific calculation formula and data sources", expanded=False):
        assumptions = sust_impact["assumptions"]
        for title, desc in assumptions.items():
            st.markdown(f"**{title}**")
            st.markdown(f"> {desc}")
            st.markdown("---")
        st.markdown(
            """
            *Standards Reference:* US Environmental Protection Agency (EPA) GHG Equivalencies Calculator & 
            International Energy Agency (IEA) Global EV Outlook 2024 Lifecycle Assessment Guidelines.
            """
        )


# -----------------------------------------------------------------------------
# 10. VIEW F: DATA EXPLORER & QUALITY AUDIT
# -----------------------------------------------------------------------------
elif selected_section == "🔍 Data Explorer & Quality":
    st.markdown('<div class="section-header">🔍 Data Explorer & Pipeline Quality Audit</div>', unsafe_allow_html=True)

    # Data Quality Overview Cards
    q1, q2, q3, q4 = st.columns(4)
    with q1:
        st.metric("Initial Raw Rows", f"{data_audit['initial_rows']}")
    with q2:
        st.metric("Duplicates Cleaned", f"{data_audit['duplicates_removed']}")
    with q3:
        st.metric("Cleaned Ready Records", f"{data_audit['cleaned_rows']}")
    with q4:
        st.metric("Data Pipeline Health Score", f"{data_audit['health_score']}%", "Zero Missing Values")

    st.markdown("<br>", unsafe_allow_html=True)

    # Interactive Search & Column Filter
    st.markdown("##### 🔎 Filtered Catalog Records")
    
    search_query = st.text_input(
        "Search by Model, Manufacturer, or Country",
        placeholder="e.g., Tesla, BYD, India, LFP, Sedan...",
    )

    display_df = df_filtered.copy()
    if search_query:
        mask = (
            display_df["Vehicle Model"].str.contains(search_query, case=False, na=False)
            | display_df["Manufacturer"].str.contains(search_query, case=False, na=False)
            | display_df["Manufacturing Country"].str.contains(search_query, case=False, na=False)
            | display_df["Battery Technology"].str.contains(search_query, case=False, na=False)
            | display_df["Vehicle Category"].str.contains(search_query, case=False, na=False)
        )
        display_df = display_df[mask]

    # Select columns to display
    all_cols = list(display_df.columns)
    default_show_cols = [
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
    selected_cols = st.multiselect(
        "Customize Visible Columns",
        options=all_cols,
        default=default_show_cols,
    )

    st.dataframe(
        display_df[selected_cols],
        use_container_width=True,
        hide_index=True,
    )
    st.caption(f"Showing {len(display_df)} matching records.")

    # Export Buttons Row
    st.markdown("##### 📥 Export Dataset")
    exp_col1, exp_col2, _ = st.columns([1, 1, 2])

    # 1. Download as CSV
    csv_bytes = display_df.to_csv(index=False).encode("utf-8")
    with exp_col1:
        st.download_button(
            label="📥 Download Filtered CSV",
            data=csv_bytes,
            file_name="ev_market_filtered_data.csv",
            mime="text/csv",
            use_container_width=True,
        )

    # 2. Download as Excel
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        display_df.to_excel(writer, index=False, sheet_name="EV_Market_Data")
    excel_data = excel_buffer.getvalue()

    with exp_col2:
        st.download_button(
            label="📊 Download Filtered Excel (.xlsx)",
            data=excel_data,
            file_name="ev_market_filtered_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Data Quality Audit and Statistical Summary
    st.markdown("##### 🛡️ Data Quality & Statistical Summary")
    tab_stats, tab_audit, tab_corr = st.tabs(["📊 Descriptive Statistics", "🛠️ Cleaning Audit Log", "🔗 Feature Correlations"])

    with tab_stats:
        st.dataframe(
            df_filtered[dp.NUMERIC_COLUMNS].describe().round(2),
            use_container_width=True,
        )

    with tab_audit:
        audit_col1, audit_col2 = st.columns(2)
        with audit_col1:
            st.markdown("**Initial Missing Values Identified in Raw Data:**")
            null_summary = pd.DataFrame(list(data_audit["initial_nulls"].items()), columns=["Column", "Missing Count"])
            null_summary = null_summary[null_summary["Missing Count"] > 0]
            if not null_summary.empty:
                st.dataframe(null_summary, use_container_width=True, hide_index=True)
            else:
                st.success("No missing values found in raw source.")

        with audit_col2:
            st.markdown("**Cleaning Transformations Applied:**")
            st.markdown(
                f"""
                - **Deduplication:** Dropped `{data_audit['duplicates_removed']}` duplicate Vehicle IDs.
                - **Imputation:** Imputed `Charging Time (hours)` using median by vehicle segment.
                - **Imputation:** Imputed `Customer Rating` using automaker mean rating.
                - **Validation:** Bounded numeric columns within physical constraints.
                - **Feature Engineering:** Added `Energy Efficiency (km/kWh)`, `Price per Range ($/km)`, `Fleet Revenue ($)`, and `Total Fleet CO2 Avoided (Tonnes)`.
                """
            )

    with tab_corr:
        corr_matrix = an.get_correlation_matrix(df_filtered)
        if not corr_matrix.empty:
            fig_corr = px.imshow(
                corr_matrix,
                text_auto=True,
                color_continuous_scale="RdBu_r",
                zmin=-1,
                zmax=1,
                title="Pearson Feature Correlation Matrix",
            )
            fig_corr.update_layout(
                template="plotly_white",
                height=450,
            )
            st.plotly_chart(fig_corr, use_container_width=True)


# -----------------------------------------------------------------------------
# 11. FOOTER
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="custom-footer">
        <strong>Electric Vehicle (EV) Market Intelligence Platform</strong> | Transportation Domain Project Submission<br>
        Built with Streamlit, Plotly, Pandas, and NumPy | Ready for Streamlit Community Cloud Deployment
    </div>
    """,
    unsafe_allow_html=True,
)
