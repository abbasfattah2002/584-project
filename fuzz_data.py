import pandas as pd
import re
import random
import nlpaug.augmenter.char as nac

TESTING = False
VARIANCE_MIN = 0
VARIANCE_MAX = 1
VARIANCE_COPIES = 2
count = 0
filename = "fuzzed_fixed_ssa_data" + str(VARIANCE_COPIES) + ".csv"

# This script can generate copies of the ssa_data dataset and introduce typos
df = pd.read_csv("fixed_ssa_data.csv")
df.to_csv(filename, index=False)
new_rows = []
for index, row in df.iterrows():
    if TESTING and count >= 2000:
        break
    count += 1
    for i in range(VARIANCE_COPIES):
        new_row = row.copy()
        aug = nac.KeyboardAug(
            aug_char_min=VARIANCE_MIN,
            aug_char_max=i,
            include_special_char=False,
            include_numeric=False,
        )
        newstr = str(aug.augment(row["Name"]))  # modification step
        clean = re.sub(r"[^a-zA-Z]", "", newstr)  # remove nonletter typos
        new_row["Name"] = clean[0].upper() + clean[1:].lower()  # name format
        new_rows.append(new_row)
    print("Processed row: ", count)
    if count % 1000 == 0:
        df_extension = pd.DataFrame(new_rows)
        df_extension.to_csv(filename, mode="a", header=False, index=False)
        new_rows = []
df_extension = pd.DataFrame(new_rows)
df_extension.to_csv(filename, mode="a", header=False, index=False)
