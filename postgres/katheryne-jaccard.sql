CREATE EXTENSION IF NOT EXISTS pg_trgm;

EXPLAIN ANALYZE SELECT Year, Name, Gender FROM ssa_names WHERE similarity(Name, 'Katheryne') > 0.35;

CREATE TEMP TABLE temp AS SELECT Year, Name, Gender FROM ssa_names WHERE similarity(Name, 'Katheryne') > 0.35;

SELECT 'Accuracy: ' ||
	(SELECT COUNT(*) FROM temp t
	INNER JOIN katheryne j
	ON j.Year = t.Year AND j.Name = t.Name AND j.Gender = t.Gender)
|| '/' || (SELECT COUNT(*) FROM katheryne);

SELECT 'False Positives: ' || 
	(SELECT COUNT(*) FROM temp t
	WHERE NOT EXISTS (
		SELECT * FROM katheryne j
		WHERE j.Year = t.Year AND j.Name = t.Name AND j.Gender = t.Gender
	));

DROP TABLE temp;

\copy ( SELECT Year, Name, Gender FROM ssa_names WHERE similarity(Name, 'Katheryne') > 0.35 ORDER BY Year ASC, Name ASC, Gender ASC) TO './postgres/katheryne-jaccard-gt0.25.csv' WITH CSV DELIMITER ',';
