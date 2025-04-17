<!-- Explain the usage of your tool, e.g. command line arguments and pointers to some small text data that can be used to run your tool -->

# Main Sources of data
- `fixed_ssa_data.csv` - master list of names
- `names/johnathan.csv` - ground truth "Johnathan" set
- `names/katheryne.csv` - ground truth "Katheryne" set

# DBMS Usage

## DuckDB
```bash
python3 evaluation.py # Runs all DuckDB queries
```

## Oracle
- This assumes the Docker container is running
```bash
./oracle/oracle_evaluate.sh # Runs all variants on thresholds
```

## PostgreSQL
- Install `psql`

## SQL Server
- The queries in `sql-server/` can be ran directly.
- Look in the "Messages" tab next to "Results" to get execution time of the specified query

## sqlite
```bash
./sqlite/sqlite_evaluation.sh # Runs all queries with only one threshold value
```

# Source Code Explanation
- Other than DuckDB, all other DBMSs have their own folder

## DuckDB
- `udfs.py` contains implementations of each similarity metric and custom fuzzy logic
  - `trigram()` is the only similarity metric we implemented ourselves

## Oracle

## PostgreSQL

## SQL Server

## sqlite