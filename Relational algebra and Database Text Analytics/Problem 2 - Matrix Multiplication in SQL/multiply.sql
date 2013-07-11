/*
Express A X B as a SQL query
*/

SELECT val
FROM(
SELECT A.row_num as row, B.col_num as col, SUM(A.value * B.value) as val
FROM A, B
WHERE A.col_num = B.row_num
GROUP BY A.row_num, B.col_num)
WHERE row = 2 AND col = 3
;


