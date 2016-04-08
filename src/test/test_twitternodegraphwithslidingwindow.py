"""Twitter Node Graph With Sliding Window Test Module."""
from datetime import timedelta
import unittest
from utils.twitter import Tweet, TwitterNodeGraphWithSlidingWindow


class TwitterNodeGraphWithSlidingWindowTests(unittest.TestCase):
    """Test for Twitter Node Graph With Sliding Window class."""

    OLDTWEET = Tweet('Thu Mar 24 17:50:09 +0000 2016', ['Apache'])

    TWEET0 = Tweet('Thu Mar 24 17:51:10 +0000 2016', ['Apache', 'Spark'])
    TWEET1 = Tweet('Thu Mar 24 17:51:15 +0000 2016',
                   ['Apache', 'Hadoop', 'Storm'])
    TWEET2 = Tweet('Thu Mar 24 17:51:30 +0000 2016', ['Apache'])
    TWEET3 = Tweet('Thu Mar 24 17:51:55 +0000 2016', ['Flink', 'Spark'])
    TWEET4 = Tweet('Thu Mar 24 17:51:58 +0000 2016', ['HBase', 'Spark'])
    TWEET5 = Tweet('Thu Mar 24 17:52:12 +0000 2016', ['Hadoop', 'Apache'])
    TWEET6 = Tweet('Thu Mar 24 17:52:10 +0000 2016', ['Flink', 'HBase'])
    TWEET7 = Tweet('Thu Mar 24 17:52:20 +0000 2016', ['Kafka', 'Apache'])

    def test_twitternodegraphwithwindow_contains_necessary_details(self):
        """Test for Twitter Node Graph With SlidingWindow has details."""
        td = timedelta(seconds=60)
        graph = TwitterNodeGraphWithSlidingWindow(td)
        graph.add_tweet(self.TWEET3)
        graph.add_tweet(self.TWEET1)
        graph.add_tweet(self.TWEET0)
        graph.add_tweet(self.TWEET2)
        graph.add_tweet(self.TWEET4)
        self.assertEqual(td, graph.timewindow)
        tweets = [self.TWEET0, self.TWEET1, self.TWEET2, self.TWEET3,
                  self.TWEET4]
        self.assertEqual(tweets, list(graph.tweets))
        self.assertEqual(6, graph.number_of_nodes)
        self.assertEqual(6, graph.number_of_edges)
        self.assertEqual(2.0, graph.average_degree)

    def test_twitternodegraphwithwindow_doesnt_add_old_tweet(self):
        """Test for Twitter Node Graph With SlidingWindow does not add
        tweet outside of the window.
        """
        td = timedelta(seconds=60)
        graph = TwitterNodeGraphWithSlidingWindow(td)
        graph.add_tweet(self.TWEET0)
        self.assertEqual(2, graph.number_of_nodes)
        self.assertEqual(2, graph.number_of_edges)
        self.assertEqual(1.0, graph.average_degree)
        has_added = graph.add_tweet(self.OLDTWEET)
        self.assertEqual(False, has_added)
        self.assertEqual([self.TWEET0], list(graph.tweets))

    def test_twitternodegraphwithwindow_removes_old_tweets(self):
        """Test for Twitter Node Graph With SlidingWindow removes
        old tweet outside of the window.
        """
        td = timedelta(seconds=60)
        graph = TwitterNodeGraphWithSlidingWindow(td)
        graph.add_tweet(self.TWEET0)
        graph.add_tweet(self.TWEET2)
        self.assertEqual([self.TWEET0, self.TWEET2], list(graph.tweets))
        self.assertEqual(2, graph.number_of_nodes)
        self.assertEqual(2, graph.number_of_edges)
        self.assertEqual(1.0, graph.average_degree)
        new_tweet = Tweet('Thu Mar 24 17:55:12 +0000 2016', ['Hadoop'])
        graph.add_tweet(new_tweet)
        self.assertEqual([new_tweet], list(graph.tweets))
        self.assertEqual(0, graph.number_of_nodes)
        self.assertEqual(0, graph.number_of_edges)
        self.assertEqual(0.0, graph.average_degree)
        new_tweet = Tweet('Thu Mar 24 17:58:12 +0000 2016', [])
        graph.add_tweet(new_tweet)
        self.assertEqual([new_tweet], list(graph.tweets))
        self.assertEqual(0, graph.number_of_nodes)
        self.assertEqual(0, graph.number_of_edges)
        self.assertEqual(0.0, graph.average_degree)

    def test_twitternodegraphwithwindow_removes_old_tweets_2(self):
        """Test for Twitter Node Graph With SlidingWindow removes
        old tweet outside of the window.
        """
        td = timedelta(seconds=60)
        graph = TwitterNodeGraphWithSlidingWindow(td)
        graph.add_tweet(self.OLDTWEET)
        tweets = [self.TWEET0, self.TWEET1, self.TWEET2, self.TWEET3,
                  self.TWEET4, self.TWEET5]
        for t in tweets:
            graph.add_tweet(t)
        self.assertEqual(tweets[1:], list(graph.tweets))

        graph.add_tweet(self.TWEET6)
        self.assertEqual(2.0, graph.average_degree)
        graph.add_tweet(self.TWEET7)
        self.assertEqual(6, graph.number_of_nodes)
        self.assertEqual(1.66, graph.average_degree)
        new_tweet = Tweet('Thu Mar 24 17:58:12 +0000 2016', ['Hadoop'])
        graph.add_tweet(new_tweet)
        self.assertEqual([new_tweet], list(graph.tweets))
        self.assertEqual(0, graph.number_of_nodes)
        self.assertEqual(0, graph.number_of_edges)
        self.assertEqual(0.0, graph.average_degree)
        # test for last tweet with high createdAt but no hashtags coming in
