"""
TITLE:          GameAgent.py (Snake)
AUTHOR:         Aakash Sudhakar

SUMMARY:        Support Python file holding the reinforcement learning algorithm for 
                the deep learning reinforcement simulation of Snake.
NOTE:           Uses the Deep-Q Networks Reinforcement model.
"""

from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers.core import Dense, Dropout
from random import sample
import numpy as np
import pandas as pd
from operator import add

class GameAgent(object):
    """ Object structure storing the Deep Reinforcement Learning Agent. """
    def __init__(self):
        self.reward = 0
        self.gamma = 0.9
        self.df = pd.DataFrame()
        self.short_memory = np.array([])
        self.agent_target = 1
        self.agent_prediction = 0
        self.learning_rate = 0.0005
        self.model = self.produce_network_architecture()
        self.epsilon = 0
        self.actual = list()
        self.memory = list()

    def get_game_state(self):
        pass

    def get_game_reward(self):
        pass

    def produce_network_architecture(self):
        """ Method to create neural network architecture using optimized Keras models. """
        model = Sequential()
        model.add(Dense(120, activation="relu", input_shape=(11,)))
        model.add(Dropout(0.15))
        model.add(Dense(120, activation="relu"))
        model.add(Dropout(0.15))
        model.add(Dense(120, activation="relu"))
        model.add(Dropout(0.15))
        model.add(Dense(3, activation="softmax"))
        optimizer = Adam(self.learning_rate)
        model.compile(loss="mse", optimizer=optimizer)
        return model

    def save_state_to_memory(self, current_state, current_action, current_reward, next_state, stop):
        """ Method to save current detailed state to object's memory. """
        self.memory.append((current_state, current_action, current_reward, next_state, stop))

    def short_term_memory_trainer(self, current_state, current_action, current_reward, next_state, stop):
        """ Method to train short-term memory bank using detailed saved state info. """
        target_ = current_reward
        if not stop:
            target_ = current_reward + (self.gamma * np.amax(self.model.predict(next_state.reshape((1, 11)))[0]))
        target_final = self.model.predict(current_state.reshape((1, 11)))
        target_final[0][np.argmax(current_action)] = target_
        self.model.fit(current_state.reshape((1, 11)), target_final, epochs=1, verbose=0)

    def replay_from_memory(self, memory_bank):
        """ Method to retrieve state details from object's memory bank. """
        if len(memory_bank) > 1000:
            batch = sample(memory_bank, 1000)
        else:
            batch = memory_bank
        for current_state, current_action, current_reward, next_state, stop in batch:
            target_ = current_reward
            if not stop:
                target_ = current_reward + (self.gamma * np.amax(self.model.predict(np.array([next_state]))[0]))
            target_final = self.model.predict(np.array([current_state]))
            target_final[0][np.argmax(current_action)] = target_
            self.model.fit(np.array([current_state]), target_final, epochs=1, verbose=0)
