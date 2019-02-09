import pickle
import requests
import numpy as np
import timeit

def test(url):
    svc_model = pickle.load(open('/Users/andres/Documents/Data Science/Detectify Data Science Challenge/svc_final_model.pickle', 'rb'))

    sleep_delay = 3
    start = timeit.default_timer()
    resp = requests.get(url + 'SLEEP({})'.format(sleep_delay))
    rtt = np.array(timeit.default_timer() - start).reshape(-1,1)
    
    return svc_model.predict(rtt)[0]



for i in range(1,21):
    times = []

    if(i % 2 == 0):
        print('Predict 0: ')
        url = 'http://localhost:5000/{}/{}/page?id='.format('safe', i)
    else:
        print('Predict 1: ')
        url = 'http://localhost:5000/{}/{}/page?id='.format('vulnerable', i)
    start = timeit.default_timer()
    print(test(url))
    times.append(timeit.default_timer() - start)


print(np.mean(times))
