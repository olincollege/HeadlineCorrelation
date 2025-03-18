import random
from nltk.corpus import twitter_samples
from nltk.tokenize import word_tokenize


def load_data():
    """
    Loads known positive and negative datasets from nltk
    """
    # Load twitter samples dataset
    positive_tweets = twitter_samples.strings("positive_tweets.json")
    negative_tweets = twitter_samples.strings("negative_tweets.json")

    # Combine the datasets and create labels
    tweets = positive_tweets + negative_tweets
    labels = ["Positive"] * len(positive_tweets) + ["Negative"] * len(
        negative_tweets
    )

    # Shuffle the dataset
    combined = list(zip(tweets, labels))
    random.shuffle(combined)
    tweets, labels = zip(*combined)

def tokenize():
    '''
    Tokenizes words

    Returns:
        tokens: list of words/tokens
    '''
    sample_text = "NLTK is a powerful library for NLP."
    tokens = word_tokenize(sample_text)
    return tokens
