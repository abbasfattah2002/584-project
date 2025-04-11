CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;

EXPLAIN ANALYZE SELECT Year, Name, Gender FROM ssa_names WHERE difference(Name, 'Johnathan') = 4;

CREATE TEMP TABLE temp AS SELECT Year, Name, Gender FROM ssa_names WHERE difference(Name, 'Johnathan') = 4;

SELECT 'Accuracy: ' ||
	(SELECT COUNT(*) FROM temp t
	INNER JOIN johnathan j
	ON j.Year = t.Year AND j.Name = t.Name AND j.Gender = t.Gender)
|| '/' || (SELECT COUNT(*) FROM johnathan);

SELECT 'False Positives: ' || 
	(SELECT COUNT(*) FROM temp t
	 WHERE NOT EXISTS (
		SELECT * FROM johnathan j
		WHERE j.Year = t.Year AND j.Name = t.Name AND j.Gender = t.Gender
	 ));

DROP TABLE temp;

\copy ( SELECT Year, Name, Gender FROM ssa_names WHERE difference(Name, 'Johnathan') = 4 ORDER BY Year ASC, Name ASC, Gender ASC) TO './postgres/johnathan-soundex.csv' WITH CSV DELIMITER ',';