import duckdb
from udfs import register

JOHNATHAN = "J[aeou]{1,2}[h]?n{1,2}[aeio]{0,2}[t]{1,2}[h]?[aeio]{0,2}n"
KATHERYNE = "[CK][ae]th[ae]?r[eiy]n{1,2}e?"
RYAN = "R[iy]a[n]{1,2}e?"


def soundex_evaluation(
    con: duckdb.DuckDBPyConnection,
    truth_regex: str,
    csv_out_name: str,
    run_analysis: bool = False,
) -> None:
    # Export a query's results to CSV
    query = con.sql(
        "SELECT Year, Name, Gender FROM ssa_names WHERE Name SIMILAR TO $pattern",
        params={"pattern": truth_regex},
    )
    query.write_csv(f"names/{csv_out_name}.csv")

    print(f"Exported {csv_out_name}.csv")

    if not run_analysis:
        return

    truth = set(
        con.execute(
            "SELECT Year, Name, Gender FROM ssa_names WHERE Name SIMILAR TO ?",
            [truth_regex],
        ).fetchall()
    )

    con.execute("PRAGMA enable_profiling")
    con.execute("PRAGMA enable_profile")

    soundex = set(
        con.execute(
            "SELECT Year, Name, Gender FROM ssa_names WHERE soundex(Name) = soundex('Johnathan')"
        ).fetchall()
    )

    print(
        f"Soundex accuracy for {csv_out_name}: {len(soundex.intersection(truth))}/{len(truth)} = {len(soundex.intersection(truth)) / len(truth) * 100}%\n"
        f"Soundex false positive count: {len(soundex.difference(truth))}"
    )


def metric_evaluation(
    con: duckdb.DuckDBPyConnection,
    truth_regex: str,
    csv_out_name: str,
    reference_name: str,
    metric_sql: str,
    run_analysis: bool = False,
    threshold: float | int | None = None,
) -> None:
    # Export truth set to CSV
    truth_query = con.sql(
        "SELECT Year, Name, Gender FROM ssa_names WHERE Name SIMILAR TO $pattern",
        params={"pattern": truth_regex},
    )
    truth_query.write_csv(f"names/{csv_out_name}_truth.csv")
    print(f"Exported {csv_out_name}_truth.csv")

    if not run_analysis:
        return

    truth = set(truth_query.fetchall())

    con.execute("PRAGMA enable_profiling")
    con.execute("PRAGMA enable_profile")

    if threshold is not None:
        results = set(
            con.execute(
                f"""
                SELECT Year, Name, Gender FROM ssa_names
                WHERE {metric_sql} AND Name != '{reference_name}'
                """
            ).fetchall()
        )
    else:
        # Use raw metric if no thresholding needed (e.g., Soundex equality)
        results = set(
            con.execute(
                f"""
                SELECT Year, Name, Gender FROM ssa_names
                WHERE {metric_sql}
                """
            ).fetchall()
        )

    print(
        f"{csv_out_name} accuracy for {csv_out_name}: {len(results.intersection(truth))}/{len(truth)} = {len(results.intersection(truth)) / len(truth) * 100:.2f}%\n"
        f"{csv_out_name} false positives: {len(results.difference(truth))}"
    )


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


# --------------------- JOHNATHAN -----------------------

soundex_evaluation(con, JOHNATHAN, "soundex_johnathan", True)

# Jaro-Winkler
metric_evaluation(
    con,
    JOHNATHAN,
    "jaro_johnathan_85",
    "Johnathan",
    "jaro_winkler(Name, 'Johnathan') > 0.85",
    run_analysis=True,
)
# Jaro-Winkler
metric_evaluation(
    con,
    JOHNATHAN,
    "jaro_johnathan_90",
    "Johnathan",
    "jaro_winkler(Name, 'Johnathan') > 0.90",
    run_analysis=True,
)
# Jaro-Winkler
metric_evaluation(
    con,
    JOHNATHAN,
    "jaro_johnathan_95",
    "Johnathan",
    "jaro_winkler(Name, 'Johnathan') > 0.95",
    run_analysis=True,
)


