import numpy as np
import asyncio
import timeit
import time
from aiohttp import ClientSession
from aiohttp import TCPConnector
import csv
import time_based_test as tb  # Make sure time_based_test.py is in the same directory as this script or inside the site-packages folder


def save_data(data, num_urls, high, low):
    '''
    Saves the results from the "data" into a CSV file and names the file according to the parameters used during the test
    '''

    file_name = 'safe_pairs_{}_{}_{}.csv'.format(str(num_urls), str(high), str(low))
    num_urls = len(data)

    with open(file_name, 'w') as file:
        writer = csv.writer(file, delimiter=',', lineterminator='\n')
        writer.writerow(['URL', 'High Delay', 'RTT'])
        for i in range(num_urls):

            url = data[i][2]
            rtt = data[i][1]

            if data[i][0] % 2 == 0:
                writer.writerow([url, rtt])
            else:
                writer.writerow([url, rtt])


def collect_samples(url, high, low, num_urls):
    '''
    Collects and Saves into CSV file the RTTs for two sets of requests, one set of requests with a high sleep delay
    and the other half with a "low" sleep delay
    '''

    start_time = time.time()

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(tb.scan_url(url, high, low, num_urls))
    loop.run_until_complete(future)
    save_data(future.result(), num_urls, high, low)

    print("This Process took: {} seconds".format(time.time() - start_time))


if __name__ == '__main__':

    url = 'http://localhost:5000/safe/1/page?id='
    high = 0.7
    low = 0.05
    num_urls = 50
    
    collect_samples(url, high, low, num_urls)
