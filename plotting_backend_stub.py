
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns
import io
from enum import Enum, auto
from http import HTTPStatus
import backend_stub as bs

def get_histogram(regions=None, date_from=None, date_to=None, components='PM2.5'):

    df = bs.get_data(regions, date_from, date_to, components)

    fig = plt.figure()
    plt.hist(df[components], bins=50)
    plt.xlabel("")
    plt.xticks([])

    return fig

def get_boxplot(regions=None, date_from=None, date_to=None, components='PM2.5'):

    df = bs.get_data(regions, date_from, date_to, components)

    fig = plt.figure()
    ax = df[[components]].boxplot()
    ax.set_xlabel("")
    ax.set_xticklabels([])

    return fig

def get_na_heatmap(regions=None, date_from=None, date_to=None, components='PM2.5'):

    df = bs.get_data(regions, date_from, date_to, components)

    fig = plt.figure()
    sns.heatmap(
        df[[components]].isna().T,
    )
    return fig

def get_valid_data(regions=None, date_from=None, date_to=None, components=['PM2.5', 'PM10']):

    df = bs.get_data(regions, date_from, date_to, components)

    valid = df[components[0]].notna() & df[components[1]].notna()
    x = df[components[0]][valid]
    y = df[components[1]][valid]
    interval = np.linspace(x.min(), x.max())

    return x, y, interval 

def get_scatterplot(regions=None, date_from=None, date_to=None, components=['PM2.5', 'PM10']):

    x, y, interval = get_valid_data(regions, date_from, date_to, components)

    fig = plt.figure()        
    plt.scatter(x, y, s=0.25)

    z = np.polyfit(x, y, deg=1)
    y_hat = np.poly1d(z)
    plt.plot(interval, y_hat(interval), "k--", lw=0.5)

    return fig

def get_correlation_matrix(regions=None, date_from=None, date_to=None, components=None):

    corr = bs.get_data(regions, date_from, date_to, None).corr(numeric_only=True)

    fig = plt.figure()
    sns.heatmap(corr, cmap='coolwarm', annot=True, annot_kws={'fontsize': 'x-small'}, fmt='.2f',)
    return fig

class Endpoint(Enum):
    HIST = auto()
    BOX = auto()
    HEAT_NA = auto()
    SCAT = auto()
    CORR = auto()

ENDPOINTS = {
    Endpoint.HIST : get_histogram,
    Endpoint.BOX : get_boxplot,
    Endpoint.HEAT_NA : get_na_heatmap,
    Endpoint.SCAT : get_scatterplot,
    Endpoint.CORR : get_correlation_matrix,
}

class PlottingAPI:

    @staticmethod
    def request(endpoint, regions=None, date_from=None, date_to=None, components=None):

        if not isinstance(endpoint, Endpoint):
            return {'status': HTTPStatus.BAD_REQUEST, 'data': 'Endpoint does not exist'}

        if endpoint not in ENDPOINTS:
            return {'status': HTTPStatus.INTERNAL_SERVER_ERROR, 'data': 'Route does not exist'}

        try:
            # TODO: Temporary fudge
#            if endpoint in [Endpoint.HIST, Endpoint.BOX, Endpoint.HEAT_NA, Endpoint.SCAT]:
            return {'status': HTTPStatus.OK, 'data': ENDPOINTS[endpoint](regions, date_from, date_to, components)}

#            return {'status': HTTPStatus.OK, 'data': ENDPOINTS[endpoint](regions, date_from, date_to)}
        except TypeError as ex:

            return {'status': HTTPStatus.INTERNAL_SERVER_ERROR, 'data': {ex}}
