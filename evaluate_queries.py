import duckdb
from udfs import register

# Connect to DuckDB
con = duckdb.connect()

# Register UDFs from your custom module
register(con)

JOHNATHAN = 'J[aeou]{1,2}[h]?n{1,2}[aeio]{0,2}[t]{1,2}[h]?[aeio]{0,2}n$'

con.execute("""
			CREATE TABLE ssa_names  (
				Year INTEGER,
				Name VARCHAR,
				Gender CHAR,
				Count INTEGER
			);
			COPY ssa_names FROM 'fixed_ssa_data.csv'
			""")

result = con.execute("SELECT Year, Name, Gender FROM ssa_names WHERE Name SIMILAR TO ?", (JOHNATHAN,)).fetchall()
# for row in result:
#     print(row)  # Should print actual plan content if it ran correctly



# # Optimized query with filtering
query = """
SELECT name, edit_distance(Name, 'Jonathan') AS similarity_score
FROM ssa_names
WHERE year = 2020
ORDER BY similarity_score
LIMIT 10;
"""

# # Execute and fetch EXPLAIN ANALYZE output
result = con.execute(query).fetchall()
print("Execution Plan + Timing:\n")
for row in result:
    print(row[0])  # Should print actual plan content if it ran correctly

