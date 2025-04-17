DECLARE @JoinCount INT;
DECLARE @JohnathanCount INT;
DECLARE @FalseCount INT;

SET statistics time ON

-- DIFFERENCE score of 4 means no difference
SELECT Year, Name, Gender
FROM [CSE584].[dbo].[ssa_names] WHERE DIFFERENCE(Name, 'Johnathan') = 4

SET statistics time OFF

SELECT Year, Name, Gender INTO #JohnathanSoundex
FROM [CSE584].[dbo].[ssa_names] WHERE DIFFERENCE(Name, 'Johnathan') = 4

SELECT @JoinCount = COUNT(*) FROM #JohnathanSoundex j
INNER JOIN [CSE584].[dbo].[johnathan] s
ON s.Year = j.Year AND s.Name = j.Name AND s.Gender = j.Gender
 
SELECT @JohnathanCount = COUNT(*) FROM [CSE584].[dbo].[johnathan]

SELECT CONCAT('Accuracy: ', @JoinCount, '/', @JohnathanCount)

SELECT @FalseCount = COUNT(*)
FROM #JohnathanSoundex t
WHERE NOT EXISTS (
    SELECT *
    FROM [CSE584].[dbo].[johnathan] j
    WHERE j.Year = t.Year 
    AND j.Name = t.Name 
    AND j.Gender = t.Gender
)

SELECT CONCAT('False positives: ', @FalseCount)

DROP TABLE #JohnathanSoundex