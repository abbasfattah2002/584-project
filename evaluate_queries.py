import duckdb
from udfs import register

# Connect to DuckDB
con = duckdb.connect()

# Register UDFs from your custom module
register(con)

# Run EXPLAIN ANALYZE on Levenshtein query
query = """
EXPLAIN ANALYZE
SELECT column0 AS name, edit_distance(column0, 'Jonathan') AS similarity_score
FROM read_csv_auto('fixed_ssa_data.csv', HEADER=False) AS ssa_baby_names
ORDER BY similarity_score;
"""

# Execute and print the execution plan + timing
explain_output = con.execute(query).fetchall()

# Print formatted EXPLAIN ANALYZE output
print("Execution Plan + Timing:")
for row in explain_output:
    print(row[0])
