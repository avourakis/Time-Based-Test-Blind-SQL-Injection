import pickle
import requests
import numpy as np
import timeit

def test(url):
    
    # Load the trained SVC Model
    svc_model = pickle.load(open('svc_final_model.pickle', 'rb'))

    sleep_delay = 2 # The same sleep delay used during the training of the model
    start = timeit.default_timer()
    resp = requests.get(url + 'SLEEP({})'.format(sleep_delay))
    rtt = np.array(timeit.default_timer() - start).reshape(-1,1)
    
    return svc_model.predict(rtt)[0]
