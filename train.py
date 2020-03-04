import os
from dotenv import load_dotenv
load_dotenv()
from Data import DataTransform, DataRequest, DBSingleton
import Models.NNModel as NNModel
import tensorflow as tf
from tensorflow import keras
import tensorflow_docs as tfdocs
import tensorflow_docs.plots
import tensorflow_docs.modeling
import threading


# Env variables
EPOCHS = 10
DB_CONNECTION = os.getenv('DB_CONNECTION')
dataURL =  os.getenv('DATA_SERVICE_URL')
print(dataURL)
DBSingleton(DB_CONNECTION)
# get data
dataSource = DataRequest.getData(dataURL)
dataset = DataTransform.transform(dataSource)

# Sample from dataset to create training and verification dataset
train_dataset = dataset.sample(frac=0.8, random_state=0)
test_dataset = dataset.drop(train_dataset.index)

# seperate labels from training data
train_labels = train_dataset.pop('solarMW')
test_labels = test_dataset.pop('solarMW')

# Normalise the data
train_stats = train_dataset.describe()
train_stats = train_stats.transpose()

normed_train_data = DataTransform.normalise(train_dataset, train_stats)
normed_test_data = DataTransform.normalise(test_dataset, train_stats)
 
# Build the model
model = NNModel.buildModel(train_dataset.keys(), hidden_nodes=32)

# Train model
early_stop = keras.callbacks.EarlyStopping(
    monitor='val_loss', patience=50, restore_best_weights=True)

history = model.fit(
    normed_train_data, train_labels,
    epochs=EPOCHS, validation_split=0.2, verbose=0, callbacks=[early_stop, tfdocs.modeling.EpochDots()])

# Test and evaluation
loss, mae, mse = model.evaluate(normed_test_data, test_labels, verbose=2)
print("\nTesting set Mean Abs Error: {:5.2f} MW\n".format(mae))

# Save trained model
print("saving model")

meta = {
    'mae':repr(mae),
    'loss':repr(loss),
    'mse':repr(mse),
    'norm_data':train_stats.to_dict()
}
NNModel.saveToDb(model, DB_CONNECTION, meta)

