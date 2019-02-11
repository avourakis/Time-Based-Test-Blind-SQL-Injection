import time
import numpy as np
import random
import time_based_test as tb


def calculate_avg_runtime(function, *args, num_tests = 20):
    '''
    Runs a "function" multiple times ("num_tests" times) and prints the average running time
    '''

    run_times = []

    for i in range(num_tests):

        if i % 2 == 0:
            start_time = time.time()
            function('http://localhost:5000/vulnerable/{}/page?id='.format(i))
            run_times.append(time.time() - start_time)
        else:
            start_time = time.time()
            function('http://localhost:5000/safe/{}/page?id='.format(i))
            run_times.append(time.time() - start_time)
    
    print("The average running time ({} tests) is: {} seconds".format(num_tests, np.mean(run_times)))

if __name__ == '__main__':

    calculate_avg_runtime(tb.test)