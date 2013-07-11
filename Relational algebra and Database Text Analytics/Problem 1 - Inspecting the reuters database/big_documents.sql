/* 
SQL statement to find all documents that have more than 300 total terms, including duplicate terms.
*/


SELECT count(*)
FROM(
SELECT docid
FROM frequency
GROUP BY docid
HAVING SUM(count) > 300);