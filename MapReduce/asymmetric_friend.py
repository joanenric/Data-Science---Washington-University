"""
Generate a list of all non-symmetric friend relationships.
"""

import MapReduce
import sys

mr = MapReduce.MapReduce()


def mapper(record):
    # key: document identifier
    # value: document contents
    name = record[0]
    friend = record[1] 
    mr.emit_intermediate(tuple(sorted((name, friend))), 1)

def reducer(name, friends):
    # key: word
    # value: list of occurrence counts
    if  len(friends) == 1:   
        mr.emit(name)
        mr.emit(name[::-1])
        #mr.emit((name, k))
        #mr.emit((k,name))

if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
