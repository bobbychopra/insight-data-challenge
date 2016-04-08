"""Tweet Test Module."""
import unittest
from dateutil.parser import parse
from utils.twitter import Tweet, parse_tweet


class TweetTests(unittest.TestCase):
    """Test for Tweet class."""


    TAGS = ["alpha", "beta", "gamma"]
    CREATION_TS = 'Thu Mar 24 17:50:01 +0000 2016'
    CREATED_AT = parse(CREATION_TS)

    def test_tweet_contains_unique_hashtags(self):
        """test if the tweet contains unique hashtags."""
        duplicate_tags = self.TAGS + [self.TAGS[0]]
        tweet = Tweet(self.CREATION_TS, duplicate_tags)
        self.assertEqual(set(duplicate_tags), tweet.hashtags)

    def test_tweet_contains_unique_casesensitive_hashtags(self):
        """test if the tweet contains unique case sensitive hashtags."""
        duplicate_tags = self.TAGS + [self.TAGS[0].upper()]
        tweet = Tweet(self.CREATION_TS, duplicate_tags)
        self.assertEqual(set(duplicate_tags), tweet.hashtags)

    def test_tweet_parses_timestamp(self):
        """test if the tweet parses the string timestamp."""
        tweet = Tweet(self.CREATION_TS, self.TAGS)
        self.assertEqual(self.CREATED_AT, tweet.created_at)

if __name__ == '__main__':
    unittest.main()
