-- https://sqlite.org/forum/info/03324542051ff1f8
-- This was the ticket to get this to work
.load './spellfix1'

.timer ON
SELECT Year, Name, Gender FROM ssa_names WHERE editdist3(Name, 'Katheryne') < 550;
.timer OFF

CREATE TEMP TABLE temp AS
SELECT Year, Name, Gender FROM ssa_names WHERE editdist3(Name, 'Katheryne') < 550;

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

-- sqlite3 -header -csv data.db "SELECT load_extension('./spellfix1'); SELECT Year, Name, Gender FROM ssa_names WHERE editdist3(Name, 'Katheryne') < 400;" > katheryne-edit-distance-sub400.csv