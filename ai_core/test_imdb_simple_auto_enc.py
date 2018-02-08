from keras.models import Model
from keras.layers import Input, Dense, Embedding, SimpleRNN, LSTM, GRU
from keras.preprocessing.text import text_to_word_sequence
from keras.datasets import imdb
import numpy as np

(X_train_seq, y_train), (X_test_seq, y_test) = imdb.load_data()

word2num = imdb.get_word_index()
num2word = dict(dict (zip(word2num.values(),word2num.keys())))

# function to decode reviews
def nums2sentence(nums):
    return " ".join(["UNK" if i == 2 else num2word[i-3] for i in nums[1:]]) 

def preprocess_sequences(seq, vocab_size, maxlen):
    out = [[word for word in rev if word < vocab_size] for rev in seq]
    out = [([0] * (maxlen - len(rev)) + rev )[:maxlen] for rev in out]
    return np.array(out)

vocab_size = 20000
maxlen = 80

X_train = preprocess_sequences(X_train_seq, vocab_size, maxlen)
X_test = preprocess_sequences(X_test_seq, vocab_size, maxlen)

#Definign a simple RNN 
embed_size = 128
rnn_size = 128

x = Input(shape=(None,), dtype='int32')
e = Embedding(vocab_size, embed_size, mask_zero=True)(x)
r = SimpleRNN(rnn_size, return_sequences=False)(e)
p = Dense(1, activation='sigmoid')(r)

rnn_model = Model(x, p)
rnn_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
#rnn_model.summary()

# Training the simple RNN, should get accuracy above 50% (maybe even 60%)
# you can change nr of epochs to train longer, if you can afford spending more time
history = rnn_model.fit(X_train, y_train, batch_size=32, epochs=5, validation_data=(X_test, y_test))

def words2sequences(words):
    return [word2num[w]+3 if w in word2num else 2 for w in text_to_word_sequence(words)]

def sentences2sequences(sentences):
    return [[1] + words2sequences(s) for s in sentences]

myreviews = [
    "It was the best movie ever seen, extra ordinary characters. Scenario was the best comedy scenario ever. It totally deserves oscars.", # fill this with good review
    "It was the worst movie ever seen. It is just waste of time and money. Dont go with anyone if you dont want to torchure them." # fill this with bad review
]

myreviews_seq = sentences2sequences(myreviews)
X_myreviews = preprocess_sequences(myreviews_seq, vocab_size, maxlen)
model.predict(X_myreviews)