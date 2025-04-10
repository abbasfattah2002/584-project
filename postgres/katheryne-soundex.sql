CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;

EXPLAIN ANALYZE SELECT Year, Name, Gender FROM ssa_names WHERE difference(Name, 'Katheryne') = 4;

CREATE TEMP TABLE tempkatheryne AS SELECT Year, Name, Gender FROM ssa_names WHERE difference(Name, 'Katheryne') = 4;

SELECT 'Accuracy: ' ||
	(SELECT COUNT(*) FROM tempkatheryne tk
	INNER JOIN katheryne k
	ON k.Year = tk.Year AND k.Name = tk.Name AND k.Gender = tk.Gender)
|| '/' || (SELECT COUNT(*) FROM katheryne);

SELECT 'False Positives: ' || 
	(SELECT COUNT(*) FROM tempkatheryne tk
	 WHERE NOT EXISTS (
		SELECT * FROM katheryne k
		WHERE k.Year = tk.Year AND k.Name = tk.Name AND k.Gender = tk.Gender
	 ));

DROP TABLE tempkatheryne;

\copy ( SELECT Year, Name, Gender FROM ssa_names WHERE difference(Name, 'Katheryne') = 4 ORDER BY Year ASC, Name ASC, Gender ASC) TO './postgres/katheryne-soundex.csv' WITH CSV DELIMITER ',';