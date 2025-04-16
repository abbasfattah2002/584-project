import pandas as pd
import jellyfish
import editdistance

# Load fuzzed SSA data and ground truth
fuzzed_df = pd.read_csv("fuzzed_fixed_ssa_data2.csv")
truth_df = pd.read_csv("names/johnathan.csv")
truth_names = set(truth_df["Name"].unique())

# All names from fuzzed data that are not already part of the ground truth
fuzzed_names = set(fuzzed_df["Name"].unique())
candidate_names = [name for name in fuzzed_names if name not in truth_names]

# Reference string
reference = "Jonathan"
reference_soundex = jellyfish.soundex(reference)

# Collect matches
levenshtein_matches = []
soundex_matches = []

for name in candidate_names:
    if not isinstance(name, str):
        continue  # skip non-strings or NaNs

    lev = editdistance.eval(name.lower(), reference.lower())
    snd = jellyfish.soundex(name)

    if lev <= 2:  # typo detection
        levenshtein_matches.append((name, lev))
    if snd == reference_soundex:
        soundex_matches.append(name)

# UNION of both
union_matches = set(name for name, _ in levenshtein_matches) | set(soundex_matches)

# Output results
print("🧠 Levenshtein Matches (<= 2 edits):")
for name, dist in sorted(levenshtein_matches, key=lambda x: x[1]):
    print(f"{name} (distance {dist})")

print("\n🔊 Soundex Matches:")
for name in sorted(set(soundex_matches)):
    print(name)

print("\n🔀 UNION (Combined Matches):")
for name in sorted(union_matches):
    print(name)

# You can also export them:
pd.DataFrame({"Name": list(union_matches)}).to_csv(
    "names/johnathan_fuzzed_candidates.csv", index=False
)
