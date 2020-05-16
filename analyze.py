from nltk import bigrams
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.util import ngrams
import string

stop_words = set(stopwords.words("english"))

def join_comments(comments):
    return ' '.join([comment['text'] for comment in comments])

def is_punctuation(word):
    return word in string.punctuation or all(char in string.punctuation for char in word)

def filter_words (tokens):
    return [token for token in tokens if not is_punctuation(token) and token not in stop_words]

def get_top_most_common(comments, number):
    text = join_comments(comments).lower()
    tokens = word_tokenize(text)

    filtered_words = filter_words(tokens)
    b_grams = bigrams(filtered_words)
    trigrams = ngrams(filtered_words, 3)
    all_tokens = list(filtered_words) + list(b_grams) + list(trigrams)

    frequency_distribution = FreqDist(all_tokens)
    most_common_tokens = frequency_distribution.most_common(number)

    return [[token, freq] for token, freq in most_common_tokens]
