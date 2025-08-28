import pandas as pd
import numpy as np

# Load raw data
data = pd.read_csv("production_data.csv")

# ---- Cleaning ----
data = data.dropna(subset=['batch_id'])
data['production_date'] = pd.to_datetime(data['production_date'], errors='coerce')

# raw_material_supplier
data['raw_material_supplier'] = data['raw_material_supplier'].replace({1: 'national_supplier', 2: 'international_supplier'})
data['raw_material_supplier'] = data['raw_material_supplier'].fillna('national_supplier')

# pigment_quantity
data['pigment_quantity'] = pd.to_numeric(data['pigment_quantity'], errors='coerce')
data.loc[(data['pigment_quantity'] < 1) | (data['pigment_quantity'] > 100), 'pigment_quantity'] = np.nan
data['pigment_quantity'] = data['pigment_quantity'].fillna(data['pigment_quantity'].median())

# product_quality_score
data['product_quality_score'] = pd.to_numeric(data['product_quality_score'], errors='coerce')
data.loc[(data['product_quality_score'] < 1) | (data['product_quality_score'] > 10), 'product_quality_score'] = np.nan
data['product_quality_score'] = data['product_quality_score'].fillna(data['product_quality_score'].mean()).round(2)

# ---- Stats ----
pq_mean = round(data['pigment_quantity'].mean(), 2)
pq_sd   = round(data['pigment_quantity'].std(), 2)
pqs_mean = round(data['product_quality_score'].mean(), 2)
pqs_sd   = round(data['product_quality_score'].std(), 2)

# Pearson correlation
corr = round(data[['pigment_quantity', 'product_quality_score']].corr().iloc[0,1], 2)

# ---- Output DataFrame ----
product_quality = pd.DataFrame([{
    'product_quality_score_mean': pqs_mean,
    'product_quality_score_sd': pqs_sd,
    'pigment_quantity_mean': pq_mean,
    'pigment_quantity_sd': pq_sd,
    'corr_coef': corr
}])

print(product_quality)

