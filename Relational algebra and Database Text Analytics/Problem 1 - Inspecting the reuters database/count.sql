/*  
SQL statement to count the number of documents containing the word “parliament”
*/ 

SELECT DISTINCT count(docid)
FROM frequency
WHERE term = "parliament";