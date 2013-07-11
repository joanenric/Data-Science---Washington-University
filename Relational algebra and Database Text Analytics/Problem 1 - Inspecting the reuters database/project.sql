/* 
 SQL statement that is equivalent to the following relational algebra expression. 
πterm( σdocid=10398_txt_earn and count=1(frequency)) U πterm( σdocid=925_txt_trade and count=1(frequency))
*/


SELECT count(term)
FROM frequency
WHERE docid = "10398_txt_earn" AND count = 1;