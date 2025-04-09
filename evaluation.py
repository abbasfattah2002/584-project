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

soundex_evaluation(con, JOHNATHAN, "johnathan", True)
