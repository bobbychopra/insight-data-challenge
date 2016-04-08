"""Twitter Utility Classes Module."""
import collections
from datetime import datetime
from utils.mathext import floor
from sortedcontainers import SortedListWithKey
from dateutil.parser import parse
from dateutil.tz import tzutc


def is_tweet_text(text):
    return 'created_at' in text

def parse_tweet(text):
    """Return Tweet object for raw tweet string."""
    import json
    tweet_json = json.loads(text)
    created_at = tweet_json['created_at']
    hashtags = []
    if 'hashtags' in tweet_json['entities']:
        hashtags = [entry['text'] for entry in tweet_json['entities']['hashtags']]
    return Tweet(created_at, hashtags)


class Tweet(object):
    """Class representing a Tweet."""

    def __init__(self, created_at, hashtags):
        """initialize the tweet class.

        created_at:string
        hashtags:string set
        """
        self.__created_at__ = parse(created_at)
        self.__hashtags__ = set(hashtags)

    @property
    def hashtags(self):
        """get the distinct hashtags for tweet."""
        return self.__hashtags__

    @property
    def created_at(self):
        """get the creation time for tweet."""
        return self.__created_at__

    @property
    def can_become_node(self):
        """check if tweet can become a valid node."""
        return len(self.hashtags) > 1

    def __str__(self):
        """string representing tweet."""
        return 'Hashtags: %s created_at: %s' % (self.hashtags, self.created_at)


class TwitterNode(collections.Iterable):
    """Class representing a Twitter Node or Vertex on Graph."""

    def __init__(self, name, tweet):
        """initialize the node class.

        name:string
        tweet:Tweet
        """
        self.__nodename__ = name
        self.__tweets__ = SortedListWithKey(key=lambda d: d.created_at)
        self.add(tweet)

    @property
    def name(self):
        """get the name for the node."""
        return self.__nodename__

    @property
    def tweets(self):
        """get the tweets for node."""
        return list(self.__tweets__)

    def __iter__(self):
        """iterate through tweets."""
        return self.__tweets__

    def add(self, tweet):
        """add tweet for node."""
        self.__tweets__.add(tweet)

    def remove(self, tweet):
        """add remove for node."""
        self.__tweets__.remove(tweet)

    def __len__(self):
        """len of tweets for node."""
        return len(self.__tweets__)

    def __str__(self):
        """string representing node."""
        return "Name: %s Tweets: %s" % (self.name, self.tweets)


