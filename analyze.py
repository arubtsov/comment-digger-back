from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import string

stop_words = set(stopwords.words("english"))

def join_comments(comments):
    return ' '.join([comment['text'] for comment in comments])

def remove_stop_words(words):    
    return [word for word in words if word not in stop_words]

def is_punctuation(word):
    return word in string.punctuation or all(char in string.punctuation for char in word)

def remove_punctuation(words):
    return [word for word in words if not is_punctuation(word)]

def get_top_most_common(comments, number):
    text = join_comments(comments).lower()
    tokenized_word = remove_punctuation(remove_stop_words(word_tokenize(text)))
    frequency_distribution = FreqDist(tokenized_word)
    most_common = frequency_distribution.most_common(number)

    return [[word, freq] for word, freq in most_common]

