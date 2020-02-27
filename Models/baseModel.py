
from pymongo import MongoClient
import gridfs
import io

class BaseModel():
    __model = 'undefined'

    def __init__(self):
        super().__init__()


    def loadModel(self, location=''):
        print('loading model' )

    @staticmethod
    def buildModel():
        raise NotImplementedError

    @staticmethod
    def saveToDb(model, connection, meta):
        filename = './tmp_saved_model.h5'
        db = MongoClient(connection)
        fs = gridfs.GridFS(db.TrainedModels)

        model.save(filename)
        
        fileToUpload = io.FileIO(filename, 'r')

        fs.put(fileToUpload, meta=meta)
        fileToUpload.close()
    