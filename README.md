# ⚡ Electric Vehicle (EV) Market Analysis Dashboard

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-5.18%2B-3F4F75.svg?logo=plotly&logoColor=white)](https://plotly.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)]()

> An interactive data analytics and business intelligence platform built for the transportation domain. Analyzes global electric vehicle adoption curves, manufacturer competitiveness, battery chemistry performance, driving range trade-offs, and fleet-scale carbon displacement.

---

## 🔗 Live Application & Repository Placeholders

- **Live Demo:** `https://<your-username>-ev-market-analysis.streamlit.app` *(Streamlit Community Cloud placeholder)*
- **GitHub Repository:** `https://github.com/<your-username>/EV-Market-Analysis-Dashboard` *(GitHub repository placeholder)*

---

## 📌 Executive Summary & Problem Statement

The global automotive landscape is undergoing a massive transformation from internal combustion engine (ICE) vehicles to electrified mobility systems. However, industry decision-makers—including **business analysts, market strategy directors, fleet procurement managers, and sustainability researchers**—face significant challenges when analyzing market dynamics:

1. **Fragmented Data Ecosystems:** Sales volumes, battery pack chemistries, range ratings, and charging durations are frequently siloed across disparate sources.
2. **Technological Trade-Offs:** Rapid advancements in battery chemistries (LFP vs. NMC vs. NCA vs. Sodium-Ion vs. Solid-State) require transparent benchmarking across energy density, charging speed, and price.
3. **Decarbonization Measurement:** Organizations struggle to quantify verifiable tailpipe carbon avoidance against real-world electric grid emissions factors.

This project delivers a responsive dashboard that harmonizes technical specifications and market performance metrics into actionable business intelligence.

---

## 🎯 Key Project Objectives

- **Market Adoption Tracking:** Evaluate annual sales progression and segment distribution across Hatchbacks, Sedans, SUVs, Commercial Trucks, Urban Transit Buses, and Two-Wheelers (2019–2025).
- **Automaker Benchmarking:** Analyze market concentration, unit volumes, revenue generation, customer satisfaction, and manufacturing footprints across 30+ global automakers.
- **Battery Chemistry Evaluation:** Compare energy storage performance, capacity vs. range correlation, charging speeds, and pack efficiency across key battery chemistries.
- **Environmental Impact Quantification:** Model tailpipe CO2 displacement, lifecycle emissions offset, and equivalent environmental indicators (mature trees sequestered, fossil gasoline gallons saved, coal combustion avoided).
- **Interactive Self-Service Exploration:** Provide real-time multi-dimensional filtering, free-text catalog search, and single-click export to CSV and Excel (`.xlsx`).

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **User Interface** | [Streamlit](https://streamlit.io/) (v1.35+) | Reactive, modern web dashboard with custom CSS theme |
| **Visualization** | [Plotly](https://plotly.com/) (v5.18+) | Interactive charts (line, stacked bar, treemap, donut, box plot, scatter) |
| **Data Cleaning & ETL** | [Pandas](https://pandas.pydata.org/) (v2.0+), [NumPy](https://numpy.org/) | Deduplication, imputation, feature engineering, and statistical aggregations |
| **File Formats** | CSV, [OpenPyXL](https://openpyxl.readthedocs.io/) | Data persistence, multi-format export support |
| **Testing** | Python Assertions & Pytest pattern | Automated validation of data schema, KPIs, filters, and exports |
| **Deployment** | [Streamlit Community Cloud](https://streamlit.io/cloud) | Cloud-native hosting directly integrated with GitHub |

---

## 📂 Project Architecture

```text
Electric Vehicle Market Performance/
│
├── .streamlit/
│   └── config.toml               # Streamlit UI theme and server configuration
│
├── data/
│   └── ev_market_data.csv        # Comprehensive raw EV market dataset (680+ records)
│
├── app.py                        # Main Streamlit web application & UI layouts
├── data_processing.py            # Data loading, validation, deduplication, imputation & feature engineering
├── analysis.py                   # Reusable analytical functions, KPIs, and carbon accounting models
├── generate_dataset.py           # Reproducible dataset generator script
├── test_app_logic.py             # Automated end-to-end test suite (10 test modules)
│
├── requirements.txt              # Production Python dependencies
├── .gitignore                    # Git exclusions (environments, caches, IDE configs)
└── README.md                     # Comprehensive project documentation
```

---

## 📊 Dataset Specifications & Data Quality Pipeline

### Schema Definition
The dataset contains **684 raw records** (679 unique records after automated deduplication) spanning **2019 through 2025**, covering 34 manufacturers and 6 major vehicle categories across 11 countries:

| Column Name | Data Type | Description / Units | Physical Bounds |
| :--- | :--- | :--- | :--- |
| `Vehicle ID` | String | Unique vehicle identification code | `EV-1001` to `EV-1684` |
| `Vehicle Model` | String | Commercial vehicle model & trim name | e.g., *Tesla Model Y*, *BYD Han EV* |
| `Manufacturer` | String | Global automaker brand | e.g., *Tesla, BYD, Hyundai, BMW* |
| `Vehicle Category` | String | Vehicle classification segment | *Hatchback, Sedan, SUV, Bus, Truck, Two-Wheeler* |
| `Manufacturing Country`| String | Country of primary assembly / headquarters | *USA, China, Germany, India, South Korea, etc.* |
| `Model Year` | Integer | Production model release year | `2019` – `2025` |
| `Annual Sales` | Integer | Annual unit deliveries | `500` – `520,000` units |
| `Battery Technology` | String | Battery pack chemistry | *LFP, NMC, NCA, Sodium-Ion, Solid-State* |
| `Battery Capacity (kWh)`| Float | Usable battery pack capacity | `2.5` – `753.0` kWh |
| `Driving Range (km)` | Integer | Real-world driving range on full charge | `75` – `850` km |
| `Charging Time (hours)` | Float | Standard full charge duration (AC/DC cycle) | `0.4` – `15.0` hours |
| `Vehicle Price` | Integer | Manufacturer's retail price (USD) | `$1,250` – `$580,000` |
| `Customer Rating` | Float | Verified customer satisfaction score | `1.0` – `5.0` (out of 5.0) |
| `Estimated CO2 Emissions Avoided` | Float | Per-vehicle tailpipe CO2 displacement (Tonnes/yr) | `0.6` – `64.0` Tonnes/year |

### Data Cleaning & Validation Pipeline (`data_processing.py`)
To demonstrate real-world enterprise data engineering practices, the raw dataset includes deliberate edge cases that are automatically resolved:
1. **Deduplication:** Detects and eliminates duplicate `Vehicle ID` rows, preserving record integrity.
2. **Missing Value Imputation:**
   - Missing `Charging Time (hours)` values are imputed using the **median of the corresponding Vehicle Category**.
   - Missing `Customer Rating` scores are imputed using the **manufacturer's average rating**.
3. **Range Validation:** Numeric fields are clamped within physical limits (e.g., rating $\in [1.0, 5.0]$, capacity $\ge 1.0\text{ kWh}$, price $\ge \$500$).
4. **Engineered Features:**
   - $\text{Energy Efficiency} = \frac{\text{Driving Range (km)}}{\text{Battery Capacity (kWh)}}$ ($\text{km/kWh}$)
   - $\text{Consumption} = \frac{\text{Battery Capacity (kWh)}}{\text{Driving Range (km)}} \times 100$ ($\text{kWh/100km}$)
   - $\text{Price per Range} = \frac{\text{Vehicle Price (\USD)}}{\text{Driving Range (km)}}$ ($\text{\$/km}$)
   - $\text{Fleet Revenue} = \text{Annual Sales} \times \text{Vehicle Price}$ ($\text{\USD}$)
   - $\text{Total Fleet CO2 Avoided} = \text{Annual Sales} \times \text{Per-Vehicle CO2 Avoided}$ ($\text{Tonnes/year}$)

> **⚠️ Sample Data Notice:** This dataset has been programmatically synthesized based on industry benchmarks (EPA, IEA, and OEM technical datasheets) for academic and analytical demonstration. It should not be interpreted as official corporate financial or regulatory filings.

---

## 🖥️ Dashboard Views & Analytics Modules

### 1. 📌 Executive Overview
- **Dynamic KPI Scorecard:** Total sales delivered, active manufacturers, fleet-wide average driving range, average customer rating, total vehicles analyzed, cumulative CO2 avoided, and gross market revenue.
- **Annual Sales Evolution:** Interactive bar and line combination chart depicting 2019–2025 adoption growth.
- **Category Sales Share Donut:** Percentage contribution of each vehicle segment to global deliveries.
- **Executive Strategic Takeaways:** High-level summary of market expansion, pricing dynamics, and segment leadership.

### 2. 📈 EV Sales Analysis
- **Annual Sales Progression by Category:** Stacked interactive time-series chart showing adoption velocity across vehicle types.
- **Category Volume & Average Price:** Dual-dimension bar chart mapping sales volumes against average retail pricing.
- **Top 10 Manufacturers:** Horizontal bar chart highlighting market leaders by volume and market share percentage.
- **Segment Breakdown League Table:** Tabular summary with vehicle count, sales volume, market share, and average range.

### 3. 🔋 Battery Technology Analysis
- **Chemistry Market Share:** Distribution breakdown across LFP (Lithium Iron Phosphate), NMC, NCA, Sodium-Ion, and Solid-State.
- **Capacity Benchmarks:** Average pack capacity (kWh) per chemistry.
- **Driving Range Distribution:** Interactive box plot highlighting range spreads, medians, and outlier boundaries.
- **Charging Time Box Plot:** Full-cycle charging duration comparisons.
- **Capacity vs. Range Scatter Plot:** Interactive scatter plot with bubble sizes weighted by annual sales, complete with hover tooltips detailing efficiency and pricing.

### 4. 🏭 Manufacturer Performance
- **Global Market Share Treemap:** Hierarchical visualization of market share grouped by Manufacturing Country and Automaker, color-coded by customer satisfaction.
- **Country-Wise Manufacturing Output:** Geographic distribution of total vehicle deliveries.
- **Customer Satisfaction vs. Retail Price:** Bubble plot exploring brand positioning, perceived value, and customer loyalty.
- **Comprehensive Automaker League Table:** Formatted ranking table with revenue estimates, unit volumes, and average ratings.

### 5. 🌱 Sustainability Analysis
- **Carbon Avoidance KPIs:** Total metric tonnes of tailpipe CO2 avoided per year.
- **Environmental Equivalencies:**
  - Mature tree absorption equivalents ($\sim 21.77\text{ kg CO}_2/\text{tree/year}$).
  - Displaced fossil gasoline liters and gallons ($\sim 2.31\text{ kg CO}_2/\text{liter}$).
  - Displaced coal-fired power generation ($\sim 2.42\text{ kg CO}_2/\text{kg coal}$).
- **Emissions Avoided by Segment & Chemistry:** Comparative bar and donut charts.
- **Interactive "What-If" Fleet Simulator:** Allows strategy directors to slide adoption targets ($0.5\times$ to $5.0\times$) and view instant emissions reductions.
- **Methodology Documentation:** Transparent explanation of carbon accounting baselines (EPA & IEA standards).

### 6. 🔍 Data Explorer & Quality Audit
- **Interactive Search:** Instant multi-column filtering across Model, Brand, Category, Country, and Battery Chemistry.
- **Column Customization:** Toggle visibility of catalog features.
- **Dual Format Export:** Single-click download buttons for **CSV** and **Excel (.xlsx)**.
- **Pipeline Quality Audit:** Real-time visibility into raw rows, duplicates dropped, imputation results, and data health scores ($100\%$).
- **Statistical Summaries & Correlation Matrix:** Descriptive statistics (`mean`, `std`, `min`, `max`, `quartiles`) and an interactive Pearson correlation heatmap.

---

## ⚡ Installation & Local Setup

Follow these steps to run the application locally on your workstation:

### Prerequisites
- Python 3.10, 3.11, 3.12, or 3.13 installed.
- Git installed on your system.

### Step 1: Clone the Repository
```bash
git clone https://github.com/<your-username>/EV-Market-Analysis-Dashboard.git
cd "EV-Market-Analysis-Dashboard"
```

### Step 2: Create and Activate a Virtual Environment
- **Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Automated Test Suite
Verify that all data pipelines, statistical calculations, and export generators work without issues:
```bash
python test_app_logic.py
```
*Expected output: `[SUCCESS] ALL 10 TEST SUITES PASSED FLAWLESSLY!`*

### Step 5: Launch the Streamlit Application
```bash
streamlit run app.py
```
The dashboard will open automatically in your browser at `http://localhost:8501`.

---

## 🚀 Deployment Guide: Streamlit Community Cloud

This project is configured for one-click deployment on **Streamlit Community Cloud**:

1. **Push Code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "feat: complete EV market performance analytics dashboard"
   git branch -M main
   git remote add origin https://github.com/<your-username>/EV-Market-Analysis-Dashboard.git
   git push -u origin main
   ```
2. **Access Streamlit Community Cloud:**
   - Navigate to [share.streamlit.io](https://share.streamlit.io/) and authenticate with your GitHub account.
3. **Configure New App:**
   - Click **"New app"**.
   - Select your repository: `<your-username>/EV-Market-Analysis-Dashboard`.
   - Set Branch to `main`.
   - Set Main file path to `app.py`.
4. **Deploy:**
   - Click **"Deploy!"**. Streamlit will install packages from `requirements.txt` and launch the live URL within 1–2 minutes.

---

## 📸 Dashboard Preview

| View | Description |
| :--- | :--- |
| **Executive Overview** | Metric cards with total deliveries, global manufacturers, average range, and annual sales area chart. |
| **Sales Analysis** | Interactive stacked bar chart displaying adoption across vehicle categories and top 10 automaker ranking. |
| **Battery Benchmarking** | Distribution donut, pack capacity bars, and range vs. capacity correlation scatter plot. |
| **Automaker Intelligence** | Global manufacturing treemap, customer satisfaction vs. price bubble plot, and automaker league table. |
| **Sustainability & Decarbonization**| Tailpipe carbon avoidance scorecard, equivalent tree/fuel savings, and interactive adoption multiplier. |
| **Data Explorer & Audit** | Searchable grid, custom column toggles, CSV/Excel downloads, and Pearson correlation heatmap. |

*(Screenshots can be stored in `docs/screenshots/` and referenced here after live deployment).*

---

## 📜 Scientific Methodology & Assumptions

The carbon avoidance calculations utilize established transportation life-cycle metrics:
- **ICE Baseline Emissions:** Standard tailpipe emissions from internal combustion engines: Passenger Cars ($170\text{ g CO}_2/\text{km}$), SUVs ($250\text{ g CO}_2/\text{km}$), Heavy Transit Buses ($1,350\text{ g CO}_2/\text{km}$), Commercial Trucks ($680\text{ g CO}_2/\text{km}$), Two-Wheelers ($52\text{ g CO}_2/\text{km}$).
- **EV Grid Carbon Intensity:** Factored at global average grid intensity of $\sim 430\text{ g CO}_2/\text{kWh}$, with $7\%$ transmission line loss and $88\%$ inverter charging efficiency.
- **Tree Offset Equivalency:** Based on US Environmental Protection Agency (EPA) standard: 1 mature urban tree sequesters $21.77\text{ kg CO}_2/\text{year}$ ($45.93\text{ trees}/\text{tonne CO}_2$).
- **Fossil Fuel Equivalency:** 1 liter of finished motor gasoline combustion produces $2.31\text{ kg CO}_2$ ($432.9\text{ liters}/\text{tonne CO}_2$).

---

## 📄 License

This project is distributed under the **MIT License**. See the `LICENSE` file for details.

---

## 👤 Author & Acknowledgments

- **Domain:** Transportation Analytics & Clean Energy Transition
- **Project Type:** Individual Comprehensive Analytics Project Submission
- **Built With:** Streamlit, Plotly, Pandas, NumPy, OpenPyXL
