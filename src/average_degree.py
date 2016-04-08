"""Calculate the average degree of a vertex in a Twitter hashtag graph for the last 60 seconds"""
import sys

def main():
    """Process tweets to calculate average degree for last 60 seconds."""
    if len(sys.argv) != 3:
        raise ValueError("usage: average_degree.py path_to_tweets.txt path_to_output.txt")
    input_file, output_file = sys.argv[1:]
    print input_file, output_file

if __name__ == '__main__':
    sys.exit(int(main() or 0))
