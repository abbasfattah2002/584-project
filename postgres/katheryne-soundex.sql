CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;

EXPLAIN ANALYZE SELECT Year, Name, Gender FROM ssa_names WHERE difference(Name, 'Katheryne') = 4;

CREATE TEMP TABLE temp AS SELECT Year, Name, Gender FROM ssa_names WHERE difference(Name, 'Katheryne') = 4;

SELECT 'Accuracy: ' ||
	(SELECT COUNT(*) FROM temp t
	INNER JOIN katheryne k
	ON k.Year = t.Year AND k.Name = t.Name AND k.Gender = t.Gender)
|| '/' || (SELECT COUNT(*) FROM katheryne);

SELECT 'False Positives: ' || 
	(SELECT COUNT(*) FROM temp t
	 WHERE NOT EXISTS (
		SELECT * FROM katheryne k
		WHERE k.Year = t.Year AND k.Name = t.Name AND k.Gender = t.Gender
	 ));

DROP TABLE temp;

\copy ( SELECT Year, Name, Gender FROM ssa_names WHERE difference(Name, 'Katheryne') = 4 ORDER BY Year ASC, Name ASC, Gender ASC) TO './postgres/katheryne-soundex.csv' WITH CSV DELIMITER ',';