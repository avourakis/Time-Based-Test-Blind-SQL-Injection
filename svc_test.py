import pickle
import requests
import numpy as np

def test(url):
    svc_model = pickle.load(open('/Users/andres/Documents/Data Science/Detectify Data Science Challenge/svc_final_model.pickle', 'rb'))

    sleep_delay = 2
    resp = requests.get(url + 'SLEEP({})'.format(sleep_delay))
    rtt = np.array(resp.elapsed.total_seconds()).reshape(-1,1)
    
    return svc_model.predict(rtt)[0]