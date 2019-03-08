# Time-based test for Blind SQL injection


## Goal: 

My goal was to write a time-based algorithm to identify whether a url is "vulnerable" or "safe" to a blind SQL injection and optimize it for speed and specificity. This is how the optimization will be approached:

**Speed:** Make sure that testing a single for a vulnerability only takes a few seconds to complete.

**Specificity:** Make sure that each test returns less than one false positive result in ten thousand, that is a false positive rate (FPR) of less than 0.0001. *The False Negative Rate (FNR) does not need to be optimized to less than 0.0001*.


## Approach:

After defining the problem at hand, two different approaches were used to try to achieve the goal described above

1. Classification Algorithm

    Seeing that the goal of this time-based algorithm is to "classify" a url as either "vulnerable" or "safe", my first thought was to collect data, round trip time (RTT) of thousands of vulnerable and safe URLs and their respective classification, and use it to train a Classification model.

     For more details please see `classification_approach.ipynb`

2. Custom algorithm

    This approach involves building a custom algorithm that makes pairs of requests (One with a high sleep delay and another with a low sleep delay) to the url being tested and compare the difference in their RTT to decide whether the url is vulnerable or safe. 

     For more details please see `custom_approach.ipynb`

## Results and Analysis

Using an out-of-the-box classifier was the first method I used to approach the problem. After testing different classifiers and tweaking their parameters, I decided to use a Support Vector Classifier (SVC). After training the SVC with the RTTs of thousands of urls with different sleep delays, I noticed that in order to achieve a FPR of less than 0.0001, I'd need to continue to increase the sleep delay, which would make the algorithm take much longer than 10 seconds to test each url. I also encountered other issues with the training data I collected, which I explain in more detail in the appropriate jupyter notebook.

After doing more research and data exploration, I decided to build a custom time-based algorithm that would give me more control over the parameters that would allow me to increase the speed of the test and minimize the FPR.

Here are some of the performance metrics I collected for each approach:

| Approach | Algorithm| FPR | Average Running Time (Seconds) | FNR |
|---|---|---|---|---|
| Classification | SVC | 0.0002 | 7.75 | 0.02 |
| Custom Algorithm | time-based| 0.0000  | 7.5 | 0.0934 |

*As you can clearly see, the SVC algorithm did not meet the speed and specificity criteria stated above. On the other hand, the custom time-based algorithm can be used to test a url within a few seconds with a FPR of less than 0.0001 (one in ten thousand)*

## Testing URLs

#### Here is an example of how to test a single URL using the custom time-based algorithm. The code can be found inside `time_based_test.py`

```shell
$ python3
```

```python
>>> import time_based_test as tb
>>> 
>>> url = 'http://localhost:5000/vulnerable/1/page?id='
>>> tb.test(url)
1
```

*Requirements: numpy 1.16.0 and aiohttp 3.54*



The same can be done to test a url using the SVC algorithm. The code can be found inside `Other/svc_test.py`

Code used to collect training data and test predictions (as well as some extra data collected) can be found inside the `Other` folder.

