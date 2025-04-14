import oracledb
import csv

un = "sys"
cs = "localhost:1521/XEPDB1"
pw = "cse584"

with oracledb.connect(
    user=un, password=pw, dsn=cs, mode=oracledb.AUTH_MODE_SYSDBA
) as connection:
    with connection.cursor() as cursor:
        cursor.execute("DROP TABLE ssa_names")
        print("Dropped ssa_names")

        cursor.execute("DROP TABLE johnathan")
        print("Dropped johnathan")

        cursor.execute("DROP TABLE katheryne")
        print("Dropped katheryne")

        cursor.execute(
            """CREATE TABLE ssa_names(
                        Year  	NUMBER,
                        Name  	VARCHAR2(50),
                        Gender 	VARCHAR2(1),
                        Count  	NUMBER
                        )
                        """
        )
        print("Created ssa_names")

        cursor.execute(
            """CREATE TABLE johnathan(
                        Year  	NUMBER,
                        Name  	VARCHAR2(50),
                        Gender 	VARCHAR2(1)
                        )
                        """
        )
        print("Created johnathan")

        cursor.execute(
            """CREATE TABLE katheryne(
                        Year  	NUMBER,
                        Name  	VARCHAR2(50),
                        Gender 	VARCHAR2(1)
                        )
                        """
        )
        print("Created katheryne")

        with open("fixed_ssa_data.csv", newline="") as csv_file:
            BATCH_SIZE = 10000
            rows = csv.reader(csv_file)
            next(rows, None)  # Skip header
            insert_sql = "INSERT INTO ssa_names (Year, Name, Gender, Count) VALUES (:1, :2, :3, :4)"
            data = []
            for row in rows:
                data.append(tuple(row))
                if len(data) % BATCH_SIZE == 0:
                    cursor.execute(insert_sql, parameters=data)
                    data = []
            if data:
                cursor.execute(insert_sql, parameters=data)
            
            print(f"{cursor.execute("SELECT COUNT(*) FROM ssa_names").fetchone()} rows inserted into ssa_names")

        with open("names/johnathan.csv", newline="") as csv_file:
            rows = csv.reader(csv_file)
            next(rows, None)  # Skip header
            data = []
            for row in rows:
                data.append(tuple(row))
            cursor.executemany("""INSERT INTO johnathan (Year, Name, Gender) VALUES (:1, :2, :3)""", parameters=data)

            print(f'{cursor.rowcount} rows inserted into johnathan')
        
        with open("names/katheryne.csv", newline="") as csv_file:
            rows = csv.reader(csv_file)
            next(rows, None)  # Skip header
            data = []
            for row in rows:
                data.append(tuple(row))
            cursor.executemany("""INSERT INTO katheryne (Year, Name, Gender) VALUES (:1, :2, :3)""", parameters=data)

            print(f'{cursor.rowcount} rows inserted into katheryne')

    connection.commit()