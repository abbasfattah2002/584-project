import duckdb
from udfs import register


con = duckdb.connect()
con.execute("PRAGMA enable_profiling")
con.execute("PRAGMA enable_profile")
register(con)
