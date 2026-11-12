import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. 12-Row Dataset Direct Code Ke Andar (No external file error!)
raw_data = {
    'sku_id': [501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512],
    'store_zone': ['Dwarka Sec-14', 'Greater Noida KP-3', 'Janakpuri West', 'Rohini Sec-7', 
                   'Dwarka Sec-14', 'Saket Select', 'Greater Noida KP-3', 'Janakpuri West', 
                   'Rohini Sec-7', 'Saket Select', 'Dwarka Sec-14', 'Greater Noida KP-3'],
    'product_name': ['Greek Yogurt 400g', 'Multigrain Bread', 'Avocado Imported', 'Cold Brew Can', 
                     'Paneer Fresh 200g', 'Blueberry Box', 'Whey Protein Sachet', 'Garlic Herb Butter', 
                     'Sourdough Loaf', 'Almond Milk 1L', 'ON Creatine 100g', 'Protein Bar Choco'],
    'category': ['Dairy', 'Bakery', 'Fruits & Veg', 'Beverages', 'Dairy', 'Fruits & Veg', 
                 'Health', 'Dairy', 'Bakery', 'Beverages', 'Health', 'Health'],
    'unit_cost': [65, 55, 180, 90, 85, 220, 140, 75, 110, 240, 450, 60],
    'system_stock': [120, 200, 60, 150, 180, 80, 100, 90, 70, 110, 40, 220],
    'actual_physical_stock': [95, 190, 42, 125, None, 58, 68, 88, 64, 82, 24, 175],
    'expired_units_dumped': [18, 45, 22, 5, 32, 28, 0, None, 25, 8, 0, 0],
    'ghost_order_cancels': [14, 4, 11, 19, 2, 16, 24, 1, 3, 21, 15, 28],
    'days_to_expiry': [1, 1, 2, 15, 1, 1, 60, 4, 1, 10, 365, 45]
}

df = pd.DataFrame(raw_data)

# 2. Data Cleaning (Missing values fill karna)
df['actual_physical_stock'] = df['actual_physical_stock'].fillna(df['system_stock'])
df['expired_units_dumped'] = df['expired_units_dumped'].fillna(0)

# 3. Feature Engineering (Loss calculate karna)
df['ghost_missing_units'] = df['system_stock'] - df['actual_physical_stock']
df['shrinkage_loss_inr'] = df['ghost_missing_units'] * df['unit_cost']
df['expiry_loss_inr'] = df['expired_units_dumped'] * df['unit_cost']

# 4. Automated Flash Sale Logic
df['action_trigger'] = df['days_to_expiry'].apply(
    lambda x: 'Trigger 30% Flash Sale' if x <= 2 else 'Normal Pricing'
)

# 5. Save Clean CSV for Excel & Power BI on Desktop
df.to_csv('cleaned_dark_store_data.csv', index=False)

print("=== DARK STORE AUDIT REPORT ===")
print(df[['product_name', 'store_zone', 'shrinkage_loss_inr', 'expiry_loss_inr', 'action_trigger']].to_string(index=False))

# 6. Correlation Heatmap
plt.figure(figsize=(8, 5))
numeric_cols = df[['system_stock', 'ghost_missing_units', 'ghost_order_cancels', 'shrinkage_loss_inr', 'expiry_loss_inr']]
sns.heatmap(numeric_cols.corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Dark Store Shrinkage & Order Cancellation Correlation')
plt.tight_layout()
plt.savefig('heatmap.png')
print("\n[SUCCESS] CSV and heatmap.png saved! Opening chart window...")
plt.show()