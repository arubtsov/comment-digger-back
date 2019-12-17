from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
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
    filtered_words = filter_words(word_tokenize(text))
    frequency_distribution = FreqDist(filtered_words)
    most_common = frequency_distribution.most_common(number)

    return [[word, freq] for word, freq in most_common]

