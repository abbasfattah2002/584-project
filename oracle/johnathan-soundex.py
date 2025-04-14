import oracledb
import csv

un = "sys"
cs = "localhost:1521/XEPDB1"
pw = "cse584"

with oracledb.connect(
    user=un, password=pw, dsn=cs, mode=oracledb.AUTH_MODE_SYSDBA
) as connection:
    with connection.cursor() as cursor:
        result = set(cursor.execute("SELECT Year, Name, Gender FROM ssa_names WHERE SOUNDEX(NAME) = SOUNDEX('Johnathan')").fetchall())
        print(result)
