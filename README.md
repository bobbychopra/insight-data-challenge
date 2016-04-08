Insight Data Engineering - Coding Challenge
===========================================================

I am using Python 2.7.11 for the coding challenge 
```
admins-MacBook-Air:insight-data-challenge admin$ python
Python 2.7.11 (default, Jan 22 2016, 08:29:18) 
[GCC 4.2.1 Compatible Apple LLVM 7.0.2 (clang-700.1.81)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```


I used the parser.parse method of the `python-dateutil` module to parse date and time in the raw tweet json and used the SortedListWithKey collection from the `sortedcontainers` module to maintain an ordered collection of tweets based on their created_at timestamps. 
Please use [pip](https://pip.pypa.io/en/stable/quickstart/) to install the required python modules by running the command _pip install -r requirements.txt_ 
```
(venv) admins-MacBook-Air:insight-data-challenge admin$ pip install -r requirements.txt 
Collecting python-dateutil==2.5.2 (from -r requirements.txt (line 1))
  Using cached python_dateutil-2.5.2-py2.py3-none-any.whl
Collecting six==1.10.0 (from -r requirements.txt (line 2))
  Using cached six-1.10.0-py2.py3-none-any.whl
Collecting sortedcontainers==1.4.4 (from -r requirements.txt (line 3))
Installing collected packages: six, python-dateutil, sortedcontainers
Successfully installed python-dateutil-2.5.2 six-1.10.0 sortedcontainers-1.4.4
```

There are 4 classes in `src/utils/twitter.py` that help calculate the average degree of a vertex in a Twitter hashtag graph for the last 60 seconds, and update this each time a new tweet appears

1. Tweet Class - Represents a Tweet with has some attributes defined
1. TweetWithRawData Class - Derived class of Tweet, which contains the raw text   
1. TwitterNode Class - Represents a Twitter Vertex or Node on the Graph 
1. TwitterNodeGraph Class - Represents a graph with Twitter Vertices or Nodes and Edges between them
1. TwitterNodeGraphWithSlidingWindow Class - Similar to TwitterNodeGraph but has a sliding window  
