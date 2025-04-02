import duckdb
from udfs import register


con = duckdb.connect()
con.execute("PRAGMA enable_profiling")
con.execute("PRAGMA enable_profile")
register(con)

con.execute("""
			CREATE TABLE ssa_names  (
				Year INTEGER,
				Name VARCHAR,
				Gender CHAR,
				Count INTEGER
			);
			COPY ssa_names FROM 'fixed_ssa_data.csv'
			""")

print(con.execute("SELECT Name FROM ssa_names").fetchall())