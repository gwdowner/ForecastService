import gridfs
import io
from Data import DBSingleton as conn
import time
from bson import ObjectId
import tensorflow.keras.models as tf

class BaseModel():
    Model = 'undefined'

    def __init__(self):
        super().__init__()

    @staticmethod
    def loadModel(model_id):
        filename = './tmp_saved_model.h5'
        db = conn.getInstance()
        fs = gridfs.GridFS(db.TrainedModels, collection='fs')
        returnData = {}
        if fs.exists(ObjectId(model_id)):
            tmpFile = fs.get(ObjectId(model_id))
            returnData['norm_data'] = tmpFile.meta['norm_data'] 
            outFile = io.FileIO(filename, 'w')
            outFile.write(tmpFile.read())
            returnData['model'] = tf.load_model(filename)
        return returnData
    
    @staticmethod
    def buildModel():
        raise NotImplementedError

    @staticmethod
    def saveToDb(model, connection, meta):
        filename = './tmp_saved_model.h5'

        db = conn.getInstance()

        fs = gridfs.GridFS(db.TrainedModels)

        model.save(filename)

        fileToUpload = io.FileIO(filename, 'r')

        fs.put(fileToUpload, meta=meta, filename='')
        fileToUpload.close()
