import duckdb
from udfs import register

JOHNATHAN = "J[aeou]{1,2}[h]?n{1,2}[aeio]{0,2}[t]{1,2}[h]?[aeio]{0,2}n"

con = duckdb.connect()
con.execute("PRAGMA enable_profiling")
con.execute("PRAGMA enable_profile")
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

# Export a query's results to a CSV
con.execute(
    "COPY (SELECT Year, Name, Gender FROM ssa_names WHERE Name SIMILAR TO ?) TO 'johnathan.csv'",
    [JOHNATHAN],
)

# Or save it in-memory
johnathan_truth = set(
    con.execute(
        "SELECT Year, Name, Gender FROM ssa_names WHERE Name SIMILAR TO ?", [JOHNATHAN]
    ).fetchall()
)
johnathan_soundex = set(
    con.execute(
        "SELECT Year, Name, Gender FROM ssa_names WHERE soundex(Name) = soundex('Johnathan')"
    ).fetchall()
)

print(
    f"Soundex accuracy: {len(johnathan_soundex.intersection(johnathan_truth)) / len(johnathan_truth) * 100}%"
    f"Soundex false positive count: {len(johnathan_soundex.difference(johnathan_truth))}"
)
