import pandas as pd
import numpy as np

# Load the survey data
survey_file_path = 'D:\\University stuff\\upb\\S5\\KEPUTUSAN\\angket.csv'
angket_data = pd.read_csv(survey_file_path)

# Rename columns in survey data for easier access
angket_data.columns = [
    'timestamp', 'nama', 'semester', 'laptop_digunakan', 
    'harga_kepentingan', 'cpu_kepentingan', 'ram_kepentingan', 'penyimpanan_kepentingan', 
    'gpu_kepentingan', 'baterai_kepentingan', 'berat_kepentingan', 'layar_kepentingan', 
    'resolusi_layar_kepentingan', 'harga_penilaian', 'cpu_penilaian', 'ram_penilaian', 
    'penyimpanan_penilaian', 'gpu_penilaian', 'baterai_penilaian', 'berat_penilaian', 
    'ukuran_layar_penilaian', 'resolusi_layar_penilaian', 'prioritas_utama', 
    'kisaran_harga_ideal', 'preferensi_performa'
]

# Clean and average multi-value entries for importance ratings
def clean_and_average(value):
    if isinstance(value, str) and ';' in value:
        values = [float(x) for x in value.split(';') if x.strip().isdigit()]
        return np.mean(values) if values else np.nan
    else:
        return float(value) if str(value).strip().isdigit() else np.nan

angket_data['harga_kepentingan'] = angket_data['harga_kepentingan'].apply(clean_and_average)
angket_data['cpu_kepentingan'] = angket_data['cpu_kepentingan'].apply(clean_and_average)
angket_data['ram_kepentingan'] = angket_data['ram_kepentingan'].apply(clean_and_average)
angket_data['penyimpanan_kepentingan'] = angket_data['penyimpanan_kepentingan'].apply(clean_and_average)
angket_data['baterai_kepentingan'] = angket_data['baterai_kepentingan'].apply(clean_and_average)
angket_data['berat_kepentingan'] = angket_data['berat_kepentingan'].apply(clean_and_average)

# Calculate weights based on survey averages
weights = {
    'cpu_penilaian': angket_data['cpu_kepentingan'].mean() / 5,
    'ram_penilaian': angket_data['ram_kepentingan'].mean() / 5,
    'penyimpanan_penilaian': angket_data['penyimpanan_kepentingan'].mean() / 5,
    'baterai_penilaian': angket_data['baterai_kepentingan'].mean() / 5,
    'harga_penilaian': angket_data['harga_kepentingan'].mean() / 5,
    'berat_penilaian': angket_data['berat_kepentingan'].mean() / 5,
}

# Load the new laptop data file
laptop_file_path = 'D:\\University stuff\\upb\\S5\\KEPUTUSAN\\Laptop-Price.csv'
laptop_data = pd.read_csv(laptop_file_path)

# Rename relevant columns in laptop data
laptop_data = laptop_data.rename(columns={
    'Cpu Rate': 'cpu_frequency', 
    'Ram': 'ram', 
    'SSD': 'ssd', 
    'HDD': 'hdd', 
    'Price_euros': 'price'
})
laptop_data['original_price'] = laptop_data['price']  # Retain original price

# Clean RAM and storage data
laptop_data['ram'] = laptop_data['ram'].replace('GB', '', regex=True).astype(float)
laptop_data['primary_storage'] = laptop_data['ssd'].fillna(0) + laptop_data['hdd'].fillna(0)
laptop_data['cpu_frequency'] = laptop_data['cpu_frequency'].replace('GHz', '', regex=True).astype(float)

# Normalize data for benefit and cost criteria
benefit_criteria = ['cpu_frequency', 'ram', 'primary_storage']
cost_criteria = ['price']

# Create a normalized data copy for scoring
normalized_data = laptop_data.copy()
for col in benefit_criteria:
    max_value = laptop_data[col].max()
    normalized_data[col] = laptop_data[col] / max_value if max_value else 0
for col in cost_criteria:
    min_value = laptop_data[col].min()
    normalized_data[col] = min_value / laptop_data[col] if min_value else 0

# Calculate scores based on weighted importance
normalized_data['Score'] = (
    normalized_data['cpu_frequency'] * weights['cpu_penilaian'] +
    normalized_data['ram'] * weights['ram_penilaian'] +
    normalized_data['primary_storage'] * weights['penyimpanan_penilaian'] +
    normalized_data['price'] * weights['harga_penilaian'] +
    normalized_data['price'] * weights['berat_penilaian']
)

# Filter laptops in the price range (Rp 10,000,000 - Rp 15,000,000 or approx €650 - €975)
desired_range_laptops = normalized_data[(laptop_data['original_price'] >= 600) & (laptop_data['original_price'] <= 880)]
top_ranked_laptop = desired_range_laptops.loc[desired_range_laptops['Score'].idxmax()]

# Print the top-ranked laptop
print("Best Laptop in Price Range (Rp. 10,000,000 - Rp. 15,000,000):")
print(top_ranked_laptop[['Company', 'Product', 'Score', 'original_price', 'price']])
