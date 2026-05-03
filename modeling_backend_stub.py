
import pandas as pd
from enum import Enum, auto
from http import HTTPStatus
import backend_stub as bs
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
from sklearn.preprocessing import RobustScaler
from sklearn.neighbors import KNeighborsRegressor
import matplotlib.pylab as plt
import seaborn as sns

processed = pd.read_csv('processed.csv', index_col='datetime', parse_dates=['datetime'])

def get_processed_data():

    return processed

def get_training_test_split():

    dataset = get_processed_data()
    ind = dataset.copy()

    dep = ind['aqi']
    ind = ind.drop('aqi', axis=1)

    return train_test_split(ind, dep, test_size=0.3, random_state=37, shuffle=False)

def get_metrics(model, X_train, y_train, y_test, predictions):

    #print(f'Train Accuracy : {model.score(X_train, y_train)*100:.2f}%')
    #print(f'Test  Accuracy : {accuracy_score(y_test, predictions)*100:.2f}%')
    cr = classification_report(y_test, predictions)
    cm = confusion_matrix(y_test, predictions)

    fig, ax = plt.subplots(figsize=(10, 8))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)

    disp.plot(ax=ax, xticks_rotation='vertical')

    return cr, fig

def run_classifier(model, scaler):

    x_train, x_test, y_train, y_test = get_training_test_split()

    scaled = x_test
    if scaler is not None:
        scaled = scaler.transform(x_test)

    predictions = model.predict(scaled)

    # mae = mean_absolute_error(y_test, predictions)
    # r2  = r2_score(y_test, predictions)

    return get_metrics(model, scaled, y_train, y_test, predictions)

def get_linear_classifier():

    model = joblib.load('linear_model.pkl')
    scaler = joblib.load('linear_model_scaler.pkl')

    return run_classifier(model, scaler)

def get_knn_classifier():

    model = joblib.load('knn_model.pkl')
    scaler = joblib.load('knn_model_scaler.pkl')

    return run_classifier(model, scaler)

def get_tree_classifier():

    model = joblib.load('forest_model.pkl')
    return run_classifier(model, None)

class Endpoint(Enum):
    LINEAR = auto()
    KNN = auto()
    TREE = auto()

ENDPOINTS = {
    Endpoint.LINEAR : get_linear_classifier,
    Endpoint.KNN : get_knn_classifier,
    Endpoint.TREE : get_tree_classifier,
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
