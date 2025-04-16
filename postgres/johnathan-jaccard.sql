CREATE EXTENSION IF NOT EXISTS pg_trgm;

EXPLAIN ANALYZE SELECT Year, Name, Gender FROM ssa_names WHERE similarity(Name, 'Johnathan') > 0.25;

CREATE TEMP TABLE temp AS SELECT Year, Name, Gender FROM ssa_names WHERE similarity(Name, 'Johnathan') > 0.25;

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

\copy ( SELECT Year, Name, Gender FROM ssa_names WHERE similarity(Name, 'Johnathan') > 0.25 ORDER BY Year ASC, Name ASC, Gender ASC) TO './postgres/johnathan-jaccard-gt0.25.csv' WITH CSV DELIMITER ',';
