"""
Implement a relational join as a MapReduce query:
SELECT * 

FROM Orders, LineItem 

WHERE Order.order_id = LineItem.order_id
"""

import MapReduce
import sys


mr = MapReduce.MapReduce()


counter = 0
def mapper(record):
    global counter
    # key: table identifier
    # value: document contents
    key = record[1]
    value = record
    mr.emit_intermediate(key, value)

def reducer(key, values):
    total=[]
    # key: word
    # values: list of occurrence counts
    order = [value for value in values if value[0] == "order"]
    line_items = [value for value in values if value[0] == "line_item"]
    for l in line_items:
        total.append(order[0] + l)
    for t in total:
        mr.emit(t)

if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
