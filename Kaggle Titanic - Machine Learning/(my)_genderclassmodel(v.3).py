# Kaggle Competition Titanic Machine Learning From Disaster.
# Modification of AstroDave Remake by AGC
# Inclusions:
# A. manage the NaN elements 0: male, 1: female
# Improvement from 0.8080 to 0.8080
# Improvement in Kaggle from 0.77990 to 0.77990
# B. Include age as a decisor
# Improvement from 0.8080 to 0.820
# Improvement in Kaggle from 0.77990 to 0.77512

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
      
    
    data[:,pclass] = data[:,pclass].astype(np.int) - 1
    data[data[:,sex] == "female",sex] = 0
    data[data[:,sex] == "male",sex] = 1
    data[data[:,age] == "", age] = np.median(data[data[:,age] != "", age].astype(np.float))    
    for p in data:
        if p[price] == "":
            p[price] = np.mean(data[(data[:,pclass] == p[pclass]) 
                                    & (data[:,price] != ""), price].astype(np.float))
        if "Mr." in p[name]: p[name] = 1
        if "Mrs." in p[name]: p[name] = 2
        if "Miss" in p[name]: p[name] = 3
        if "Master." in p[name]: p[name] = 4
        else: p[name] = 0
        if p[embarked] == "C": p[embarked] = 0
        elif p[embarked] == "S": p[embarked] = 1
        elif p[embarked] == "Q": p[embarked] = 2
        elif p[embarked] == "": p[embarked] = 1
        
        if "A" in p[cabin]: p[cabin] = 1
        elif "B" in p[cabin]: p[cabin] = 2
        elif "C" in p[cabin]: p[cabin] = 3
        elif "D" in p[cabin]: p[cabin] = 4
        elif "E" in p[cabin]: p[cabin] = 5
        elif "F" in p[cabin]: p[cabin] = 6
        elif "G" in p[cabin]: p[cabin] = 7
        else: p[cabin] = np.mean([1, 2, 3, 4, 5, 6, 7])

    data = np.delete(data, [ticket], axis = 1)
    return data.astype(np.float)

def algorithm(train, test):
    ## select data imput    
    #offset = 0 if len(train[0,:]) == 10 else -1 
    offset = 0
    ##indices
    pclass = offset + 1 #OK
    name = offset + 2   #OK 
    sex = offset + 3 #OK
    age = offset + 4 #OK
    sibl = offset + 5 #OK
    childs = offset + 6 #OK
    price = offset + 7 #OK
    cabin = offset + 8 #Falta assignar int
    embarked = offset + 9 #Falta
    
    ## variables of the decision table
    price_max = 40
    price_bin = 10
    n_prices = price_max // price_bin
    train[train[:,price] >= price_max,price] = price_max - 1
    age_max = 40
    age_bin = 10
    n_ages = age_max // age_bin
    train[train[:,age] >= price_max,age] = age_max - 1    
    n_classes = 3
    
    ##decision table
    decision_t = np.zeros([2,n_classes,n_prices, n_ages],float)
    for page in xrange(n_ages):
        for pclass_i in xrange(n_classes):
            for pprice in xrange(n_prices):
                for psex in xrange(2):
                    element = train[(train[0::,sex] == psex) \
                        & (train[0::,pclass].astype(np.float) == pclass_i) \
                        & (train[0:,price].astype(np.float) // price_bin== pprice) \
                        & (train[0:,age].astype(np.float)// age_bin == page), 0]                
                    decision_t[psex, pclass_i, pprice, page] = np.mean(element)
    
    #print decision_t, "\n\n\n"
    
    decision_t = replace_NaN(decision_t)
    decision_t = round_table(decision_t)
    
    output = []
    test[test[:,price-1] >= price_max,price-1] = price_max - 1
    test[test[:,age-1] >= age_max,age-1] = age_max - 1
    for p in test:
        output.append(decision_t[p[sex-1].astype(np.int), p[pclass-1].astype(np.int), int(p[price-1] // price_bin), int(p[age-1] // age_bin)])
    output = np.array(output).astype(np.int)
    return output
    
def replace_NaN(decision_t):
    ##put zeros
    #decision_t[decision_t != decision_t] = 0
    ##check sex
    decision_t[0, decision_t[0,] != decision_t[0,]] = 1
    decision_t[1, decision_t[1,] != decision_t[1,]] = 0
    return decision_t

def round_table(decision_t):
    decision_t[decision_t < 0.5] = 0
    decision_t[decision_t >= 0.5] = 1 
    return decision_t
    
def performance(output, target):
    temp = np.absolute(np.sum([output, -target.astype(np.float)], axis = 0))
    return np.mean(temp)
    
#performance = 1 - np.mean(results)

def validate_data(train):
    cv = sk.cross_validation.KFold(len(clean_train), n_folds = 10, indices = False)
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

write_in_file('Data/(my)_genderclassmodel(v.3).csv', test, output)