# Edit Distance
metric_evaluation(
    con,
    JOHNATHAN,
    "edit_johnathan_lt_3",
    "Johnathan",
    "edit_distance(Name, 'Johnathan') < 3",
    run_analysis=True,
)
# Edit Distance
metric_evaluation(
    con,
    JOHNATHAN,
    "edit_johnathan_lt_4",
    "Johnathan",
    "edit_distance(Name, 'Johnathan') < 4",
    run_analysis=True,
)
# Edit Distance
metric_evaluation(
    con,
    JOHNATHAN,
    "edit_johnathan_lt_5",
    "Johnathan",
    "edit_distance(Name, 'Johnathan') < 5",
    run_analysis=True,
)


# Trigram similarity
metric_evaluation(
    con,
    JOHNATHAN,
    "trigram_johnathan_gt_25",
    "Johnathan",
    "trigram(Name, 'Johnathan') > 0.25",
    run_analysis=True,
)
# Trigram similarity
metric_evaluation(
    con,
    JOHNATHAN,
    "trigram_johnathan_gt_.5",
    "Johnathan",
    "trigram(Name, 'Johnathan') > 0.5",
    run_analysis=True,
)
# Trigram similarity
metric_evaluation(
    con,
    JOHNATHAN,
    "trigram_johnathan_gt_75",
    "Johnathan",
    "trigram(Name, 'Johnathan') > 0.75",
    run_analysis=True,
)


# --------------------- Katheryne -----------------------

# Soundex
metric_evaluation(
    con,
    KATHERYNE,
    "soundex_katheryne",
    "Katheryne",
    "soundex(Name) = soundex('Katheryne')",
    run_analysis=True,
)


# Jaro-Winkler
metric_evaluation(
    con,
    KATHERYNE,
    "jaro_katheryne_85",
    "katheryne",
    "jaro_winkler(Name, 'katheryne') > 0.85",
    run_analysis=True,
)
# Jaro-Winkler
metric_evaluation(
    con,
    KATHERYNE,
    "jaro_katheryne_90",
    "katheryne",
    "jaro_winkler(Name, 'katheryne') > 0.90",
    run_analysis=True,
)
# Jaro-Winkler
metric_evaluation(
    con,
    KATHERYNE,
    "jaro_katheryne_95",
    "katheryne",
    "jaro_winkler(Name, 'katheryne') > 0.95",
    run_analysis=True,
)


# Edit Distance
metric_evaluation(
    con,
    KATHERYNE,
    "edit_katheryne_lt_3",
    "katheryne",
    "edit_distance(Name, 'katheryne') < 3",
    run_analysis=True,
)
# Edit Distance
metric_evaluation(
    con,
    KATHERYNE,
    "edit_katheryne_lt_4",
    "katheryne",
    "edit_distance(Name, 'katheryne') < 4",
    run_analysis=True,
)
# Edit Distance
metric_evaluation(
    con,
    KATHERYNE,
    "edit_katheryne_lt_5",
    "katheryne",
    "edit_distance(Name, 'katheryne') < 5",
    run_analysis=True,
)


# Trigram similarity
metric_evaluation(
    con,
    KATHERYNE,
    "trigram_katheryne_gt_25",
    "katheryne",
    "trigram(Name, 'katheryne') > 0.25",
    run_analysis=True,
)
# Trigram similarity
metric_evaluation(
    con,
    KATHERYNE,
    "trigram_katheryne_gt_5",
    "katheryne",
    "trigram(Name, 'katheryne') > 0.5",
    run_analysis=True,
)
# Trigram similarity
metric_evaluation(
    con,
    KATHERYNE,
    "trigram_katheryne_gt_75",
    "katheryne",
    "trigram(Name, 'katheryne') > 0.75",
    run_analysis=True,
)
