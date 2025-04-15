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
        for i in [0.75, 0.8, 0.85]:
            before = time.time()
            result = cursor.execute(
                "SELECT Year, Name, Gender FROM ssa_names WHERE UTL_MATCH.JARO_WINKLER(Name, 'Johnathan') > :1", parameters=[i]
            )
            time_elapsed = time.time() - before
            

            result = set(result.fetchall())

            truth = set(cursor.execute("SELECT * FROM johnathan").fetchall())

            print(
                f"Jaro Winkler accuracy at >{i}: {len(result.intersection(truth))}/{len(truth)} = {len(result.intersection(truth)) / len(truth) * 100}%\n"
                f"False positive count: {len(result.difference(truth))}\n"
                f"Exeuction time: {time_elapsed} seconds\n"
            )


