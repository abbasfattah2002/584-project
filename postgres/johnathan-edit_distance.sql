CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;

EXPLAIN ANALYZE SELECT Year, Name, Gender FROM ssa_names WHERE levenshtein(Name, 'Johnathan') < 3;

CREATE TEMP TABLE tempjohnathan AS SELECT Year, Name, Gender FROM ssa_names WHERE levenshtein(Name, 'Johnathan') < 3;

SELECT 'Accuracy: ' ||
	(SELECT COUNT(*) FROM tempjohnathan tj
	INNER JOIN johnathan j
	ON j.Year = tj.Year AND j.Name = tj.Name AND j.Gender = tj.Gender)
|| '/' || (SELECT COUNT(*) FROM johnathan);

SELECT 'False Positives: ' || 
	(SELECT COUNT(*) FROM tempjohnathan tj
	WHERE NOT EXISTS (
		SELECT * FROM johnathan j
		WHERE j.Year = tj.Year AND j.Name = tj.Name AND j.Gender = tj.Gender
	));

DROP TABLE tempjohnathan;

\copy ( SELECT Year, Name, Gender FROM ssa_names WHERE levenshtein(Name, 'Johnathan') < 3 ORDER BY Year ASC, Name ASC, Gender ASC) TO './postgres/johnathan-edit-distance.csv' WITH CSV DELIMITER ',';
