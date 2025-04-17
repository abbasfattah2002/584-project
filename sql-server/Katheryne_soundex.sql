DECLARE @JoinCount INT;
DECLARE @KatheryneCount INT;
DECLARE @FalseCount INT;

SET statistics time ON

SELECT Year, Name, Gender
FROM [CSE584].[dbo].[ssa_names] WHERE DIFFERENCE(Name, 'Katheryne') = 4

SET statistics time OFF

SELECT Year, Name, Gender INTO #KatheryneSoundex
FROM [CSE584].[dbo].[ssa_names] WHERE DIFFERENCE(Name, 'Katheryne') = 4

SELECT @JoinCount = COUNT(*) FROM #KatheryneSoundex s
INNER JOIN [CSE584].[dbo].[katheryne] k
ON s.Year = k.Year AND s.Name = k.Name AND s.Gender = k.Gender
 
SELECT @KatheryneCount = COUNT(*) FROM [CSE584].[dbo].[katheryne]

SELECT CONCAT('Accuracy: ', @JoinCount, '/', @KatheryneCount)

SELECT @FalseCount = COUNT(*)
FROM #KatheryneSoundex t
WHERE NOT EXISTS (
    SELECT *
    FROM [CSE584].[dbo].[katheryne] k
    WHERE k.Year = t.Year 
    AND k.Name = t.Name 
    AND k.Gender = t.Gender
)

SELECT CONCAT('False positives: ', @FalseCount)

DROP TABLE #KatheryneSoundex