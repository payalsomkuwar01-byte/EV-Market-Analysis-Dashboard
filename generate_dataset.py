"""
Dataset Generator for Electric Vehicle (EV) Market Performance Analysis.
Generates realistic sample data across 2019-2025 for individual project submission.
Total records: >650 records with realistic physical attributes and market metrics.
Includes sample duplicates and missing values for demonstrating data cleaning pipeline.
"""

import os
import random
import numpy as np
import pandas as pd

# Set deterministic seed for reproducibility
random.seed(42)
np.random.seed(42)

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# Comprehensive catalog of EV models, manufacturers, categories, and countries
vehicle_catalog = [
    # Two-Wheelers
    {"model": "Ola S1 Pro", "mfr": "Ola Electric", "cat": "Two-Wheeler", "country": "India", "tech": ["LFP", "NMC"], "cap_range": (3.5, 4.0), "range_range": (140, 185), "charge_range": (4.0, 6.5), "price_range": (1600, 1950), "co2_factor": 0.95},
    {"model": "Ola S1 Air", "mfr": "Ola Electric", "cat": "Two-Wheeler", "country": "India", "tech": ["LFP"], "cap_range": (2.8, 3.2), "range_range": (110, 135), "charge_range": (4.5, 5.5), "price_range": (1250, 1450), "co2_factor": 0.85},
    {"model": "Ather 450X", "mfr": "Ather Energy", "cat": "Two-Wheeler", "country": "India", "tech": ["NMC"], "cap_range": (3.2, 3.7), "range_range": (115, 150), "charge_range": (3.5, 5.5), "price_range": (1750, 2100), "co2_factor": 0.92},
    {"model": "Ather 450S", "mfr": "Ather Energy", "cat": "Two-Wheeler", "country": "India", "tech": ["LFP"], "cap_range": (2.7, 3.0), "range_range": (95, 120), "charge_range": (4.0, 6.0), "price_range": (1400, 1600), "co2_factor": 0.80},
    {"model": "TVS iQube ST", "mfr": "TVS Motor", "cat": "Two-Wheeler", "country": "India", "tech": ["LFP"], "cap_range": (3.4, 4.6), "range_range": (100, 145), "charge_range": (3.8, 5.0), "price_range": (1550, 1850), "co2_factor": 0.88},
    {"model": "Bajaj Chetak Premium", "mfr": "Bajaj Auto", "cat": "Two-Wheeler", "country": "India", "tech": ["NMC"], "cap_range": (2.9, 3.4), "range_range": (90, 125), "charge_range": (4.0, 5.0), "price_range": (1450, 1750), "co2_factor": 0.82},
    {"model": "Gogoro SuperSport", "mfr": "Gogoro", "cat": "Two-Wheeler", "country": "Taiwan", "tech": ["NMC", "Solid-State"], "cap_range": (3.0, 3.8), "range_range": (110, 160), "charge_range": (2.5, 4.0), "price_range": (2800, 3600), "co2_factor": 0.90},
    {"model": "Niu NQi GTS", "mfr": "Niu Technologies", "cat": "Two-Wheeler", "country": "China", "tech": ["LFP", "Sodium-Ion"], "cap_range": (3.0, 4.2), "range_range": (90, 130), "charge_range": (4.5, 6.0), "price_range": (2900, 3700), "co2_factor": 0.85},
    {"model": "Zero SR/F", "mfr": "Zero Motorcycles", "cat": "Two-Wheeler", "country": "USA", "tech": ["NMC"], "cap_range": (14.4, 17.3), "range_range": (190, 260), "charge_range": (2.0, 4.5), "price_range": (18500, 22500), "co2_factor": 1.45},
    {"model": "LiveWire ONE", "mfr": "LiveWire", "cat": "Two-Wheeler", "country": "USA", "tech": ["NMC"], "cap_range": (15.0, 16.0), "range_range": (175, 235), "charge_range": (1.8, 4.0), "price_range": (21000, 24000), "co2_factor": 1.40},

    # Hatchbacks
    {"model": "Nissan Leaf SV", "mfr": "Nissan", "cat": "Hatchback", "country": "Japan", "tech": ["LFP", "NMC"], "cap_range": (40.0, 60.0), "range_range": (240, 350), "charge_range": (6.5, 8.5), "price_range": (28000, 36000), "co2_factor": 2.9},
    {"model": "Renault Zoe E-Tech", "mfr": "Renault", "cat": "Hatchback", "country": "France", "tech": ["NMC"], "cap_range": (52.0, 54.0), "range_range": (340, 395), "charge_range": (6.0, 8.0), "price_range": (31000, 38000), "co2_factor": 3.1},
    {"model": "Fiat 500e", "mfr": "Stellantis", "cat": "Hatchback", "country": "Italy", "tech": ["NMC"], "cap_range": (24.0, 42.0), "range_range": (180, 320), "charge_range": (4.5, 6.5), "price_range": (26000, 34000), "co2_factor": 2.6},
    {"model": "Volkswagen ID.3 Pro", "mfr": "Volkswagen", "cat": "Hatchback", "country": "Germany", "tech": ["NMC"], "cap_range": (58.0, 77.0), "range_range": (390, 520), "charge_range": (6.5, 8.5), "price_range": (37000, 46000), "co2_factor": 3.4},
    {"model": "BYD Dolphin Standard", "mfr": "BYD", "cat": "Hatchback", "country": "China", "tech": ["LFP", "Sodium-Ion"], "cap_range": (44.9, 60.4), "range_range": (310, 427), "charge_range": (5.5, 7.5), "price_range": (21000, 29000), "co2_factor": 3.0},
    {"model": "MG4 EV Trophy", "mfr": "SAIC", "cat": "Hatchback", "country": "China", "tech": ["LFP", "NMC"], "cap_range": (51.0, 64.0), "range_range": (350, 450), "charge_range": (5.5, 7.5), "price_range": (27000, 35000), "co2_factor": 3.2},
    {"model": "Peugeot e-208 GT", "mfr": "Peugeot", "cat": "Hatchback", "country": "France", "tech": ["NMC"], "cap_range": (50.0, 52.0), "range_range": (340, 400), "charge_range": (6.0, 7.5), "price_range": (33000, 41000), "co2_factor": 3.1},
    {"model": "Tata Tiago EV", "mfr": "Tata Motors", "cat": "Hatchback", "country": "India", "tech": ["LFP"], "cap_range": (19.2, 24.0), "range_range": (220, 290), "charge_range": (4.0, 6.5), "price_range": (11500, 15000), "co2_factor": 2.4},
    {"model": "Mini Electric Cooper", "mfr": "BMW", "cat": "Hatchback", "country": "Germany", "tech": ["NMC"], "cap_range": (32.6, 54.2), "range_range": (215, 380), "charge_range": (4.5, 7.0), "price_range": (34000, 43000), "co2_factor": 2.8},
    {"model": "Citroen e-C3", "mfr": "Stellantis", "cat": "Hatchback", "country": "France", "tech": ["LFP"], "cap_range": (29.2, 44.0), "range_range": (280, 340), "charge_range": (5.0, 7.5), "price_range": (16000, 24000), "co2_factor": 2.7},

    # Sedans
    {"model": "Tesla Model 3 Long Range", "mfr": "Tesla", "cat": "Sedan", "country": "USA", "tech": ["NCA", "NMC", "LFP"], "cap_range": (60.0, 82.0), "range_range": (490, 630), "charge_range": (6.0, 8.5), "price_range": (38000, 52000), "co2_factor": 4.3},
    {"model": "Tesla Model S Plaid", "mfr": "Tesla", "cat": "Sedan", "country": "USA", "tech": ["NCA"], "cap_range": (95.0, 100.0), "range_range": (580, 650), "charge_range": (8.0, 10.5), "price_range": (85000, 108000), "co2_factor": 4.9},
    {"model": "BYD Han EV Flagship", "mfr": "BYD", "cat": "Sedan", "country": "China", "tech": ["LFP"], "cap_range": (65.0, 85.4), "range_range": (500, 610), "charge_range": (6.5, 8.5), "price_range": (34000, 47000), "co2_factor": 4.1},
    {"model": "BYD Seal AWD", "mfr": "BYD", "cat": "Sedan", "country": "China", "tech": ["LFP"], "cap_range": (61.4, 82.5), "range_range": (480, 570), "charge_range": (6.0, 8.0), "price_range": (33000, 45000), "co2_factor": 4.0},
    {"model": "Hyundai Ioniq 6 SE", "mfr": "Hyundai", "cat": "Sedan", "country": "South Korea", "tech": ["NMC"], "cap_range": (53.0, 77.4), "range_range": (460, 614), "charge_range": (6.0, 8.0), "price_range": (41000, 54000), "co2_factor": 4.2},
    {"model": "BMW i4 eDrive40", "mfr": "BMW", "cat": "Sedan", "country": "Germany", "tech": ["NMC"], "cap_range": (70.2, 83.9), "range_range": (460, 590), "charge_range": (7.0, 9.0), "price_range": (55000, 72000), "co2_factor": 4.5},
    {"model": "Mercedes-Benz EQE 350+", "mfr": "Mercedes-Benz", "cat": "Sedan", "country": "Germany", "tech": ["NMC"], "cap_range": (90.6, 96.0), "range_range": (520, 650), "charge_range": (8.0, 10.5), "price_range": (74000, 92000), "co2_factor": 4.8},
    {"model": "Lucid Air Grand Touring", "mfr": "Lucid", "cat": "Sedan", "country": "USA", "tech": ["NMC", "Solid-State"], "cap_range": (92.0, 118.0), "range_range": (650, 820), "charge_range": (8.5, 12.0), "price_range": (88000, 138000), "co2_factor": 5.2},
    {"model": "Porsche Taycan 4S", "mfr": "Porsche", "cat": "Sedan", "country": "Germany", "tech": ["NMC"], "cap_range": (79.2, 105.0), "range_range": (420, 560), "charge_range": (7.5, 9.5), "price_range": (95000, 145000), "co2_factor": 4.9},
    {"model": "XPeng P7i", "mfr": "XPeng", "cat": "Sedan", "country": "China", "tech": ["LFP", "NMC"], "cap_range": (60.2, 86.2), "range_range": (480, 620), "charge_range": (6.0, 8.5), "price_range": (32000, 44000), "co2_factor": 4.0},
    {"model": "NIO ET7", "mfr": "NIO", "cat": "Sedan", "country": "China", "tech": ["NMC", "Solid-State"], "cap_range": (75.0, 150.0), "range_range": (530, 850), "charge_range": (7.0, 11.0), "price_range": (58000, 79000), "co2_factor": 4.7},
    {"model": "Polestar 2 Dual Motor", "mfr": "Volvo", "cat": "Sedan", "country": "Sweden", "tech": ["NMC"], "cap_range": (69.0, 82.0), "range_range": (470, 595), "charge_range": (7.0, 8.5), "price_range": (49000, 63000), "co2_factor": 4.3},

    # SUVs
    {"model": "Tesla Model Y Performance", "mfr": "Tesla", "cat": "SUV", "country": "USA", "tech": ["NCA", "NMC", "LFP"], "cap_range": (60.0, 82.0), "range_range": (440, 533), "charge_range": (6.5, 8.5), "price_range": (44000, 58000), "co2_factor": 4.6},
    {"model": "BYD Atto 3 Superior", "mfr": "BYD", "cat": "SUV", "country": "China", "tech": ["LFP"], "cap_range": (49.9, 60.5), "range_range": (380, 450), "charge_range": (6.0, 8.0), "price_range": (28000, 38000), "co2_factor": 4.0},
    {"model": "BYD Tang EV", "mfr": "BYD", "cat": "SUV", "country": "China", "tech": ["LFP"], "cap_range": (86.4, 108.8), "range_range": (450, 560), "charge_range": (8.0, 10.5), "price_range": (42000, 56000), "co2_factor": 4.8},
    {"model": "Volkswagen ID.4 Pro AWD", "mfr": "Volkswagen", "cat": "SUV", "country": "Germany", "tech": ["NMC"], "cap_range": (62.0, 82.0), "range_range": (380, 480), "charge_range": (6.5, 8.5), "price_range": (39000, 53000), "co2_factor": 4.4},
    {"model": "Hyundai Ioniq 5 Limited", "mfr": "Hyundai", "cat": "SUV", "country": "South Korea", "tech": ["NMC"], "cap_range": (58.0, 84.0), "range_range": (390, 507), "charge_range": (5.5, 7.5), "price_range": (42000, 57000), "co2_factor": 4.5},
    {"model": "Kia EV6 GT-Line", "mfr": "Kia", "cat": "SUV", "country": "South Korea", "tech": ["NMC"], "cap_range": (58.0, 77.4), "range_range": (400, 528), "charge_range": (5.5, 7.5), "price_range": (43000, 59000), "co2_factor": 4.5},
    {"model": "Ford Mustang Mach-E Premium", "mfr": "Ford", "cat": "SUV", "country": "USA", "tech": ["NMC", "LFP"], "cap_range": (70.0, 91.0), "range_range": (390, 510), "charge_range": (7.0, 9.5), "price_range": (43000, 62000), "co2_factor": 4.7},
    {"model": "Rivian R1S Adventure", "mfr": "Rivian", "cat": "SUV", "country": "USA", "tech": ["NMC"], "cap_range": (105.0, 149.0), "range_range": (450, 640), "charge_range": (9.0, 13.0), "price_range": (76000, 98000), "co2_factor": 5.4},
    {"model": "BMW iX xDrive50", "mfr": "BMW", "cat": "SUV", "country": "Germany", "tech": ["NMC"], "cap_range": (76.6, 111.5), "range_range": (440, 630), "charge_range": (8.5, 12.0), "price_range": (84000, 112000), "co2_factor": 5.3},
    {"model": "Mercedes-Benz EQE SUV", "mfr": "Mercedes-Benz", "cat": "SUV", "country": "Germany", "tech": ["NMC"], "cap_range": (89.0, 96.0), "range_range": (450, 560), "charge_range": (8.0, 10.5), "price_range": (78000, 99000), "co2_factor": 5.1},
    {"model": "Tata Nexon EV Max", "mfr": "Tata Motors", "cat": "SUV", "country": "India", "tech": ["LFP"], "cap_range": (30.2, 40.5), "range_range": (312, 453), "charge_range": (5.5, 7.5), "price_range": (17500, 24000), "co2_factor": 3.7},
    {"model": "Tata Curvv EV", "mfr": "Tata Motors", "cat": "SUV", "country": "India", "tech": ["LFP"], "cap_range": (45.0, 55.0), "range_range": (420, 502), "charge_range": (6.0, 7.5), "price_range": (21000, 27000), "co2_factor": 3.9},
    {"model": "Volvo EX30 Ultra", "mfr": "Volvo", "cat": "SUV", "country": "Sweden", "tech": ["LFP", "NMC"], "cap_range": (51.0, 69.0), "range_range": (340, 475), "charge_range": (5.5, 8.0), "price_range": (36000, 48000), "co2_factor": 4.1},
    {"model": "NIO ES6 Performance", "mfr": "NIO", "cat": "SUV", "country": "China", "tech": ["NMC", "Solid-State"], "cap_range": (75.0, 100.0), "range_range": (465, 625), "charge_range": (7.0, 9.5), "price_range": (52000, 68000), "co2_factor": 4.8},

    # Trucks
    {"model": "Ford F-150 Lightning Lariat", "mfr": "Ford", "cat": "Truck", "country": "USA", "tech": ["NMC"], "cap_range": (98.0, 131.0), "range_range": (370, 515), "charge_range": (8.5, 12.5), "price_range": (58000, 84000), "co2_factor": 11.2},
    {"model": "Tesla Cybertruck Dual Motor", "mfr": "Tesla", "cat": "Truck", "country": "USA", "tech": ["NMC", "NCA"], "cap_range": (123.0, 128.0), "range_range": (480, 547), "charge_range": (9.0, 13.0), "price_range": (79000, 102000), "co2_factor": 11.8},
    {"model": "Rivian R1T Dual Motor", "mfr": "Rivian", "cat": "Truck", "country": "USA", "tech": ["NMC", "LFP"], "cap_range": (105.0, 149.0), "range_range": (430, 660), "charge_range": (8.5, 12.0), "price_range": (72000, 94000), "co2_factor": 11.5},
    {"model": "Chevrolet Silverado EV WT", "mfr": "General Motors", "cat": "Truck", "country": "USA", "tech": ["NMC"], "cap_range": (170.0, 205.0), "range_range": (510, 720), "charge_range": (10.0, 15.0), "price_range": (74000, 96000), "co2_factor": 12.4},
    {"model": "Volvo FM Electric Heavy", "mfr": "Volvo", "cat": "Truck", "country": "Sweden", "tech": ["NMC", "LFP"], "cap_range": (180.0, 360.0), "range_range": (300, 480), "charge_range": (7.0, 11.0), "price_range": (195000, 280000), "co2_factor": 26.5},
    {"model": "Scania 25 P Electric", "mfr": "Scania", "cat": "Truck", "country": "Sweden", "tech": ["NMC"], "cap_range": (165.0, 300.0), "range_range": (250, 400), "charge_range": (6.5, 10.0), "price_range": (180000, 260000), "co2_factor": 24.0},
    {"model": "Mercedes-Benz eActros 300", "mfr": "Mercedes-Benz", "cat": "Truck", "country": "Germany", "tech": ["LFP", "NMC"], "cap_range": (210.0, 336.0), "range_range": (300, 420), "charge_range": (7.5, 11.5), "price_range": (210000, 290000), "co2_factor": 25.0},
    {"model": "Nikola Tre BEV", "mfr": "Nikola", "cat": "Truck", "country": "USA", "tech": ["NMC"], "cap_range": (500.0, 753.0), "range_range": (420, 530), "charge_range": (3.5, 6.0), "price_range": (290000, 370000), "co2_factor": 32.0},

    # Buses
    {"model": "BYD K9 Electric Transit", "mfr": "BYD", "cat": "Bus", "country": "China", "tech": ["LFP"], "cap_range": (324.0, 422.0), "range_range": (270, 380), "charge_range": (3.5, 6.0), "price_range": (340000, 460000), "co2_factor": 58.0},
    {"model": "Yutong E12 CityBus", "mfr": "Yutong", "cat": "Bus", "country": "China", "tech": ["LFP"], "cap_range": (280.0, 422.0), "range_range": (260, 390), "charge_range": (3.0, 5.5), "price_range": (320000, 440000), "co2_factor": 56.0},
    {"model": "Proterra ZX5 Max", "mfr": "Proterra", "cat": "Bus", "country": "USA", "tech": ["NMC"], "cap_range": (350.0, 675.0), "range_range": (310, 520), "charge_range": (3.5, 6.0), "price_range": (420000, 580000), "co2_factor": 64.0},
    {"model": "Volvo 7900 Electric", "mfr": "Volvo", "cat": "Bus", "country": "Sweden", "tech": ["NMC", "LFP"], "cap_range": (264.0, 470.0), "range_range": (240, 400), "charge_range": (4.0, 6.5), "price_range": (380000, 510000), "co2_factor": 55.0},
    {"model": "Mercedes-Benz eCitaro", "mfr": "Mercedes-Benz", "cat": "Bus", "country": "Germany", "tech": ["NMC", "Solid-State"], "cap_range": (292.0, 490.0), "range_range": (260, 410), "charge_range": (4.0, 6.5), "price_range": (410000, 550000), "co2_factor": 57.0},
    {"model": "Tata Starbus EV 12m", "mfr": "Tata Motors", "cat": "Bus", "country": "India", "tech": ["LFP"], "cap_range": (200.0, 310.0), "range_range": (200, 300), "charge_range": (3.0, 5.0), "price_range": (180000, 240000), "co2_factor": 48.0},
    {"model": "Solaris Urbino 12 Electric", "mfr": "Solaris", "cat": "Bus", "country": "Poland", "tech": ["LFP", "NMC"], "cap_range": (280.0, 400.0), "range_range": (250, 360), "charge_range": (3.5, 5.5), "price_range": (350000, 470000), "co2_factor": 53.0},
]

