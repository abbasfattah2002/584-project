import pandas as pd
import os
import glob

# Path setup
NAMES_DIR = "names"
KATHERINE_TRUTH = os.path.join(NAMES_DIR, "katheryne.csv")
JOHNATHAN_TRUTH = os.path.join(NAMES_DIR, "johnathan.csv")

# Load both truth datasets once
kath_truth_df = pd.read_csv(KATHERINE_TRUTH)[["Name"]]
john_truth_df = pd.read_csv(JOHNATHAN_TRUTH)[["Name"]]

# Normalize to sets of lowercase names
kath_truth_set = set(kath_truth_df["Name"].str.strip().str.lower())
john_truth_set = set(john_truth_df["Name"].str.strip().str.lower())

# Loop through all *_results.csv files
result_files = sorted(glob.glob(os.path.join(NAMES_DIR, "*_results.csv")))

for result_path in result_files:
    base_name = os.path.basename(result_path).replace("_results.csv", "")

    # Load result file
    result_df = pd.read_csv(result_path)
    if "Name" not in result_df.columns:
        print(f"❌ Skipping {base_name} — no 'Name' column")
        continue

    result_set = set(result_df["Name"].str.strip().str.lower())

    # Choose correct ground truth
    if "katheryne" in base_name:
        truth_set = kath_truth_set
    elif "johnathan" in base_name:
        truth_set = john_truth_set
    else:
        print(f"❌ Skipping {base_name} — can't determine target name")
        continue

    # Compute FP and FN
    false_positives = result_set - truth_set
    false_negatives = truth_set - result_set

    # Write outputs
    fp_path = os.path.join(NAMES_DIR, f"{base_name}_false_positives.csv")
    fn_path = os.path.join(NAMES_DIR, f"{base_name}_false_negatives.csv")

    pd.DataFrame(sorted(false_positives), columns=["Name"]).to_csv(fp_path, index=False)
    pd.DataFrame(sorted(false_negatives), columns=["Name"]).to_csv(fn_path, index=False)

    print(f"✅ {base_name}")
    print(f"   Results: {len(result_set)} | Truth: {len(truth_set)}")
    print(f"   False Positives: {len(false_positives)} | False Negatives: {len(false_negatives)}")
