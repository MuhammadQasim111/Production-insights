import pandas as pd
import numpy as np

# Load the original table
data = pd.read_csv("production_data.csv")

# --- Minimal cleaning relevant to this task ---
# Ensure supplier is numeric even if stored as strings with spaces, etc.
data['raw_material_supplier'] = pd.to_numeric(
    data['raw_material_supplier'].astype(str).str.strip(), errors='coerce'
)

# Ensure numeric types for calculations
data['pigment_quantity'] = pd.to_numeric(data['pigment_quantity'], errors='coerce')
data['product_quality_score'] = pd.to_numeric(data['product_quality_score'], errors='coerce')

# --- EXTRACT DATA BASED ON DIFFERENT CONDITIONS ---
# Condition 1: supplier equals 2
# Condition 2: pigment_quantity > 35
filtered = data.query("raw_material_supplier == 2 and pigment_quantity > 35")

# Compute required averages (rounded to 2 decimals)
avg_qty = round(filtered['pigment_quantity'].mean(), 2)
avg_score = round(filtered['product_quality_score'].mean(), 2)

# Build 1-row output DataFrame with required columns
pigment_data = pd.DataFrame({
    'raw_material_supplier': [2],
    'pigment_quantity': [avg_qty],
    'avg_product_quality_score': [avg_score]
})

print(pigment_data)
