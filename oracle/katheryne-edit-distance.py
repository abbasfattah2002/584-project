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
        for i in [4, 5]:
            before = time.time()
            result = cursor.execute(
                "SELECT Year, Name, Gender FROM ssa_names WHERE UTL_MATCH.EDIT_DISTANCE(Name, 'Katheryne') < :1",
                parameters=[i],
            )
            time_elapsed = time.time() - before

            result = set(result.fetchall())

            truth = set(cursor.execute("SELECT * FROM katheryne").fetchall())

            print(
                f"Edit distance accuracy for Katheryne at <{i}: {len(result.intersection(truth))}/{len(truth)} = {len(result.intersection(truth)) / len(truth) * 100}%"
            )
            print(f"False positive count: {len(result.difference(truth))}")
            print(f"Exeuction time: {time_elapsed} seconds")
