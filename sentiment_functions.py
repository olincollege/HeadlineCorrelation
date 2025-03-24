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


def tokenize(sample_text):
    """
    Tokenizes words

    Arg:
        sample_text: string of text to be tokenized

    Returns:
        tokens: list of words/tokens
    """
    tokens = word_tokenize(sample_text)
    return tokens


from nltk.corpus import stopwords


def remove_stopwords(tokens):
    """
    Removes words that don't mean anything

    Arg:
        tokens: list of tokens

    Returns:
        filtered_tokens: list of filtered tokens
    """
    stop_words = set(stopwords.words("english"))
    filtered_tokens = [
        word for word in tokens if word.lower() not in stop_words
    ]
    return filtered_tokens


# Stemming and Lemmatization
# This step turns the words into their root cases
# For example - 'powerful' is converted to 'power'

from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer


def stem_and_lem(filtered_tokens):
    """
    Turns words into their root cases

    Args:
        filtered_tokens: list of filtered tokens
    Returns:

    """
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    stemmed_tokens = [stemmer.stem(word) for word in filtered_tokens]
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
    return stemmed_tokens, lemmatized_tokens


# Feature detection
from nltk.probability import FreqDist

all_words = [word.lower() for tweet in tweets for word in word_tokenize(tweet)]
all_words_freq = FreqDist(all_words)

# Select the top 2000 words as features
word_features = list(all_words_freq.keys())[:2000]


def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features["contains({})".format(word)] = word in document_words
    return features


# Create feature sets for training and testing
feature_sets = [
    (document_features(word_tokenize(tweet)), label)
    for (tweet, label) in zip(tweets, labels)
]
train_set, test_set = feature_sets[1000:], feature_sets[:1000]

# Building a sentiment analysis model
from nltk.classify import NaiveBayesClassifier

classifier = NaiveBayesClassifier.train(train_set)


import nltk.classify.util

accuracy = nltk.classify.util.accuracy(classifier, test_set)
print(f"Accuracy: {accuracy * 100:.2f}%")


# Classifying a new sentence using the trained classifier
test_sentence = "bad"
test_features = document_features(word_tokenize(test_sentence))
classification = classifier.classify(test_features)
print(classification)

# nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sid = SentimentIntensityAnalyzer()
text = "love"
sentiment_scores = sid.polarity_scores(text)
print(sentiment_scores)
