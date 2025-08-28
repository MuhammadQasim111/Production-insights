import pandas as pd
import numpy as np

# Load the data
data = pd.read_csv("production_data.csv")

# ---- Cleaning Step by Step ----

# 1. batch_id: must not have missing values (drop rows with missing batch_id)
data = data.dropna(subset=['batch_id'])

# 2. production_date: convert to datetime, invalid -> NaT
data['production_date'] = pd.to_datetime(data['production_date'], errors='coerce')

# 3. raw_material_supplier: categorical (1=national_supplier, 2=international_supplier)
data['raw_material_supplier'] = data['raw_material_supplier'].replace({1: 'national_supplier', 2: 'international_supplier'})
data['raw_material_supplier'] = data['raw_material_supplier'].fillna('national_supplier')

# 4. pigment_type: allowed ['type_a','type_b','type_c'], invalid -> 'other'
valid_pigments = ['type_a', 'type_b', 'type_c']
data['pigment_type'] = data['pigment_type'].where(data['pigment_type'].isin(valid_pigments), 'other')
data['pigment_type'] = data['pigment_type'].fillna('other')

# 5. pigment_quantity: continuous (1–100), missing -> median
data['pigment_quantity'] = pd.to_numeric(data['pigment_quantity'], errors='coerce')
data.loc[(data['pigment_quantity'] < 1) | (data['pigment_quantity'] > 100), 'pigment_quantity'] = np.nan
data['pigment_quantity'] = data['pigment_quantity'].fillna(data['pigment_quantity'].median())

# 6. mixing_time: continuous, missing -> mean (rounded to 2 decimals)
data['mixing_time'] = pd.to_numeric(data['mixing_time'], errors='coerce')
data['mixing_time'] = data['mixing_time'].fillna(data['mixing_time'].mean())
data['mixing_time'] = data['mixing_time'].round(2)

# 7. mixing_speed: categorical ['Low','Medium','High'], invalid/missing -> 'Not Specified'
valid_speeds = ['Low', 'Medium', 'High']
data['mixing_speed'] = data['mixing_speed'].where(data['mixing_speed'].isin(valid_speeds), 'Not Specified')
data['mixing_speed'] = data['mixing_speed'].fillna('Not Specified')

# 8. product_quality_score: continuous (1–10), missing -> mean (rounded to 2 decimals)
data['product_quality_score'] = pd.to_numeric(data['product_quality_score'], errors='coerce')
data.loc[(data['product_quality_score'] < 1) | (data['product_quality_score'] > 10), 'product_quality_score'] = np.nan
data['product_quality_score'] = data['product_quality_score'].fillna(data['product_quality_score'].mean())
data['product_quality_score'] = data['product_quality_score'].round(2)

# ---- Final Cleaned DataFrame ----
clean_data = data.copy()

# Show sample
print(clean_data.head())

