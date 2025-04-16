import pandas as pd

# Load the two CSV files
ground_truth_df = pd.read_csv("names/katheryne.csv")[["Name"]]
soundex_results_df = pd.read_csv("names/soundex_katheryne_results.csv")[["Name"]]

print(len(ground_truth_df))
print(len(soundex_results_df))

# Normalize names (strip whitespace, lowercase)
ground_truth_set = set(ground_truth_df["Name"].str.strip().str.lower())
soundex_set = set(soundex_results_df["Name"].str.strip().str.lower())

# Set difference calculations
false_positives = soundex_set - ground_truth_set
false_negatives = ground_truth_set - soundex_set

# Convert to DataFrames
false_positives_df = pd.DataFrame(sorted(false_positives), columns=["False Positives"])
false_negatives_df = pd.DataFrame(sorted(false_negatives), columns=["False Negatives"])

# Save to CSV
false_positives_df.to_csv("false_positives.csv", index=False)
false_negatives_df.to_csv("false_negatives.csv", index=False)
print(f"# False Positives: {len(false_positives)}")
print(f"# False Negatives: {len(false_negatives)}")

print("✅ Saved false_positives.csv and false_negatives.csv")
