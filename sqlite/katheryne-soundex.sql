.timer ON
SELECT Year, Name, Gender FROM ssa_names WHERE soundex(Name) = soundex('Katheryne');
.timer OFF

CREATE TEMP TABLE temp AS
SELECT Year, Name, Gender FROM ssa_names WHERE soundex(Name) = soundex('Katheryne');

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

-- sqlite3 -header -csv sqlite/data.db "SELECT Year, Name, Gender FROM ssa_names WHERE soundex(Name) = soundex('Katheryne');" > sqlite/katheryne-soundex.csv