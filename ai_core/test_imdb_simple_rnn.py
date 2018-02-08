from keras.models import Model
from keras.layers import Input, Dense, Embedding, SimpleRNN, LSTM, GRU
from keras.preprocessing.text import text_to_word_sequence
from keras.datasets import imdb
import numpy as np
import csv
import numpy as np
import csv
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
import random
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from gensim.models import Word2Vec

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.normalization import BatchNormalization
from keras.layers import Merge
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, CSVLogger, EarlyStopping
from keras.optimizers import RMSprop, Adam, SGD, Nadam
from keras.layers.advanced_activations import *
from keras.layers import Convolution1D, MaxPooling1D, AtrousConvolution1D
from keras.layers.recurrent import LSTM, GRU
from keras import regularizers

import theano
theano.config.compute_test_value = "ignore"

len_voc = 0

class PreProcessing():
	def __init__(self, stemming=True, vector_size=100):
		self.__data = None
		self.__stemming = stemming
		self.__vector_size = vector_size
		
	def stemming(self):
		porter_stemmer = PorterStemmer()
		self.__data = [[[ porter_stemmer.stem(word) for word in news] for news in entry] for entry in self.__data]
		
	def word_fill(self):
		avg_number_of_words = int(np.mean([len(news) for row in self.__data for news in row]))
		self.__data = [[ (news + [""] * avg_number_of_words)[:avg_number_of_words] for news in row] for row in self.__data]
		
	def vectorize(self):
		w2vector_data = []
		for row in self.__data:
			w2vector_data.append([word for news in row for word in news])
		model = Word2Vec(w2vector_data, size=self.__vector_size, window=5, min_count=1, workers=4)
		global len_voc
		len_voc = len(model.wv.vocab)
		print(len_voc)
		self.__data = [[np.mean(model[word],axis=0) for word in row] for row in self.__data]
		
	def run(self):
		if self.__stemming:
			self.stemming()
		self.word_fill()
		self.vectorize()
			
	def get_data(self):
		return self.__data
	
	def set_data(self, data):
		self.__data = data

data = []
labels = []

# Read CSV to load price information
with open('data/sport.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        data.append(row[4])
        labels.append(row[3])

preprocessing = PreProcessing(stemming=True, vector_size=10)
preprocessing.set_data(data)
preprocessing.run()
data = preprocessing.get_data()


split = int(len(data)*0.6)

data_train = np.array(data[0:split])
data_test = np.array(data[split:])

label_train = np.array(labels[0:split])
label_test = np.array(labels[split:])

print(data_train[0])

rnn_model = Sequential()
rnn_model.add(LSTM(input_shape = (len_voc, 10,), output_dim=len_voc, return_sequences=False, recurrent_dropout=0.75))    
rnn_model.add(Dense(16))
rnn_model.add(BatchNormalization())
rnn_model.add(LeakyReLU())

rnn_model.add(Dense(1))
rnn_model.add(Activation('softmax'))

rnn_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
#rnn_model.summary()

# Training the simple RNN, should get accuracy above 50% (maybe even 60%)
# you can change nr of epochs to train longer, if you can afford spending more time
history = rnn_model.fit(data_train, label_train, batch_size=32, epochs=5, validation_data=(data_test, label_test))

myreviews = [
    "It was the best movie ever seen, extra ordinary characters. Scenario was the best comedy scenario ever. It totally deserves oscars.", # fill this with good review
    "It was the worst movie ever seen. It is just waste of time and money. Dont go with anyone if you dont want to torchure them." # fill this with bad review
]

rnn_model.predict(X_myreviews)