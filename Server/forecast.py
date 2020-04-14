import os
from flask import Blueprint
from Models import BaseModel
from Data import DBSingleton, DataTransform, DataRequest
import json
import pandas as pd

client = DBSingleton.getInstance()
forecastApi = Blueprint('forecast', __name__, url_prefix='/api/forecast')
modelData = BaseModel.loadModel()
model = modelData['model']
norm_stats = pd.read_json(modelData['norm_data'], orient='split')


def mergeForecastWithPrediction(a, b):

    return {
        'region': b['region'],
        'time': b['time'],
        'solarMW': a[0]
    }


def mapRemoveRegion(a):
    return {
        'time': a['time'],
        'solarMW': a['solarMW']
    }


@forecastApi.route('/')
def get_all():
    baseurl = os.getenv('DATA_SERVICE_URL')
    uri = '{url}/api/data/forecast'.format(url=baseurl)
    rawData = DataRequest.getData(uri)

    data = DataTransform.transform(rawData)

    norm_data = DataTransform.normalise(data, norm_stats)
    prediction = model.predict(norm_data).tolist()

    regions = DataRequest.getData('{url}/api/data/regions'.format(url=baseurl))
    mergedData = list(map(mergeForecastWithPrediction, prediction, rawData))
    rtnRegions = []

    for r in regions:
        tmpFilter = map(mapRemoveRegion, filter(
            lambda x: x['region'] == r['pes_id'], mergedData))
        rtnRegions.append({
            'region': r['pes_id'],
            'forecast': list(tmpFilter)
        })

    return {'prediction': rtnRegions}
