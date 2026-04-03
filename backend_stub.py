
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns
import io
from enum import Enum, auto
from http import HTTPStatus

original = pd.read_csv('original_data.csv', index_col='datetime', parse_dates=['datetime'])
#processed = pd.read_csv('processed.csv')

def get_data(regions=None, date_from=None, date_to=None, components=None):

    if (regions is None or len(regions)==0) and components is None:
        return original

    result = []
    tmp = original.groupby('station')
    #tmp = processed.groupby('station')

    for region in regions:
        result.append(tmp.get_group(region))
    result = pd.concat(result)

    if date_from is not None:
        result = result[result.index >= pd.to_datetime(date_from)]

    if date_to is not None:
        result = result[result.index <= pd.to_datetime(date_to)]

    if components is not None:
        cols = ['No', 'station'] + components
        result = result[cols]

    return result

def get_region_names(regions=None, date_from=None, date_to=None):
    return original['station'].unique()

def get_component_names(regions=None, date_from=None, date_to=None):
    return original.columns

def get_dataset_shape(regions=None, date_from=None, date_to=None):
    return get_data(regions, date_from, date_to).shape

def get_dataset_info(regions=None, date_from=None, date_to=None):
    df = get_data(regions, date_from, date_to)
    result = io.StringIO()
    df.info(buf=result)
    return result.getvalue()

def get_dataset_description(regions=None, date_from=None, date_to=None):
    return get_data(regions, date_from, date_to).describe()

def get_dataset_nans(regions=None, date_from=None, date_to=None):

    data = get_data(regions, date_from, date_to)
    nans = data.isna().sum()
    row_total = len(data)
    nan_tab = pd.concat([nans, (nans/row_total)*100], axis=1)
    nan_tab.rename(columns={0: 'Missing Values', 1: '% of Total Values'}, inplace=True)
    nan_tab.sort_values('% of Total Values', ascending=False, inplace=True)
    return nan_tab.style.background_gradient(cmap='Greens')

import matplotlib.pyplot as plt

def get_histogram(regions=None, date_from=None, date_to=None, components='PM2.5'):

    df = get_data(regions, date_from, date_to, components)

    fig = plt.figure()
    plt.hist(df[components], bins=50)
    plt.xlabel("")
    plt.xticks([])

    return fig

def get_boxplot(regions=None, date_from=None, date_to=None, components='PM2.5'):

    df = get_data(regions, date_from, date_to, components)

    fig = plt.figure()
    ax = df[[components]].boxplot()
    ax.set_xlabel("")
    ax.set_xticklabels([])

    return fig

def get_na_heatmap(regions=None, date_from=None, date_to=None, components='PM2.5'):

    df = get_data(regions, date_from, date_to, components)

    fig = plt.figure()
    sns.heatmap(
        df[[components]].isna().T,
    )
    return fig

def get_valid_data(regions=None, date_from=None, date_to=None, components=['PM2.5', 'PM10']):

    df = get_data(regions, date_from, date_to, components)

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


class Endpoint(Enum):
    DATA = auto()
    REGIONS = auto()
    COLUMNS = auto()
    SHAPE = auto()
    INFO = auto()
    DESC = auto()
    NANS = auto()
    HIST = auto()
    BOX = auto()
    HEAT_NA = auto()
    SCAT = auto()

ENDPOINTS = {
    Endpoint.DATA : get_data,
    Endpoint.REGIONS : get_region_names,
    Endpoint.COLUMNS : get_component_names,
    Endpoint.SHAPE : get_dataset_shape,
    Endpoint.INFO : get_dataset_info,
    Endpoint.DESC : get_dataset_description,
    Endpoint.NANS : get_dataset_nans,
    Endpoint.HIST : get_histogram,
    Endpoint.BOX : get_boxplot,
    Endpoint.HEAT_NA : get_na_heatmap,
    Endpoint.SCAT : get_scatterplot,
}

class DatasetAPI:

    @staticmethod
    def request(endpoint, regions=None, date_from=None, date_to=None, components=None):

        if not isinstance(endpoint, Endpoint):
            return {'status': HTTPStatus.BAD_REQUEST, 'data': 'Endpoint does not exist'}

        if endpoint not in ENDPOINTS:
            return {'status': HTTPStatus.INTERNAL_SERVER_ERROR, 'data': 'Route does not exist'}

        try:
            # TODO: Temporary fudge
            if endpoint in [Endpoint.HIST, Endpoint.BOX, Endpoint.HEAT_NA, Endpoint.SCAT]:
                return {'status': HTTPStatus.OK, 'data': ENDPOINTS[endpoint](regions, date_from, date_to, components)}

            return {'status': HTTPStatus.OK, 'data': ENDPOINTS[endpoint](regions, date_from, date_to)}
        except TypeError as ex:

            return {'status': HTTPStatus.INTERNAL_SERVER_ERROR, 'data': f'{ex}'}