class TwitterNodeGraph(object):
    """Class representing twitter node graph."""

    def __init__(self):
        """initialize the twitter node graph class."""
        self.__nodes__ = dict()
        self.__edges__ = dict()

    @property
    def number_of_nodes(self):
        """get number of nodes."""
        return len(self.__nodes__)

    @property
    def number_of_edges(self):
        """get number of edges."""
        return len(self.__edges__)

    @property
    def average_degree(self, number_of_decimals=2):
        """get average degree of graph."""
        number_of_degrees = 0
        for node in self.__edges__.keys():
            number_of_degrees += len(self.__edges__[node])
        numerator = number_of_degrees
        denominator = self.number_of_nodes * 1.0
        return 0 if number_of_degrees == 0 \
            else floor(numerator / denominator, number_of_decimals)

    def add_edges_for_nodes(self, nodes):
        """add edges to twitter node graph for nodes."""
        edges = [(n1, n2) for n1 in nodes for n2 in nodes if n1 != n2]
        for node1, node2 in edges:
            self.add_edge(node1, node2)

    def add_nodes_from_tweet(self, tweet):
        """add tweet to twitter node graph."""
        if not tweet.can_become_node:
            return
        nodes = []
        for tag in tweet.hashtags:
            nodes.append(self.__get_or_add_node__(tag, tweet))
        self.add_edges_for_nodes(nodes)

    def remove_nodes_from_tweet(self, tweet):
        """remove tweet added twitter node graph."""
        if not tweet.can_become_node:
            return
        nodes = [self.__nodes__[tag] for tag in tweet.hashtags
                 if tag in self.__nodes__]
        # Remove edges between nodes
        edges = [(n1, n2) for n1 in nodes for n2 in nodes if n1 != n2]
        for node1, node2 in edges:
            self.__edges__[node1][node2] -= 1
            if self.__edges__[node1][node2] == 0:
                del self.__edges__[node1][node2]
            if len(self.__edges__[node1]) == 0:
                del self.__edges__[node1]
        # Remove tweet from node
        for node in nodes:
            node.remove(tweet)
        # Remove empty nodes
        empty_nodes = [n for n in nodes if len(n) == 0]
        for node in empty_nodes:
            del self.__nodes__[node.name]
        return nodes

    def __get_or_add_node__(self, name, tweet):
        """get existing node or adds new twitter node."""
        if name not in self.__nodes__:
            node = TwitterNode(name, tweet)
            self.__nodes__[name] = node
        if tweet not in self.__nodes__[name].tweets:
            self.__nodes__[name].add(tweet)
        return self.__nodes__[name]

    def add_edge(self, node1, node2):
        """add an edge between two nodes."""
        if node1 not in self.__edges__:
            self.__edges__[node1] = {}
        if node2 not in self.__edges__[node1]:
            self.__edges__[node1][node2] = 0
        self.__edges__[node1][node2] += 1

    def __str__(self):
        """string representing twitter node graph."""
        return "Nodes: %s Edges: %s" % (str(self.__nodes__), str(self.__edges__))


class TwitterNodeGraphWithSlidingWindow(object):
    """Class representing twitter node graph with a sliding window."""

    def __init__(self, timewindow):
        """initialize the twitter node class.

        timewindow:timedelta
        """
        self.__graph__ = TwitterNodeGraph()
        self.__timewindow__ = timewindow
        self.__tweets__ = SortedListWithKey(key=lambda d: d.created_at)
        # set min timestamp as 1/1/1900 UTC for the tweet
        self.__min_timestamp__ = datetime(1900, 1, 1, tzinfo=tzutc())

    @property
    def timewindow(self):
        """get time window."""
        return self.__timewindow__

    @property
    def tweets(self):
        """get tweets in time window."""
        return self.__tweets__

    @property
    def min_allowed_tweet_datetime(self):
        """get min allowed creation time for tweet."""
        return self.__min_timestamp__

    @property
    def number_of_nodes(self):
        """get number of nodes."""
        return self.__graph__.number_of_nodes

    @property
    def number_of_edges(self):
        """get number of edges."""
        return self.__graph__.number_of_edges

    @property
    def average_degree(self):
        """get average degree of graph."""
        return self.__graph__.average_degree

    def add_tweet(self, tweet):
        """add tweet to the graph."""
        is_tweet_newer = tweet.created_at > self.__min_timestamp__
        if is_tweet_newer:
            self.__add_new_tweet__(tweet)
            timestamp = self.__reset_sliding_window_ts__()
            self.__remove_tweets_older_than_ts__(timestamp)
        return is_tweet_newer

    def __reset_sliding_window_ts__(self):
        """reset the timestamp of the sliding window."""
        last_tweet_at = self.__tweets__[-1].created_at
        self.__min_timestamp__ = last_tweet_at - self.__timewindow__
        return self.__min_timestamp__

    def __add_new_tweet__(self, tweet):
        """add valid new tweet to graph."""
        self.__tweets__.add(tweet)
        self.__graph__.add_nodes_from_tweet(tweet)

    def __remove_tweets_older_than_ts__(self, timestamp):
        """remove any old tweets from graph."""
        index = self.__tweets__.bisect_key_left(timestamp)
        old_tweets = []
        if index > 0:
            old_tweets = self.__tweets__[0:index]
            del self.__tweets__[0:index]
            for tweet in old_tweets:
                self.__graph__.remove_nodes_from_tweet(tweet)