records = []
current_id = 1001
years = [2019, 2020, 2021, 2022, 2023, 2024, 2025]

# Category sales scale multipliers to create realistic volume
sales_volume_base = {
    "Two-Wheeler": (25000, 210000),
    "Hatchback": (18000, 160000),
    "Sedan": (15000, 340000),
    "SUV": (22000, 460000),
    "Truck": (4000, 48000),
    "Bus": (800, 14000),
}

# Year-over-year EV growth curve factor
year_growth = {
    2019: 0.38,
    2020: 0.52,
    2021: 0.78,
    2022: 1.00,
    2023: 1.28,
    2024: 1.54,
    2025: 1.76,
}

# Generate records
# For each catalog vehicle and each year, generate 1 to 3 trim/market variants to produce 700+ rows
for v in vehicle_catalog:
    cat = v["cat"]
    base_min, base_max = sales_volume_base[cat]
    
    for yr in years:
        # Determine variants per year (e.g., 2 variants per year for high-volume, 1-2 for others)
        num_variants = 2 if cat in ["SUV", "Sedan", "Two-Wheeler"] else 1
        
        for variant_idx in range(num_variants):
            veh_id = f"EV-{current_id}"
            current_id += 1
            
            # Select battery tech
            tech = random.choice(v["tech"])
            
            # Technology maturity and improvements over years
            tech_maturity_bonus = 1.0 + (yr - 2019) * 0.028
            
            # Battery Capacity
            cap = round(random.uniform(*v["cap_range"]) * tech_maturity_bonus, 1)
            
            # Driving Range (km) correlated to capacity with slight noise
            base_range = random.uniform(*v["range_range"])
            # Newer years and mature chemistries yield slightly better efficiency
            rng = int(base_range * tech_maturity_bonus * random.uniform(0.96, 1.04))
            
            # Charging Time (hours) decreases slightly over time as charging speeds improve
            base_charge = random.uniform(*v["charge_range"])
            charge_time = round(max(0.5, base_charge * (1.0 - (yr - 2019) * 0.04) * random.uniform(0.95, 1.05)), 2)
            
            # Price trend: prices soften slightly or adjust with inflation/capacity
            base_price = random.uniform(*v["price_range"])
            price = int(base_price * (1.0 + (yr - 2021) * 0.015) * random.uniform(0.96, 1.04))
            
            # Annual Sales
            growth = year_growth[yr]
            raw_sales = int(random.uniform(base_min, base_max) * growth)
            
            # Model specific boosts (e.g. Model Y, Dolphin, S1 Pro are mass leaders)
            if "Model Y" in v["model"] or "Model 3" in v["model"]:
                raw_sales = int(raw_sales * 1.6)
            elif "Dolphin" in v["model"] or "Atto 3" in v["model"]:
                raw_sales = int(raw_sales * 1.4)
            elif "Ola S1" in v["model"] or "Nexon EV" in v["model"]:
                raw_sales = int(raw_sales * 1.3)
            
            sales = max(500, raw_sales)
            
            # Customer Rating (3.5 to 4.9)
            rating = round(random.uniform(3.7, 4.9), 1)
            
            # Estimated CO2 Emissions Avoided per vehicle (tonnes/year)
            # Calculated based on fossil fuel replacement:
            # Baseline emission avoided per vehicle * efficiency adjustment
            co2_avoided_per_veh = round(v["co2_factor"] * random.uniform(0.95, 1.08), 2)
            
            # Model variant label
            if num_variants > 1:
                variant_name = f"{v['model']} Standard" if variant_idx == 0 else f"{v['model']} Extended"
            else:
                variant_name = v["model"]
                
            records.append({
                "Vehicle ID": veh_id,
                "Vehicle Model": variant_name,
                "Manufacturer": v["mfr"],
                "Vehicle Category": cat,
                "Manufacturing Country": v["country"],
                "Model Year": yr,
                "Annual Sales": sales,
                "Battery Technology": tech,
                "Battery Capacity (kWh)": cap,
                "Driving Range (km)": rng,
                "Charging Time (hours)": charge_time,
                "Vehicle Price": price,
                "Customer Rating": rating,
                "Estimated CO2 Emissions Avoided": co2_avoided_per_veh,
            })

df = pd.DataFrame(records)
print(f"Generated {len(df)} initial clean records.")

# Introduce sample data cleaning challenges (duplicates and missing values) to demonstrate data cleaning pipeline
# 1. Duplicate 5 records exactly
duplicates_to_add = df.sample(n=5, random_state=101)
df_with_issues = pd.concat([df, duplicates_to_add], ignore_index=True)

# 2. Introduce 6 missing values in Charging Time (hours)
null_indices_charge = df_with_issues.sample(n=6, random_state=202).index
df_with_issues.loc[null_indices_charge, "Charging Time (hours)"] = np.nan

# 3. Introduce 5 missing values in Customer Rating
null_indices_rating = df_with_issues.sample(n=5, random_state=303).index
df_with_issues.loc[null_indices_rating, "Customer Rating"] = np.nan

# Save raw CSV
output_path = os.path.join("data", "ev_market_data.csv")
df_with_issues.to_csv(output_path, index=False)
print(f"Saved {len(df_with_issues)} records to {output_path} with deliberate sample cleaning challenges.")
