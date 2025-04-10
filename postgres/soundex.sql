CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;

EXPLAIN ANALYZE SELECT Year, Name, Gender FROM ssa_names WHERE difference(Name, 'Johnathan') = 4;

CREATE TEMP TABLE tempjohnathan AS SELECT Year, Name, Gender FROM ssa_names WHERE difference(Name, 'Johnathan') = 4;

SELECT 'Accuracy: ' ||
	(SELECT COUNT(*) FROM tempjohnathan j
	INNER JOIN johnathan s
	ON s.Year = j.Year AND s.Name = j.Name AND s.Gender = j.Gender)
|| '/' || (SELECT COUNT(*) FROM johnathan);

DROP TABLE tempjohnathan;

\copy ( SELECT Year, Name, Gender FROM ssa_names WHERE difference(Name, 'Johnathan') = 4 ORDER BY Year ASC, Name ASC, Gender ASC) TO './postgres/johnathan-soundex.csv' WITH CSV DELIMITER ',';