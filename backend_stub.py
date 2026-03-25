
import pandas as pd

original = pd.read_csv('original_data.csv')
processed = pd.read_csv('processed.csv')

def get_data(regions=None, date_from=None, date_to=None):

    if (regions is None or len(regions)==0):
        return original

    result = []
    tmp = original.groupby('station')
    for region in regions:
        result.append(tmp.get_group(region))
    result = pd.concat(result)

    if date_from is not None:
        result = result[pd.to_datetime(result['datetime']) >= pd.to_datetime(date_from)]

    if date_to is not None:
        result = result[pd.to_datetime(result['datetime']) <= pd.to_datetime(date_to)]

    return result

def get_region_names():
    return original['station'].unique()

def get_component_names():
    return original.columns

def get_dataset_shape(regions=None, date_from=None, date_to=None):
    return get_data(regions, date_from, date_to).shape

def get_dataset_info(regions=None, date_from=None, date_to=None):
    return get_data(regions, date_from, date_to).info()

def get_dataset_description(regions=None, date_from=None, date_to=None):
    return get_data(regions, date_from, date_to).describe()
