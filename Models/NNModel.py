from .BaseModel import BaseModel
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
import tensorflow_docs.plots as plots
import pandas as pd

class NNModel(BaseModel):
    def __init__(self):
        super().__init__()

    @staticmethod
    def buildModel(keys, hidden_nodes=16, hidden_layers=3, outputNodes=1):
        modelOperations = [
            layers.Dense(hidden_nodes, activation='relu', input_shape=[
                len(keys)])
        ]

        for i in range(hidden_layers):
            modelOperations.append(layers.Dense(
                hidden_nodes, activation='relu'))

        modelOperations.append(layers.Dense(outputNodes))

        model = keras.Sequential(modelOperations)

        optimizer = tf.keras.optimizers.RMSprop(0.001)

        model.compile(loss='mse',
                      optimizer=optimizer,
                      metrics=['mae', 'mse'])
        return model

    @staticmethod
    def showTrainingHistory(history):
        hist = pd.DataFrame(history.history)
        hist['epoch'] = history.epoch
        plt.figure()
        plotter = plots.HistoryPlotter(smoothing_std=1)
        plotter.plot({'Basic': history}, metric="mae")
        plt.ylabel('MAE [MW]')
        plt.draw()
        plt.show(block=False)
       