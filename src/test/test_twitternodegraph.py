"""Twitter Node Graph Test Module."""
import unittest
from utils.twitter import Tweet, TwitterNodeGraph


class TwitterNodeGraphTests(unittest.TestCase):
    """Test for Twitter Node Graph class."""

    TWEET0 = Tweet('Thu Mar 24 17:51:10 +0000 2016', ['Apache', 'Spark'])
    TWEET1 = Tweet('Thu Mar 24 17:51:15 +0000 2016',
                   ['Apache', 'Hadoop', 'Storm'])
    TWEET2 = Tweet('Thu Mar 24 17:51:30 +0000 2016', ['Apache'])
    TWEET3 = Tweet('Thu Mar 24 17:51:55 +0000 2016', ['Flink', 'Spark'])
    TWEET4 = Tweet('Thu Mar 24 17:51:58 +0000 2016', ['HBase', 'Spark'])

    def test_twitternodegraph_contains_necessary_details(self):
        """test if the tweet contains unique nodes and edges."""
        graph = TwitterNodeGraph()
        self.assertEqual(0, graph.number_of_nodes)
        self.assertEqual(0, graph.number_of_edges)
        self.assertEqual(0.0, graph.average_degree)
        
    
    def test_twitternodegraph_add_tweet_with_one_hash_contains_necessary_details(self):
        """test if the tweet contains unique nodes and edges."""
        graph = TwitterNodeGraph()
        graph.add_nodes_from_tweet(self.TWEET2)
        self.assertEqual(0, graph.number_of_nodes)
        self.assertEqual(0, graph.number_of_edges)
        self.assertEqual(0.0, graph.average_degree)

    def test_twitternodegraph_add_same_tweet_contains_necessary_details(self):
        """test if the graph adds new tweet correctly."""
        graph = TwitterNodeGraph()
        graph.add_nodes_from_tweet(self.TWEET0)
        self.assertEqual(2, graph.number_of_nodes)
        self.assertEqual(2, graph.number_of_edges)
        self.assertEqual(1.0, graph.average_degree)
        graph.add_nodes_from_tweet(self.TWEET1)
        self.assertEqual(4, graph.number_of_nodes)
        self.assertEqual(4, graph.number_of_edges)
        self.assertEqual(2.0, graph.average_degree)

    def test_twitternodegraph_add_same_tweet_contains_necessary_details2(self):
        """test if the graph adds new tweet correctly."""
        graph = TwitterNodeGraph()
        graph.add_nodes_from_tweet(self.TWEET0)
        graph.add_nodes_from_tweet(self.TWEET1)
        graph.add_nodes_from_tweet(self.TWEET2)
        graph.add_nodes_from_tweet(self.TWEET3)
        self.assertEqual(5, graph.number_of_nodes)
        self.assertEqual(5, graph.number_of_edges)
        self.assertEqual(2.0, graph.average_degree)
        graph.add_nodes_from_tweet(self.TWEET4)
        self.assertEqual(6, graph.number_of_nodes)
        self.assertEqual(6, graph.number_of_edges)
        self.assertEqual(2.0, graph.average_degree)


if __name__ == '__main__':
    unittest.main()
