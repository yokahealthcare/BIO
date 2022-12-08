# DEEP LEARNING LIBRARY
import keras
from keras.models import Sequential
from keras.layers import Dense 
from keras.optimizers import Adam

import numpy as np

class Brain:

    def __init__(self, numInputs, numOutputs, lr=0.1):
        self.numInputs = numInputs
        self.numOutputs = numOutputs
        self.lr = lr

        # Creating Neural Network
        self.model = Sequential()
        self.model.add(Dense(units=32, activation='relu', input_shape=(self.numInputs, )))
        self.model.add(Dense(units=256, activation='relu'))
        self.model.add(Dense(units=self.numOutputs))

        self.model.compile(optimizer=Adam(lr=self.lr), loss='mean_squared_error')



















