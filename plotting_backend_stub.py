
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns
import io
from enum import Enum, auto
from http import HTTPStatus
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
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

# Bivariate
def get_scatterplot(regions=None, date_from=None, date_to=None, components=['PM2.5', 'PM10']):

    x, y, interval = get_valid_data(regions, date_from, date_to, components)

    fig = plt.figure()        
    plt.scatter(x, y, s=0.25)

    z = np.polyfit(x, y, deg=1)
    y_hat = np.poly1d(z)
    plt.plot(interval, y_hat(interval), "k--", lw=0.5)

    return fig

# Multivariate
def get_correlation_matrix(regions=None, date_from=None, date_to=None, components=None):

    corr = bs.get_data(regions, date_from, date_to, None).corr(numeric_only=True)

    fig = plt.figure()
    sns.heatmap(corr, cmap='coolwarm', annot=True, annot_kws={'fontsize': 'x-small'}, fmt='.2f',)
    return fig

def get_autocorrelation(regions=None, date_from=None, date_to=None, component=None):

    df = bs.get_data(regions, date_from, date_to, component)

    fig, ax = plt.subplots(1, 2)
    fig.tight_layout()

    plot_acf(df[component].dropna(), lags=75, ax=ax[0])
    plot_pacf(df[component].dropna(), lags=75, ax=ax[1])

    return fig

def get_resampled_data(regions=None, date_from=None, date_to=None, component=None, period=None):

    df = bs.get_data(regions, date_from, date_to, component)

    # TODO: Currently you can pick date and period combinations that
    # just don't make sense, requires some thought and guard code

    #if date_from==None or date_to==None or period==None:
    #    return df, 'Hourly'

    # TODO: This needs to use the enumeration
    if period=='Yearly':
        return df.resample('YE').mean(numeric_only=True), 'Yearly'
    if period=='Quarterly':
        return df.resample('QE').mean(numeric_only=True), 'Quarterly'
    if period=='Monthly':
        return df.resample('ME').mean(numeric_only=True), 'Monthly'
    if period=='Weekly':
        return df.resample('W').mean(numeric_only=True), 'Weekly'
    if period=='Daily':
        return df.resample('D').mean(numeric_only=True), 'Daily'

    return df, 'Hourly'


def get_overview(regions=None, date_from=None, date_to=None, component='PM2.5', period=None):

    fig = plt.figure()
    fig.tight_layout()

    for region in regions:
        df, _ = get_resampled_data([region], date_from, date_to, component, period)

        plt.plot(df.index, df[component])

    plt.title(f'{period} average plot for {component}')
    plt.xticks(rotation=90)
    plt.legend(regions)
    return fig

def get_seasonal(regions=None, date_from=None, date_to=None, component='PM2.5', period=None):

    df, sample_period = get_resampled_data(regions, date_from, date_to, component, period) 

    fig = plt.figure()
    fig.tight_layout()

    plt.plot(df.index, df[component])
    plt.title(f'{sample_period} average plot for {component}')
    plt.minorticks_on()
    plt.tick_params(axis='x', rotation=90)

    return fig

class Endpoint(Enum):
    HIST = auto()
    BOX = auto()
    HEAT_NA = auto()
    SCAT = auto()
    CORR = auto()
    AUTO = auto()
    OVERVIEW = auto()
    SEASONAL = auto()


ENDPOINTS = {
    Endpoint.HIST : get_histogram,
    Endpoint.BOX : get_boxplot,
    Endpoint.HEAT_NA : get_na_heatmap,
    Endpoint.SCAT : get_scatterplot,
    Endpoint.CORR : get_correlation_matrix,
    Endpoint.AUTO : get_autocorrelation,
    Endpoint.OVERVIEW : get_overview,
    Endpoint.SEASONAL : get_seasonal,
}

class PlottingAPI:

    @staticmethod
    def request(endpoint, regions=None, date_from=None, date_to=None, components=None, period=None):

        if not isinstance(endpoint, Endpoint):
            return {'status': HTTPStatus.BAD_REQUEST, 'data': 'Endpoint does not exist'}

        if endpoint not in ENDPOINTS:
            return {'status': HTTPStatus.INTERNAL_SERVER_ERROR, 'data': 'Route does not exist'}

        try:
            if endpoint in [Endpoint.OVERVIEW, Endpoint.SEASONAL]:
                return {'status': HTTPStatus.OK, 'data': ENDPOINTS[endpoint](regions, date_from, date_to, components, period)}

            return {'status': HTTPStatus.OK, 'data': ENDPOINTS[endpoint](regions, date_from, date_to, components)}

        except TypeError as ex:

            return {'status': HTTPStatus.INTERNAL_SERVER_ERROR, 'data': {ex}}
