import duckdb
from udfs import register
import pandas as pd

JOHNATHAN = "J[aeou]{1,2}[h]?n{1,2}[aeio]{0,2}[t]{1,2}[h]?[aeio]{0,2}n"
KATHERYNE = "[CK][ae]th[ae]?r[eiy]n{1,2}e?"
RYAN = "R[iy]a[n]{1,2}e?"


# def fuzzy_join_evaluation_with_truth(
#     con: duckdb.DuckDBPyConnection,
#     truth_file: str,
#     metric_sql: str,
#     csv_out_name: str,
#     threshold: float | int | None = None,
# ) -> None:
#     # Step 1: Load ground truth CSV and filter to 1980 and 2023
#     truth_df = pd.read_csv(f"names/{truth_file}")
#     df_1980 = truth_df[truth_df["Year"] == 1980]["Name"].drop_duplicates()
#     df_2023 = truth_df[truth_df["Year"] == 2023]["Name"].drop_duplicates()

#     # Cross-join to get all true (name_1980, name_2023) name matches
#     ground_truth = set((n1, n2) for n1 in df_1980 for n2 in df_2023)

#     # Step 2: Run the fuzzy join
#     con.execute("PRAGMA enable_profiling")
#     con.execute("PRAGMA enable_profile")

#     query = f"""
#         SELECT DISTINCT t1980.Name AS name_1980, t2023.Name AS name_2023
#         FROM ssa_names t1980
#         JOIN ssa_names t2023
#         ON {metric_sql}
#         WHERE t1980.Year = 1980 AND t2023.Year = 2023
#     """
#     results = con.sql(query).fetchall()
#     results_set = set(results)

#     # Export the results
#     con.sql(query).write_csv(f"names/{csv_out_name}_join.csv")
#     print(f"Exported {csv_out_name}_join.csv")

#     # Step 3: Evaluation
#     true_positives = results_set.intersection(ground_truth)
#     false_positives = results_set.difference(ground_truth)
#     accuracy = len(true_positives) / len(ground_truth) * 100 if ground_truth else 0.0

#     print(f"{csv_out_name} Join Accuracy: {accuracy:.2f}%")
#     print(f"{csv_out_name} False Positives: {len(false_positives)}")

def fuzzy_join_evaluation_with_truth(
    con: duckdb.DuckDBPyConnection,
    truth_file: str,
    metric_sql: str,
    csv_out_name: str,
    threshold: float | int | None = None,
) -> None:

    # Step 1: Load ground truth names from CSV (under names/)
    truth_df = pd.read_csv(f"names/{truth_file}")
    df_1980 = truth_df[truth_df["Year"] == 1980]["Name"].drop_duplicates()
    df_2023 = truth_df[truth_df["Year"] == 2023]["Name"].drop_duplicates()

    # Cross-join to get ground truth name pairs
    ground_truth = set((n1, n2) for n1 in df_1980 for n2 in df_2023)

    # Convert to SQL-usable lists
    names_1980 = "', '".join(df_1980.tolist())
    names_2023 = "', '".join(df_2023.tolist())

    # Step 2: Run the filtered fuzzy join
    con.execute("PRAGMA enable_profiling")
    con.execute("PRAGMA enable_profile")

    query = f"""
        SELECT DISTINCT t1980.Name AS name_1980, t2023.Name AS name_2023
        FROM ssa_names t1980
        JOIN ssa_names t2023
        ON {metric_sql}
        WHERE t1980.Year = 1980 AND t2023.Year = 2023
          AND t1980.Name IN ('{names_1980}')
          AND t2023.Name IN ('{names_2023}')
    """
    results = con.sql(query).fetchall()
    results_set = set(results)

    # Save join output
    con.sql(query).write_csv(f"names/{csv_out_name}_join.csv")
    print(f"Exported {csv_out_name}_join.csv")

    # Step 3: Evaluation
    true_positives = results_set.intersection(ground_truth)
    false_positives = results_set.difference(ground_truth)
    accuracy = len(true_positives) / len(ground_truth) * 100 if ground_truth else 0.0

    print(f"{csv_out_name} Join Accuracy: {accuracy:.2f}%")
    print(f"{csv_out_name} False Positives: {len(false_positives)}")


con = duckdb.connect()
register(con)

# Create a table from a CSV
con.execute(
    """
			CREATE TABLE ssa_names  (
				Year INTEGER,
				Name VARCHAR,
				Gender CHAR,
				Count INTEGER
			);
			COPY ssa_names FROM 'fixed_ssa_data.csv'
			"""
)


# --------------------- Fuzzy Joins between 1980 and 2023 -----------------------

# Fuzzy join using Soundex
fuzzy_join_evaluation_with_truth(
    con,
    "johnathan.csv",
    "soundex(t1980.Name) = soundex(t2023.Name)",
    "join_johnathan_soundex"
)

# Fuzzy join using Edit Distance
fuzzy_join_evaluation_with_truth(
    con,
    "johnathan.csv",
    "edit_distance(t1980.Name, t2023.Name) <= 2",
    "join_johnathan_edit2",
    threshold=2
)

# Fuzzy join using Trigram
fuzzy_join_evaluation_with_truth(
    con,
    "johnathan.csv",
    "trigram(t1980.Name, t2023.Name) > 0.4",
    "join_johnathan_trigram40",
    threshold=0.4
)

# Fuzzy join using Jaro-Winkler
fuzzy_join_evaluation_with_truth(
    con,
    "johnathan.csv",
    "jaro_winkler(t1980.Name, t2023.Name) > 0.85",
    "join_johnathan_jaro85",
    threshold=0.85
)
