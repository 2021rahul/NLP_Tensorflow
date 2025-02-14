# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 17:27:28 2018

@author: rahul.ghosh
"""

import numpy as np
import collections
import os
import config


class DATA():

    def __init__(self):
        self.batch_size = None
        self.data_len = None
        self.batch_len = None

    def read(self, filename):
        with open(os.path.join(config.DATA_DIR, filename), "r", encoding="utf-8") as f:
            return f.read().replace("\n", "<eos>").split()

    def build_vocab(self, filename):
        data = self.read(filename)
        counter = collections.Counter(data)
        count_pairs = sorted(counter.items(), key=lambda x: (-x[1], x[0]))
        words, _ = list(zip(*count_pairs))
        word_to_id = dict(zip(words, range(len(words))))
        return word_to_id

    def file_to_word_ids(self, filename, word_to_id):
        data = self.read(filename)
        return [word_to_id[word] for word in data if word in word_to_id]


class PTB_DATA(DATA):

    def __init__(self):
        super(PTB_DATA, self).__init__()
        self.data = None
        self.vocabulary = None

    def load_data(self, filename, batch_size):
        word_to_id = self.build_vocab(filename)
        self.reverse_dictionary = dict(zip(word_to_id.values(), word_to_id.keys()))
        self.data = self.file_to_word_ids(filename, word_to_id)
        self.vocabulary = len(word_to_id)
        self.data_len = len(self.data)
        self.batch_len = self.data_len//batch_size

    def generate_batch(self, batch_size, num_steps, batch):
        data = np.reshape(self.data[0: batch_size * self.batch_len], [batch_size, self.batch_len])
        dataX = data[:, (batch):(batch + num_steps)]
        dataY = data[:, (batch + 1):(batch + 1 + num_steps)]
        return dataX, dataY


def DataTests():
    model_config = config.MediumConfig()
    train_data = PTB_DATA()
    train_data.load_data(config.TRAIN_FILENAME, model_config.batch_size)
    total_batch = int((train_data.batch_len - 1)/model_config.num_steps)
    shape = (model_config.batch_size, model_config.num_steps)
    for epoch in range(2):
        for batch in range(total_batch):
            batch_X, batch_Y = train_data.generate_batch(model_config.batch_size, model_config.num_steps, batch)
            print("batch:", batch)
            assert batch_X.shape == shape
            assert batch_Y.shape == shape

#DataTests()
