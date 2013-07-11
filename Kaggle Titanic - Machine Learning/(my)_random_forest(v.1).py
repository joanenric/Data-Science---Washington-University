# Kaggle Competition Titanic Machine Learning From Disaster.
# Modification of AstroDave Remake by AGC
# from grader: 0.8124
# from kaggle: 0.74163


import csv as csv
import numpy as np
import sklearn as sk
import scipy as sp
from sklearn.ensemble import RandomForestClassifier


def load_data(file_name):
    file_object = csv.reader(open(file_name, 'rb'))
    header = file_object.next()
    data = list(file_object)
    return data

def clean_data(array):
    data = np.array(array)
    offset = 0 if len(data[0,:]) == 11 else -1    

    pclass = offset + 1 #OK
    name = offset + 2   #OK 
    sex = offset + 3 #OK
    age = offset + 4 #OK
    sibl = offset + 5 #OK
    childs = offset + 6 #OK
    ticket = offset + 7 #Falta remove
    price = offset + 8 #OK
    cabin = offset + 9 #Falta assignar int
    embarked = offset + 10 #Falta
      
    
    data[:,pclass] = data[:,pclass].astype(np.int)
    data[data[:,sex] == "female",sex] = 0
    data[data[:,sex] == "male",sex] = 1
    data[data[:,age] == "", age] = np.median(data[data[:,age] != "", age].astype(np.float))    
    data[data[0:,embarked] =='C',embarked] = 0
    data[data[0:,embarked] =='S',embarked] = 1
    data[data[0:,embarked] =='Q',embarked] = 2  
    data[data[0:,embarked] == '',embarked] = np.round(np.mean(data[data[0:,embarked] != '',embarked].astype(np.float)))   
    
    for p in data:
        if p[price] == "":
            p[price] = np.mean(data[(data[:,pclass] == p[pclass]) 
                                    & (data[:,price] != ""), price].astype(np.float))
        if "Mr." in p[name]: p[name] = 1
        if "Mrs." in p[name]: p[name] = 2
        if "Miss" in p[name]: p[name] = 3
        if "Master." in p[name]: p[name] = 4
        else: p[name] = 0
    
        
        if "A" in p[cabin]: p[cabin] = 1
        elif "B" in p[cabin]: p[cabin] = 2
        elif "C" in p[cabin]: p[cabin] = 3
        elif "D" in p[cabin]: p[cabin] = 4
        elif "E" in p[cabin]: p[cabin] = 5
        elif "F" in p[cabin]: p[cabin] = 6
        elif "G" in p[cabin]: p[cabin] = 7
        else: p[cabin] = np.mean([1, 2, 3, 4, 5, 6, 7])

    data = np.delete(data, [name, cabin, ticket], axis = 1)
    return data.astype(np.float)


def performance(output, target):
    temp = np.absolute(np.sum([output, -target.astype(np.float)], axis = 0))
    return np.mean(temp)

def algorithm(train, test):
    rf = RandomForestClassifier(n_estimators=100)
    rf = rf.fit(train[0:,1:], train[0:,0])
    output = rf.predict(test)
    return output

def validate_data(train):
    cv = sk.cross_validation.KFold(len(clean_train), n_folds = 5, indices = False)
    perf = []
    for cv_train, cv_test in cv:
        output = algorithm(train[cv_train], train[cv_test,1:])
        perf.append(performance(output, train[cv_test,0]))
    perf_total = np.mean(np.array(perf).astype(np.float))

    print "The algorithm performance is",1 - perf_total

def write_in_file(file_name, test, output):
    output_file = open(file_name, "wb")
    open_file_object = csv.writer(output_file) 
    for row, out in zip(test, output):
        row.insert(0, int(out))
        open_file_object.writerow(row) 
    output_file.close()    



train = load_data('Data/train.csv')
clean_train = clean_data(train)

validate_data(clean_train)

test = load_data("Data/test.csv")
clean_test = clean_data(test)

output = algorithm(clean_train, clean_test)

write_in_file('Data/(my)_random_forest(v.1).csv', test, output)









