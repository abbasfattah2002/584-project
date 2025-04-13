-- https://sqlite.org/forum/info/03324542051ff1f8
-- This was the ticket to get this to work
.load './spellfix1'

.timer ON
SELECT Year, Name, Gender FROM ssa_names WHERE editdist3(Name, 'Johnathan') < 300;
.timer OFF

CREATE TEMP TABLE temp AS
SELECT Year, Name, Gender FROM ssa_names WHERE editdist3(Name, 'Johnathan') < 300;

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

-- sqlite3 -header -csv data.db "SELECT load_extension('./spellfix1'); SELECT Year, Name, Gender FROM ssa_names WHERE editdist3(Name, 'Johnathan') < 300;" > johnathan-edit-distance-sub3.csv