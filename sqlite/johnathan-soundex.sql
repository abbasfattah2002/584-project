.timer ON
SELECT Year, Name, Gender FROM ssa_names WHERE soundex(Name) = soundex('Johnathan');
.timer OFF

CREATE TEMP TABLE temp AS
SELECT Year, Name, Gender FROM ssa_names WHERE soundex(Name) = soundex('Johnathan');

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

-- sqlite3 -header -csv sqlite/data.db "SELECT Year, Name, Gender FROM ssa_names WHERE soundex(Name) = soundex('Johnathan');" > sqlite/johnathan-soundex.csv