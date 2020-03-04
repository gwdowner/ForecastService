import os
from flask import Blueprint
from Models import BaseModel
from Data import DBSingleton, DataTransform, DataRequest
import json


client = DBSingleton.getInstance()
forecastApi = Blueprint('forecast', __name__, url_prefix='/api/forecast/')
modelData = BaseModel.loadModel('5e5e96dbff5c4a28f4a6367b')
model = modelData['model']
norm_stats = modelData['norm_data']

@forecastApi.route('/')
def get_all():
    ## Tempory read in data ##
    uri = os.getenv('DATA_SERVICE_URL') 
    data = [DataRequest.getData(uri)[0]]
    ## Delete above here once support for   ##
    ## future data is availible             ##

    data = DataTransform.transform(data)
    data.pop('solarMW')
    norm_data = DataTransform.normalise(data, norm_stats)
    prediction = model.predict(norm_data).tolist()
    
    return {'prediction':prediction[0]}
