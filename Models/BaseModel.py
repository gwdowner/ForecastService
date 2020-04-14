import gridfs
import pymongo
import io
from Data import DBSingleton as conn
import time
from bson import ObjectId
import tensorflow.keras.models as tf
import os
from dotenv import load_dotenv
load_dotenv()

class BaseModel():
    Model = 'undefined'

    def __init__(self):
        super().__init__()

    @staticmethod
    def loadModel():
        filename = './tmp_saved_model.h5'
        db = conn.getInstance()
        dbName = os.getenv('DB_NAME')
        fs = gridfs.GridFS(db[dbName], collection='fs')
        returnData = {}
        # Get latest model marked as production here
        iterator = db[dbName]["fs.files"].find({"meta.isProduction":{"$eq":True}}).sort("uploadDate", pymongo.DESCENDING)
            
        model_id = iterator.clone().next()
        
        print('selected = ' + str(model_id['_id']))
        if fs.exists(ObjectId(model_id['_id'])):
          
            tmpFile = fs.get(ObjectId(model_id['_id']))
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
        dbName = os.getenv('DB_NAME')
        meta['isProduction'] = True
        db = conn.getInstance()

        fs = gridfs.GridFS(db[dbName])

        model.save(filename)

        fileToUpload = io.FileIO(filename, 'r')

        fs.put(fileToUpload, meta=meta, filename='')
        fileToUpload.close()
