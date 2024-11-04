import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the CSV file
file_path = 'D:\\University stuff\\upb\\S5\\KEPUTUSAN\\angket.csv'
data = pd.read_csv(file_path)

# Step 1: Rename columns to simpler names for easier access
data.columns = [
    'timestamp', 'nama', 'semester', 'laptop_digunakan', 
    'harga_kepentingan', 'cpu_kepentingan', 'ram_kepentingan', 'penyimpanan_kepentingan', 
    'gpu_kepentingan', 'baterai_kepentingan', 'berat_kepentingan', 'layar_kepentingan', 
    'resolusi_layar_kepentingan', 'harga_penilaian', 'cpu_penilaian', 'ram_penilaian', 
    'penyimpanan_penilaian', 'gpu_penilaian', 'baterai_penilaian', 'berat_penilaian', 
    'ukuran_layar_penilaian', 'resolusi_layar_penilaian', 'prioritas_utama', 
    'kisaran_harga_ideal', 'preferensi_performa'
]

# Step 2: Select criteria columns for analysis
criteria_columns = [
    'harga_penilaian', 'cpu_penilaian', 'ram_penilaian', 'penyimpanan_penilaian',
    'gpu_penilaian', 'baterai_penilaian', 'berat_penilaian', 'ukuran_layar_penilaian', 
    'resolusi_layar_penilaian'
]
criteria_data = data[criteria_columns]

# Step 3: Clean data by averaging multi-value entries
def clean_and_average(value):
    if isinstance(value, str) and ';' in value:
        values = [float(x) for x in value.split(';') if x.strip().isdigit()]
        return np.mean(values) if values else np.nan
    else:
        return float(value) if str(value).strip().isdigit() else np.nan

criteria_data_cleaned = criteria_data.applymap(clean_and_average)

# Step 4: Define Benefit and Cost Criteria
benefit_criteria = [col for col in criteria_data_cleaned.columns if "harga" not in col and "berat" not in col]
cost_criteria = [col for col in criteria_data_cleaned.columns if "harga" in col or "berat" in col]

# Step 5: Normalize Data
normalized_data = criteria_data_cleaned.copy()

# Normalize Benefit Criteria
for col in benefit_criteria:
    max_value = criteria_data_cleaned[col].max()
    normalized_data[col] = criteria_data_cleaned[col] / max_value if max_value else 0

# Normalize Cost Criteria
for col in cost_criteria:
    min_value = criteria_data_cleaned[col].min()
    normalized_data[col] = min_value / criteria_data_cleaned[col] if min_value else 0

# Step 6: Assign Weights to Each Criterion
weights = {
    'cpu_penilaian': 0.3,
    'ram_penilaian': 0.2,
    'penyimpanan_penilaian': 0.1,
    'baterai_penilaian': 0.15,
    'harga_penilaian': 0.1,
    'berat_penilaian': 0.05,
    'resolusi_layar_penilaian': 0.1
}

# Apply weights to normalized data
for col, weight in weights.items():
    if col in normalized_data.columns:
        normalized_data[col] *= weight

# Step 7: Calculate Final Score and Ranking
normalized_data['Score'] = normalized_data.sum(axis=1)
normalized_data['Rank'] = normalized_data['Score'].rank(ascending=False)

# Display final rankings
print(normalized_data[['Score', 'Rank']])

# Display cleaned, normalized, and weighted data for verification
print("Cleaned Data:\n", criteria_data_cleaned.head())
print("\nNormalized Data:\n", normalized_data.head())
print("\nData after applying weights:\n", normalized_data.head())

# Display all column names for further debugging if needed
print("Column names in the original dataset:\n", data.columns)
print("\nOriginal Data Preview:\n", data.head())

# Menemukan laptop dengan rank 1
top_rank = normalized_data[normalized_data['Rank'] == 1.0]
top_rank['kisaran_harga_ideal'] = data['kisaran_harga_ideal']

print("\nLaptop dengan peringkat 1 dan kisaran harga ideal:\n", top_rank[['Score', 'Rank', 'kisaran_harga_ideal']])

# Melihat distribusi kisaran harga yang dipilih
harga_distribusi = data['kisaran_harga_ideal'].value_counts()
print("\nDistribusi Kisaran Harga yang Dipilih Responden:\n", harga_distribusi)

# Visualisasi distribusi kisaran harga
plt.figure(figsize=(10, 6))
harga_distribusi.plot(kind='bar')
plt.title('Distribusi Kisaran Harga yang Dipilih Responden')
plt.xlabel('Kisaran Harga')
plt.ylabel('Jumlah Responden')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.show()
