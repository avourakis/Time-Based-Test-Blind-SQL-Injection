# Detectify Data Scientist Challenge


## Interpretation: 

My goal was to write an time-based algorithm to identify whether a url is "vulnerable" or "safe" to a blind SQL injection and optimize it for speed and accuracy. This is how the optimizations were interpreted

**Speed:** Make sure that each url tested for a vulnerability only takes a few seconds to complete.

**Accuracy:** Make sure that each test returns less than one false positive result in ten thousand, that is a false positive rate (FPR) of less than 0.0001. The False Negative Rate (FNR) does not need to be optimized to less than one in ten thousand.


## Approach:

After defining the problem at hand, two different approaches were used to try to achieve the goal described above

1. Classification Algorithm

    Seeing that the goal of this time-based algorithm is to "classify" a url as either "vulnerable" or "safe", my first thought was to collect data (Round Trip Times of thousands of vulnerable and safe URLs and their respective classification) and use it to train a Classification model.

     For more details please see `classification_approach.ipynb`

2. Custom algorithm

    This approach involves building a custom algorithm that makes pairs of requests (One with a high sleep delay and another with a low sleep delay) to the url being tested and compare the difference in their RTTs to decide whether the url is vulnerable or safe. 

     For more details please see `custom_approach.ipynb`

## Results and Analysis

Using an out-of-the-box classifier was the first method I used to approach the problem. After testing different classifiers and tweaking their parameters, I decided to use the Support Vector Classifier (SVC). After training the SVC classifier with the RTTs of thousands of urls with different sleep delays, I noticed that in order to make the FPR less than 0.0001, I'd  need to continue to increase the sleep delay, which would make the algorithm take much longer than 10 seconds to test each url.

After doing more research and data exploration, I decided to build a custom time-based algorithm that would allow me to have more control over the parameters that would help me better differientiate between the RTT of vulnerable and safe urls

Here is are some of the performance metrics of each algorithm (approach):

| Approach | Algorithm| FPR | Average Running Time (Seconds) | FNR |
|---|---|---|---|---|
| Classification | SVC | 0.0002 | 7.75 | 0.02 |
| Custom Algorithm | time-based| 0.0000  | 6.2 | 0.0934 |

*As you can clearly see, the SVC algorithm did not meet the speed and accuracy criteria stated above. On the other hand, the Custom Algorithm can be used to test a url within a few seconds with a FPR of less than 0.0001 or (one in ten thousand)*

## Testing URLs

#### *Test a URL using the time-based algorithm. The code can be found inside `time_based_test.py`*

```shell
$ python
```

```python
>>> import time_based_test as tb
>>> 
>>> url = 'http://localhost:5000/vulnerable/1/page?id='
>>> tb.test(url)
1
```

*The same can be done to test a url using the SVC algorithm. The code can be found inside `svc_test.py`*

Other algorithms were used to help collect data