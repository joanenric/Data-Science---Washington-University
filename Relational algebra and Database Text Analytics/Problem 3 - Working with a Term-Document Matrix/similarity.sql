/*
query to compute the similarity matrix DDT
*/


#solution of the exercise
SELECT  SUM(f1.count * f2.count) as val
FROM frequency as f1, frequency as f2
WHERE f1.term = f2.term AND docid  = '10080_txt_crude' AND docid = '17035_txt_earn'
GROUP BY f1.docid, f2.docid;