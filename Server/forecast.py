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

def mergeForecastWithPrediction(a, b):
    print(b)
    return {
        
        'time':b['time'],
        'solarMW':a[0]
    }

@forecastApi.route('/')
def get_all():
    ## Tempory read in data ##
    url = os.getenv('DATA_SERVICE_URL') 
    uri = '{url}/api/data/forecast'.format(url=url)
    rawData = DataRequest.getData(uri)
    # print(tmpData)
    # data = [DataRequest.getData('{uri}/api/data/'.format(uri=uri))[0]]
    # print(data)
    ## Delete above here once support for   ##
    ## future data is availible             ##

    data = DataTransform.transform(rawData)
    norm_data = DataTransform.normalise(data, norm_stats)
    prediction = model.predict(norm_data).tolist()
    x = list(map(mergeForecastWithPrediction, prediction, rawData))
    print(x)


    return {'prediction':x}
