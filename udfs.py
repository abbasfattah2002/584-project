import duckdb
from duckdb.typing import *
import editdistance
import jaro
import jellyfish

def edit_distance(a: str, b: str) -> bool:
	# levenshtein distance
	s = editdistance.eval(a, b)
	return (s < 10)

def soundex(s: str) -> str:
	return jellyfish.soundex(s)

def jaro_winkler(a: str, b: str) -> bool:
	# jaro-winkler distance
	s = jaro.jaro_winkler_metric(a, b)
	return (s > 0.8)

def register(con):
	# to call in other files, add this line: from udf_module import register

	# add a seperate line for each UDF
	con.create_function('edit_distance', edit_distance, ['VARCHAR', 'VARCHAR'], 'BOOLEAN')
	con.create_function('jaro_winkler', jaro_winkler, ['VARCHAR', 'VARCHAR'], 'BOOLEAN')
	con.create_function('soundex', soundex, ['VARCHAR'], 'VARCHAR')


# testing stuff
con = duckdb.connect()

register(con)

con.execute("CREATE TABLE people (name VARCHAR, city VARCHAR)")
con.execute("INSERT INTO people VALUES ('Alice', 'New York'), ('Bob', 'Los Angeles'), ('Charlie', 'New York'), ('Joe', 'Chicago')")

result = con.execute("SELECT * FROM people WHERE jaro_winkler(city, 'New York')").fetchall()