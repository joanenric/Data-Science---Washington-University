"""
Consider a set of key-value pairs where each key is sequence id and each value is a string of nucleotides, e.g., GCTTCCGAAATGCTCGAA....


Write a MapReduce query to remove the last 10 characters from each string of nucleotides, then remove any duplicates generated.
"""


import MapReduce
import sys


mr = MapReduce.MapReduce()


def mapper(record):
    # key: document identifier
    # value: document contents
    seq_id = record[0]
    nucleotids = record[1] 
    mr.emit_intermediate(nucleotids[:-10], 1)

def reducer(name, friends):
    # key: word
    # value: list of occurrence counts
    mr.emit(name)
        #mr.emit((name, k))
        #mr.emit((k,name))

if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
