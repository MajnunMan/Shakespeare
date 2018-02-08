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
# define documents
data = []
labels = []

# Read CSV to load price information
with open('data/sport.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    i = 0
    tmp = [row for row in reader]
    max = len(tmp)
    for row in tmp:
        data.append(row[4])
        i = i + 1
        if i%2 == 1:
            labels.append(0)
        else:
            labels.append(1)
# define documents
split = int(len(data)*0.8)

docs = np.array(data[0:split])
docs2 = np.array(data[split:])

y_train = np.array(labels[0:split])
y_test = np.array(labels[split:])
# prepare tokenizer
t = Tokenizer()
t.fit_on_texts(data)
vocab_size = 20000
# integer encode the documents
encoded_docs = t.texts_to_sequences(docs)
encoded_docs2 = t.texts_to_sequences(docs2)

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

vocab_size = 20000
maxlen = 80



X_train = np.array(preprocess_sequences(encoded_docs, vocab_size, maxlen))
X_test = np.array(preprocess_sequences(encoded_docs2, vocab_size, maxlen))

#Definign a simple RNN 
embed_size = 123
o_size = 123

x = Input(shape=(None,), dtype='int32')
e = Embedding(vocab_size, embed_size, mask_zero=True)(x)
r = LSTM(o_size, return_sequences=False)(e)
p = Dense(1, activation='sigmoid')(r)

ltsm_model = Model(x, p)
ltsm_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
ltsm_model.summary()

# Training the simple RNN, should get accuracy above 50% (maybe even 60%)
# you can change nr of epochs to train longer, if you can afford spending more time
history = ltsm_model.fit(X_train, y_train, batch_size=32, epochs=5, validation_data=(X_test, y_test))

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
    "Real men don't kill harmless & defenceless animals for 'sport'. RT if you agree #stoptrophyhunting", # fill this with good review
    "It was the worst movie ever seen. It is just waste of time and money. Dont go with anyone if you dont want to torchure them." # fill this with bad review
]
##############################################################################
#                             END OF YOUR CODE                               #
##############################################################################

myreviews_seq = t.texts_to_sequences(myreviews)
X_myreviews = preprocess_sequences(myreviews_seq, vocab_size, maxlen)
print(ltsm_model.predict(X_myreviews))