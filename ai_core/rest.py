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

vocab_size = 20000
maxlen = 80

def preprocess_sequences(seq, vocab_size, maxlen):
    out = []
    ##############################################################################
    # TODO: Write a function to preprocess sequences:                            #
    #       - all sequences should have the same length - pad them with 0s at    #
    #         the beginning (the extra zeros go in the beginning of the list)    #
    #       - if sequence is too long (above maxlen), then keep only the maxlen  #
    #         words in end of the review(works better than keeping the beginning)#
    #       - remove all words with index >= vocab_size, replace them with 2s.   #
    #         (Words are ordered by frequency, so you are in fact removing less  #
    #         frequent words.)                                                   #
    ##############################################################################
    out = [[word for word in rev if word < vocab_size] for rev in seq]
    out = [([0] * (maxlen - len(rev)) + rev )[:maxlen] for rev in out]
    ##############################################################################
    #                             END OF YOUR CODE                               #
    ##############################################################################
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

##############################################################################
# TODO: Write one positive (> 0.9) and one negative (< 0.1) movie review.    #
#       Try to write it yourself, do not just copy paste reviews from        #
#       somewhere until you find one that works.                             #
##############################################################################
myreviews = [
    "Racism against white people? Noooo, no such thing. Dunno what u talkin' about! Now hold my beer while I spray paint 'fuck whites' on this ad for Mexican food cuz that makes sense.", # fill this with good review
    "It was the worst movie ever seen. It is just waste of time and money. Dont go with anyone if you dont want to torchure them." # fill this with bad review
]
##############################################################################
#                             END OF YOUR CODE                               #
##############################################################################

myreviews_seq = tokenizer.texts_to_sequences(myreviews)
X_myreviews = preprocess_sequences(myreviews_seq, vocab_size, maxlen)
print(loaded_model.predict(X_myreviews)[0][0])