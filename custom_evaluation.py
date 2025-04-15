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
        f"Soundex accuracy: {len(soundex.intersection(truth)) / len(truth) * 100}%\n"
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
        f"{csv_out_name} accuracy: {len(results.intersection(truth)) / len(truth) * 100:.2f}%\n"
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
			COPY ssa_names FROM 'fuzzed_fixed_ssa_data2.csv'
			"""
)

# --------------------- JOHNATHAN -----------------------

# Custom Union similarity
metric_evaluation(
    con,
    JOHNATHAN,
    "custom_union_johnathan",
    "Johnathan",
    "custom_union(Name, 'Johnathan')",
    run_analysis=True,
)

# Custom Intersect similarity
metric_evaluation(
    con,
    JOHNATHAN,
    "custom_intersect_johnathan",
    "Johnathan",
    "custom_intersect(Name, 'Johnathan')",
    run_analysis=True,
)


# --------------------- Katherine -----------------------

# Custom Union similarity
metric_evaluation(
    con,
    KATHERYNE,
    "custom_union_katheryne",
    "katheryne",
    "custom_union(Name, 'katheryne')",
    run_analysis=True,
)

# Custom Intersect similarity
metric_evaluation(
    con,
    KATHERYNE,
    "custom_intersect_katheryne",
    "katheryne",
    "custom_intersect(Name, 'katheryne')",
    run_analysis=True,
)
