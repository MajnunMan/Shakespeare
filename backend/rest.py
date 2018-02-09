from numpy import asarray
from numpy import zeros
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import Embedding
import numpy as np
from keras.models import Model
from keras.layers import Input, Dense, Embedding, SimpleRNN, LSTM, GRU
from keras.preprocessing.text import text_to_word_sequence
import csv
import statistics
import pickle
from keras.models import model_from_json
import json

vocab_size = 20000
maxlen = 80

def preprocess_sequences(seq, vocab_size, maxlen):
    out = []
    out = [[word for word in rev if word < vocab_size] for rev in seq]
    out = [([0] * (maxlen - len(rev)) + rev )[:maxlen] for rev in out]
    return np.array(out)

# loading
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)
# later...
 
# load json and create model
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model.h5")
print("Loaded model from disk")
 
loaded_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

def words2sequences(words):
    return [word2num[w]+3 if w in word2num else 2 for w in text_to_word_sequence(words)]
def sentences2sequences(sentences):
    return [[1] + words2sequences(s) for s in sentences]

myreviews = [
    "Racism against white people? Noooo, no such thing. Dunno what u talkin' about! Now hold my beer while I spray paint 'fuck whites' on this ad for Mexican food cuz that makes sense.", # fill this with good review
    "It was the worst movie ever seen. It is just waste of time and money. Dont go with anyone if you dont want to torchure them." # fill this with bad review
]

### LSI Similarities
# Tokenize Corpus and filter out anything that is a
# stop word or has a frequency <1

from gensim import corpora, models, similarities
from collections import defaultdict
import numpy as np

import json


tweets = []
with open('truncated.json') as json_file:  
    data = json.load(json_file)
    for row in data:
        tweets.append([row["text"], row])

documents = np.array(tweets)[:,0]

stoplist = set(['is', 'how'])

texts = [[word.lower() for word in document.split()
          if word.lower() not in stoplist]
         for document in documents]

frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1
texts = [[token for token in text if frequency[token] > 1]
         for text in texts]
dictionary = corpora.Dictionary(texts)

# doc2bow counts the number of occurences of each distinct word,
# converts the word to its integer word id and returns the result
# as a sparse vector

corpus = [dictionary.doc2bow(text) for text in texts]
lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)


from werkzeug.wrappers import Request, Response

@Request.application
def application(request):
    text = request.args["text"]
    vec_bow = dictionary.doc2bow(text.lower().split())

    # convert the query to LSI space
    vec_lsi = lsi[vec_bow]
    index = similarities.MatrixSimilarity(lsi[corpus])

    # perform a similarity query against the corpus
    sims = index[vec_lsi]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])

    sim_tweets = []
    for i in range(10):
        tw = tweets[sims[i][0]][1]
        sim_tweets.append({"name":tw["user"]["screen_name"], "username":"@" + tw["user"]["screen_name"], "dateTime":tw["created_at"], "text":tw["text"], "comments":tw["user"]["screen_name"], "retweets":tw["retweet_count"], "likes":tw["user"]["screen_name"], "image":tw["user"]["screen_name"]})
    
    myreviews_seq = tokenizer.texts_to_sequences([text])
    X_myreviews = preprocess_sequences(myreviews_seq, vocab_size, maxlen)
    response = Response(json.JSONEncoder().encode({"tweets":sim_tweets , "score":int(100 * loaded_model.predict(X_myreviews)[0][0])}))
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,PATCH')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    return response

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 4000, application)