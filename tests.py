import unittest
from typing import List

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
			"Spain": 1
		}

		# Function that will be registered as an UDF, simply does a lookup in the python dictionary
		def world_cups(x):
			return world_cup_titles.get(x)

		# We register the function (note null_handling is set to 'special')
		con.create_function("wc_titles", world_cups, [VARCHAR], INTEGER, null_handling='special')

		# Let's create an example countries table with the countries we are interested in using
		con.execute("CREATE TABLE countries (country VARCHAR)")
		con.execute("INSERT INTO countries VALUES ('Brazil'), ('Germany'), ('Italy'), ('Argentina'), ('Uruguay'), ('France'), ('England'), ('Spain'), ('Netherlands')")
		# We can simply call the function through SQL, and even use the function return to eliminate the countries that never won a world cup
		result: List[tuple[str, int | None]] = con.sql("SELECT country, wc_titles(country) AS world_cups FROM countries").fetchall()
		# [('Brazil', 5), ('Germany', 4), ('Italy', 4), ('Argentina', 2), ('Uruguay', 2), ('France', 2), ('England', 1), ('Spain', 1), ('Netherlands', None)]
		for country, wins in result:
			if country in world_cup_titles:
				# Here is where the actual unit test takes place. Note it can take an optional error message.
				self.assertEqual(wins, world_cup_titles[country], f'Saw {wins} wins, expected {country} to have {world_cup_titles[country]} wins')
			else:
				self.assertNotIn(country, world_cup_titles)