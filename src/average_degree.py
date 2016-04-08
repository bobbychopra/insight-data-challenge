"""Calculate the average degree of a vertex in a Twitter hashtag graph for the last 60 seconds"""
import sys
from datetime import timedelta
from utils.twitter import parse_tweet, is_tweet_text, TwitterNodeGraphWithSlidingWindow

def readfile(filepath):
    """Read each line of file as generator"""
    with open(filepath, mode='r') as finput:
        for line in finput:
            yield line

def main():
    """Process tweets to calculate average degree for last 60 seconds."""
    if len(sys.argv) != 3:
        raise ValueError("usage: average_degree.py path_to_tweets.txt path_to_output.txt")
    input_file, output_file = sys.argv[1:]
    print input_file, output_file
    graph = TwitterNodeGraphWithSlidingWindow(timedelta(seconds=60))
    tweets = (parse_tweet(text) for text in readfile(input_file) if is_tweet_text(text))
    with open(output_file, mode='w') as foutput:
        # use generator style syntax, rather than list comprehensions to handle
        #  large file contents
        for tweet in tweets:
            # add tweet only if within sliding window timestamp
            #  didn't want this to be a method on graph, as it seems
            #  like a concern on processing side
            if tweet.created_at > graph.min_allowed_tweet_datetime:
                graph.add_tweet(tweet)
                foutput.write("%.2f\n" % graph.average_degree)

if __name__ == '__main__':
    sys.exit(int(main() or 0))
