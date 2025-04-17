import oracledb
import time
import csv

un = "sys"
cs = "localhost:1521/XEPDB1"
pw = "cse584"

with oracledb.connect(
    user=un, password=pw, dsn=cs, mode=oracledb.AUTH_MODE_SYSDBA
) as connection:
    with connection.cursor() as cursor:
        for i in [0.85, 0.9, 0.95]:
            before = time.time()
            result = cursor.execute(
                "SELECT Year, Name, Gender FROM ssa_names WHERE UTL_MATCH.JARO_WINKLER(Name, 'Johnathan') > :1",
                parameters=[i],
            ).fetchall()
            time_elapsed = time.time() - before

            result = set(result)
            truth = set(cursor.execute("SELECT * FROM johnathan").fetchall())

            print(
                f"Jaro Winkler accuracy for Johnathan at >{i}: {len(result.intersection(truth))}/{len(truth)} = {len(result.intersection(truth)) / len(truth) * 100}%"
            )
            print(f"False positive count: {len(result.difference(truth))}")
            print(f"Exeuction time: {time_elapsed} seconds")
