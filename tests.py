import unittest
from typing import List

from udfs import register
import duckdb
from duckdb.typing import *


class Tests(unittest.TestCase):
    # Define a function that starts with 'test'
    def test_example_udf(self):
        con = duckdb.connect()

        # Dictionary that maps countries and world cups they won
        world_cup_titles = {
            "Brazil": 5,
            "Germany": 4,
            "Italy": 4,
            "Argentina": 2,
            "Uruguay": 2,
            "France": 2,
            "England": 1,
            "Spain": 1,
        }

        # Function that will be registered as an UDF, simply does a lookup in the python dictionary
        def world_cups(x):
            return world_cup_titles.get(x)

        # We register the function (note null_handling is set to 'special')
        con.create_function(
            "wc_titles", world_cups, [VARCHAR], INTEGER, null_handling="special"
        )

        # Let's create an example countries table with the countries we are interested in using
        con.execute("CREATE TABLE countries (country VARCHAR)")
        con.execute(
            """INSERT INTO countries VALUES ('Brazil'), ('Germany'), ('Italy'), ('Argentina'), ('Uruguay'), ('France'), ('England'), ('Spain'), ('Netherlands')"""
        )
        # We can simply call the function through SQL, and even use the function return to eliminate the countries that never won a world cup
        result: List[tuple[str, int | None]] = con.sql(
            "SELECT country, wc_titles(country) AS world_cups FROM countries"
        ).fetchall()
        # [('Brazil', 5), ('Germany', 4), ('Italy', 4), ('Argentina', 2), ('Uruguay', 2), ('France', 2), ('England', 1), ('Spain', 1), ('Netherlands', None)]
        for country, wins in result:
            if country in world_cup_titles:
                # Here is where the actual unit test takes place. Note it can take an optional error message.
                self.assertEqual(
                    wins,
                    world_cup_titles[country],
                    f"Saw {wins} wins, expected {country} to have {world_cup_titles[country]} wins",
                )
            else:
                self.assertNotIn(country, world_cup_titles)

    def test_edit_distance(self):
        con = duckdb.connect()
        register(con)
        res0 = con.execute("SELECT edit_distance('kitten', 'sitting')").fetchone()[0]
        self.assertEqual(res0, 3)
        res1 = con.execute(
            "SELECT edit_distance('uninformed', 'uniformed')"
        ).fetchone()[0]
        self.assertEqual(res1, 1)

    def test_jaro_winkler(self):
        con = duckdb.connect()
        register(con)
        res0 = con.execute("SELECT jaro_winkler('DwAyNE', 'DuANE')").fetchone()[0]
        res1 = con.execute("SELECT jaro_winkler('TRATE', 'TRACE')").fetchone()[0]
        self.assertAlmostEqual(res0, 0.84)
        self.assertAlmostEqual(res1, 0.9066667)

    def test_ss_names(self):
        con = duckdb.connect()
        register(con)
        # change to loop through files in ssnames folder
        con.execute(
            "CREATE TABLE names_table (Name VARCHAR, Gender VARCHAR, Number INT, YOB INT)"
        )
        con.execute(
            "INSERT INTO names_table (Name, Gender, Number, YOB) SELECT *, '2023' FROM read_csv_auto('social_security_names/yob2023.txt', HEADER=False)"
        )

        result = con.execute(
            "SELECT * FROM names_table WHERE jaro_winkler(Name, 'Olivia') > 0.8"
        ).fetchall()
        result2 = con.execute(
            "SELECT * FROM names_table WHERE edit_distance(Name, 'Olivia') < 3"
        ).fetchall()
        self.assertNotEqual(result, result2)

    def test_trigram(self):
        con = duckdb.connect()
        register(con)
        res = con.execute("SELECT trigram('word', 'two words')").fetchone()[0]

        self.assertAlmostEqual(res, 4 / 11)

    def test_union(self):
        con = duckdb.connect()
        register(con)
        con.execute(
            "CREATE TABLE names_table (YOB VARCHAR, Name VARCHAR, Gender VARCHAR, Number INT)"
        )
        con.execute(
            "INSERT INTO names_table (YOB, Name, Gender, Number) SELECT *, FROM read_csv_auto('fixed_ssa_data.csv', HEADER=False) WHERE column0 = '2023'"
        )
        result = con.execute(
            "SELECT * FROM names_table WHERE custom_union(Name, 'Olivia')"
        ).fetchall()
        print(result)


    def test_intersect(self):
        con = duckdb.connect()
        register(con)
        con.execute(
            "CREATE TABLE names_table (YOB VARCHAR, Name VARCHAR, Gender VARCHAR, Number INT)"
        )
        con.execute(
            "INSERT INTO names_table (YOB, Name, Gender, Number) SELECT *, FROM read_csv_auto('fixed_ssa_data.csv', HEADER=False) WHERE column0 = '2023'"
        )
        result = con.execute(
            "SELECT * FROM names_table WHERE custom_intersect(Name, 'Johnathan')"
        ).fetchall()
        print(result)

