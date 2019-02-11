import pickle
import requests
import numpy as np
import timeit

def test(url):
    '''
    Returns whether a url is vulnerable (label 1) or safe (label 0).
    Uses a trained SVC model to make predictions
    '''

    # Load the trained SVC Model
    svc_model = pickle.load(open('svc_final_model.pickle', 'rb'))

    sleep_delay = 2 # The same sleep delay used during the training of the model
    start = timeit.default_timer()
    _ = requests.get(url + 'SLEEP({})'.format(sleep_delay))
    rtt = np.array(timeit.default_timer() - start).reshape(-1,1)
    
    return svc_model.predict(rtt)[0]
