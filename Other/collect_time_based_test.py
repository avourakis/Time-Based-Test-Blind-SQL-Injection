import csv
import asyncio
import time
import timeit
from aiohttp import ClientSession
from aiohttp import TCPConnector
import time_based_test as tb  # Make sure time_based_test.py is in the same directory as this script or inside the site-packages folder


async def collect_test_data(page_type, num_tests, high, low, num_requests, diff):
    '''
    Tests urls asynchronously
    '''

    url = 'http://localhost:5000/{}/{}/page?id='
    tasks = []
    socket_limit = 240 # The current limit in my machine
    sem = asyncio.Semaphore(socket_limit / num_requests)

    for i in range(1, num_tests + 1):

        task = asyncio.ensure_future(tb.scan_url(url.format(page_type, i), high, low, num_requests, sem))
        tasks.append(task)

    resp = await asyncio.gather(*tasks)

    return resp


def save_results(page_type, test_data, num_tests, high, low, num_requests, diff):
    '''
    Saves the results from the "test_data" into a CSV file and names the file according to the parameters used during the test
    '''

    file_name = '{}_results_{}_{}_{}_{}_{}.csv'.format(page_type, str(num_tests), str(high), str(low), str(num_requests), str(diff))
    
    with open(file_name, 'w') as file:
        file.write('Test Result\n')
        for result in test_data:
            file.write(str(result) + '\n')


def collect_samples(p_type = 'safe', num_tests = 10000, high = 0.8, low = 0.03, num_requests = 24, diff = 3):
    '''
    Tests urls and saves the results in a CSV file
    '''
    
    start_time = time.time()

    # Tests urls asynchronously
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(collect_test_data(p_type, num_tests, high, low, num_requests, diff))
    loop.run_until_complete(future)

    test_results = [tb.analyze_rtts(rtt, diff) for rtt in future.result()]
    save_results(p_type, test_results, num_tests, high, low, num_requests, diff)

    print("This Process took: {} seconds".format(time.time() - start_time))


if __name__ == '__main__':

    #collect_samples(p_type = 'safe', num_tests = 10000, num_requests = 24, diff = 3.5)
    collect_samples(p_type = 'safe', num_tests = 10500, high = 0.8, low = 0.03, num_requests = 24, diff = 2)
    collect_samples(p_type = 'vulnerable', num_tests = 10500, high = 0.8, low = 0.03, num_requests = 24, diff = 2)
    #collect_samples(p_type = 'vulnerable', num_tests = 10000, num_requests = 24, diff = 3)
    #collect_samples(p_type = 'safe', num_tests = 10000, num_requests = 12, diff = 3)
    #collect_samples(p_type = 'vulnerable', num_tests = 10000, num_requests = 12, diff = 3)
