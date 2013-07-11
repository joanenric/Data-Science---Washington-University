/*
 SQL statement to count the number of unique documents that contain both the word 'transactions' and the word 'world'.
*/

SELECT count(*)
FROM(
SELECT docid
FROM frequency
WHERE term == "world"
INTERSECT
SELECT docid
FROM frequency
WHERE term == "transactions");