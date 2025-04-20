import duckdb
from udfs import register

JOHNATHAN = "J[aeou]{1,2}[h]?n{1,2}[aeio]{0,2}[t]{1,2}[h]?[aeio]{0,2}n"
KATHERYNE = "[CK][ae]th[ae]?r[eiy]n{1,2}e?"

def regex_comparison(con: duckdb.DuckDBPyConnection, regex: str):
    con.execute("PRAGMA enable_profiling")
    con.execute("PRAGMA enable_profile")

    con.execute(
        "SELECT Year, Name, Gender FROM ssa_names WHERE Name SIMILAR TO ?",
        [regex],
    )

    con.execute("SELECT Year, Name, Gender FROM ssa_names WHERE soundex(Name) = soundex('Johnathan')")

    con.execute("SELECT Year, Name, Gender FROM ssa_names WHERE Name LIKE 'J%' AND soundex(Name) = soundex('Johnathan')")

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

regex_comparison(con, JOHNATHAN)



