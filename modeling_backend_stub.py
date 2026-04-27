
import pandas as pd
#import numpy as np
#import matplotlib.pylab as plt
#import seaborn as sns
#import io
from enum import Enum, auto
from http import HTTPStatus
#from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import backend_stub as bs
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

aqi_cols = [
    'aqi_Excellent',
    'aqi_Favourable',
    'aqi_Heavy pollution',
    'aqi_Light pollution',
    'aqi_Moderate pollution',
    'aqi_Ultra serious pollution',
]

processed = pd.read_csv('processed.csv', index_col='datetime', parse_dates=['datetime'])

def get_processed_data():

    return processed

def get_training_test_split():

    dataset = get_processed_data()
    ind = dataset.copy()

    dep = ind[aqi_cols]
    ind = ind.drop(aqi_cols, axis=1)

    return train_test_split(ind, dep, test_size=0.3, random_state=37, shuffle=False)

def get_linear_classifier():

    _, x_test, _, y_test = get_training_test_split()

    model = joblib.load('linear_model.pkl')
    scaler = joblib.load('linear_model_scaler.pkl')

    scaled = scaler.transform(x_test)
    predictions = model.predict(scaled)

    mae = mean_absolute_error(y_test, predictions)
    r2  = r2_score(y_test, predictions)

    return { 'MAE': mae, 'R^2': r2 }

def get_knn_classifier():

    model = joblib.load('knn_model.pkl')
    scaler = joblib.load('knn_model_scaler.pkl')

    raise NotImplemented

def get_forest_classifier():

    raise NotImplemented

class Endpoint(Enum):
    LINEAR = auto()
    KNN = auto()
    FOREST = auto()

ENDPOINTS = {
    Endpoint.LINEAR : get_linear_classifier,
    Endpoint.KNN : get_linear_classifier,
    Endpoint.FOREST : get_forest_classifier,
}

class ModelingAPI:

    def request(endpoint, regions=None, date_from=None, date_to=None, components=None, period=None):

        if not isinstance(endpoint, Endpoint):
            return {'status': HTTPStatus.BAD_REQUEST, 'data': 'Endpoint does not exist'}

        if endpoint not in ENDPOINTS:
            return {'status': HTTPStatus.INTERNAL_SERVER_ERROR, 'data': 'Route does not exist'}

        try:
            #if endpoint in [Endpoint.OVERVIEW, Endpoint.SEASONAL]:
            #    return {'status': HTTPStatus.OK, 'data': ENDPOINTS[endpoint]()}

            return {'status': HTTPStatus.OK, 'data': ENDPOINTS[endpoint]()}

        except TypeError as ex:

            return {'status': HTTPStatus.INTERNAL_SERVER_ERROR, 'data': {ex}}
