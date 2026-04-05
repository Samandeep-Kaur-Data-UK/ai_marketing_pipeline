import pandas as pd

# --- CONFIG ---
RAW_PATH = "data/raw/reviews.csv"
SAMPLE_SIZE = 5000

# --- LOAD ---
df = pd.read_csv(RAW_PATH, nrows=SAMPLE_SIZE)

# --- INSPECT ---
print("=" * 40)
print("SHAPE:", df.shape)
print("=" * 40)

print("\nCOLUMNS:")
print(df.columns.tolist())

print("\nDTYPES:")
print(df.dtypes)

print("\nFIRST 3 ROWS:")
print(df.head(3))

print("\nMISSING VALUES:")
print(df.isnull().sum())

print("\nSCORE DISTRIBUTION:")
print(df["Score"].value_counts().sort_index())