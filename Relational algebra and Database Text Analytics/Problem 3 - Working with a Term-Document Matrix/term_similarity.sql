/*
Find the best matching document to the keyword query "washington taxes treasury"
*/

SELECT MAX(val)
FROM(SELECT  SUM(f1.count * f2.count) as val
FROM frequency as f1, (SELECT * FROM frequency
UNION
SELECT 'q' as docid, 'washington' as term, 1 as count 
UNION
SELECT 'q' as docid, 'taxes' as term, 1 as count
UNION 
SELECT 'q' as docid, 'treasury' as term, 1 as count) as f2
WHERE f1.term = f2.term AND f2.docid  = 'q'
GROUP BY f1.docid, f2.docid);



