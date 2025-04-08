import duckdb
from udfs import register

JOHNATHAN = 'J[aeou]{1,2}[h]?n{1,2}[aeio]{0,2}[t]{1,2}[h]?[aeio]{0,2}n$'

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

con.execute("SELECT Year, Name, Gender FROM ssa_names WHERE Name SIMILAR TO ?", (JOHNATHAN,)).fetchall()