/*
SQL statement that is equivalent to the following relational algebra expression.
πterm( σdocid=10398_txt_earn and count=1(frequency))
*/


SELECT count(docid)
FROM frequency
WHERE docid = "10398_txt_earn";