CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;

EXPLAIN ANALYZE SELECT Year, Name, Gender FROM ssa_names WHERE levenshtein(Name, 'Johnathan') < 2;

CREATE TEMP TABLE temp AS SELECT Year, Name, Gender FROM ssa_names WHERE levenshtein(Name, 'Johnathan') < 2;

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

\copy ( SELECT Year, Name, Gender FROM ssa_names WHERE levenshtein(Name, 'Johnathan') < 2 ORDER BY Year ASC, Name ASC, Gender ASC) TO './postgres/johnathan-edit-distance-sub2.csv' WITH CSV DELIMITER ',';
