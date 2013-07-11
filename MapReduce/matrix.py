
"""
Assume you have two matrices A and B in a sparse matrix format, where each record is of the form i, j, value.  Design a MapReduce algorithm to compute matrix multiplication: A x B
"""

import MapReduce
import sys

mr = MapReduce.MapReduce()


def mapper(record):
    matrix = record [0]
    row = record [1]
    col = record [2]
    val = record [3]
    if matrix == "a":
        for i in range(10):
            t = (row, i)
            mr.emit_intermediate(t, record)    
    else:
        for i in range(10):
            t = (i, col)
            mr.emit_intermediate(t, record)    
count = 0
def reducer(key, values):
    global count
    # key: word
    # value: list of occurrence counts    
    #vec_a = [v[3] for v in values if v[0] == "a"]
    #vec_b = [v[3] for v in values if v[0] == "b"]
    result = 0
    a = [0]*10
    b = [0]*10
    for v in values:
        if v[0] == "a":
            a[v[2]] = v[3]
        else:
            b[v[1]] = v[3]
    #print a, b
    for ai, bi in zip(a, b):
        result += ai * bi
    if result > 0:
        mr.emit((key[0], key[1], result))
            
if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
