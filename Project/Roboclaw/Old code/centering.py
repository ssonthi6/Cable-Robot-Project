import cPickle as pickle

def write_origin():
    pickle.dump([str(21.5), str(52.0)], open('data_pickle.pickle', 'wb'))
    return "Location centered at zero"

def read_current():
    test = pickle.load(open('data_pickle.pickle', 'rd'))
    return test
