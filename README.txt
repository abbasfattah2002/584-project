# Main Sources of data
- `fixed_ssa_data.csv` - master list of names
- `fuzzed_fixed_ssa_data2.csv` - Fuzzed dataset, names with typos included
- `names/johnathan.csv` - ground truth "Johnathan" set
- `names/katheryne.csv` - ground truth "Katheryne" set

# DBMS Usage

## DuckDB
```bash
python3 evaluation.py # Runs all DuckDB queries
python3 custom_evaluation.py # Runs all DuckDB queries for the custom metrics
python csv_set_diff.py # Create set of FP and FN names for each similarity metric
```

## Oracle
- Start the Docker container
```bash
./oracle/oracle_evaluate.sh # Runs all variants on thresholds
```

## PostgreSQL
```bash
psql -U <USERNAME> -d <DBNAME> -a -f postgres/init.sql # Afterwards, replace "init.sql" with any other sql file
```

## SQL Server
- Create a database called CSE584
- Import these as flat files:
  - `fixed_ssa_data.csv` as ssa_names
  - `names/johnathan.csv` as johnathan
  - `names/katheryne.csv` as katheryne
- Import the queries in `sql-server/`.
- Look in the "Messages" tab next to "Results" to get execution time of the specified query

## sqlite
```bash
cd sqlite/
sqlite3 data.db < init.sql # Load the data into data.db
./sqlite_evaluate.sh # Note it doesn't run with all parameters for a given similarity metric
```
- **Do not delete `spellfix1.so`.**
  - This file enables the spellfix1 virtual table, and therefore the editdist3 function.
  - I had to compile this from source, and the latest source version is missing a header file required for compilation to work.

# Source Code Explanation
- Other than DuckDB, all other DBMSs have their own folder consisting of scripts and results.

## DuckDB
- `udfs.py` contains implementations of each similarity metric and custom fuzzy logic
  - `trigram()` is the only similarity metric we implemented ourselves
