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


# define documents
data = []

# Read
import json

with open('truncated.json') as json_file:  
    f = json.load(json_file)
    for row in f:
        data.append([row["text"], int(int(row["user"]["friends_count"]) + int(row["user"]["followers_count"]) + int(row["user"]["favourites_count"]) + int(row["user"]["statuses_count"]) + int(row["user"]["listed_count"]) + int(row["retweet_count"]) / 6)])		

data = np.array(data)
median = statistics.median(data[:,1].astype(np.int64))
i = 0
for row in data:
    if int(row[1]) > median:
        data[i][1] = 1
    else:
        data[i][1] = 0
    i = i + 1

# define documents
split = int(len(data)*0.8)

docs = np.array(data[:,0][0:split])
docs2 = np.array(data[:,0][split:])

y_train = np.array(data[:,1][0:split])
y_test = np.array(data[:,1][split:])
# prepare tokenizer
t = Tokenizer()
t.fit_on_texts(data[:,0])
vocab_size = 20000
# integer encode the documents
encoded_docs = t.texts_to_sequences(docs)
encoded_docs2 = t.texts_to_sequences(docs2)

import pickle

# saving
with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(t, handle, protocol=pickle.HIGHEST_PROTOCOL)

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

maxlen = 20



X_train = np.array(preprocess_sequences(encoded_docs, vocab_size, maxlen))
X_test = np.array(preprocess_sequences(encoded_docs2, vocab_size, maxlen))

#Definign a simple RNN 
embed_size = 100
o_size = 128

x = Input(shape=(None,), dtype='int32')
e = Embedding(vocab_size, embed_size, mask_zero=True)(x)
r = LSTM(o_size, return_sequences=False)(e)
p = Dense(1, activation='sigmoid')(r)

ltsm_model = Model(x, p)
ltsm_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
ltsm_model.summary()

# Training the simple RNN, should get accuracy above 50% (maybe even 60%)
# you can change nr of epochs to train longer, if you can afford spending more time
history = ltsm_model.fit(X_train, y_train, batch_size=128, epochs=5, validation_data=(X_test, y_test))


# serialize model to JSON
model_json = ltsm_model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
ltsm_model.save_weights("model.h5")
print("Saved model to disk")