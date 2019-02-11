import random
import asyncio
from aiohttp import ClientSession
import timeit
import csv
import time


async def get_url_rtt(url, session, vulnerable):
    '''
    Collects the request RTT of the "url" passed above and returns it along with and id "i"
    '''
    
    get_url_rtt.start_time[url] = timeit.default_timer()

    async with session.get(url) as response:
        resp = await response.read()
        rtt = timeit.default_timer() - get_url_rtt.start_time[url]

        return (url, rtt, vulnerable)


async def bound(sem, url, session, vulnerable):
    # Getter function with semaphore.
    async with sem:
        response = await get_url_rtt(url, session, vulnerable)
    return response


def save_data(data, num_urls, sleep_delay):
    '''
    Saves the "data" into a CSV file and names it according to the parameters used during the request
    '''

    file_name = 'dataset_{}_{}.csv'.format(str(num_urls), str(sleep_delay))
    num_urls = len(data)

    with open(file_name, 'w') as file:
        writer = csv.writer(file, delimiter=',', lineterminator='\n')
        writer.writerow(['URL', 'Sleep Delay', 'RTT', 'Vulnerable'])
        for i in range(num_urls):
            url = data[i][0]
            rtt = data[i][1]
            vulnerable = data[i][2]
            row = [url, sleep_delay, rtt, vulnerable]
            writer.writerow(row)


async def collect_data(num_urls, sleep_delay):
    '''
    Makes "num_urls" http requests (half vulnerable and have safe) with a "sleep_delay"
    Returns the list of RTTs along with vulnerable (label 1) or safe (label 0)
    '''

    url = "http://localhost:5000/{}/{}/page?id=SLEEP({})"
    tasks = []

    get_url_rtt.start_time = {}
    sem = asyncio.Semaphore(240)
    
    # Create client session that will ensure we dont open new connection
    # per each request.
    async with ClientSession() as session:
        for i in range(1, num_urls + 1):

            # pass Semaphore and session to every GET request
            if i <= int(num_urls/2): # First half
                task = asyncio.ensure_future(bound(sem, url.format("vulnerable", i, sleep_delay), session, 1))
                tasks.append(task)
            else: #Second Half
                task = asyncio.ensure_future(bound(sem, url.format("safe", i, sleep_delay), session, 0))
                tasks.append(task)

        responses = await asyncio.gather(*tasks)

    return responses


def collect_samples(num_urls = 5000, sleep_delay = 1):
    '''
    Collects the RTT of vulnerable and safe urls with a "sleep_delay" and save the result into a CSV file
    To be used for training a classification model
    '''

    start_time = time.time()

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(collect_data(num_urls, sleep_delay))
    loop.run_until_complete(future)

    save_data(future.result(), num_urls, sleep_delay)

    print("This Process took: {} seconds".format(time.time() - start_time))


if __name__ == '__main__':

    collect_samples(5000, 1)

