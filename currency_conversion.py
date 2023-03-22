"""
Excercise # 1 - Retrieving and applying exchange rates on raw data
"""
import pandas as pd
from xml.dom.minidom import parse
from web_downloader import fetch_data_from_url

def get_exchange_rate(source: str, target: str = "EUR") -> pd.DataFrame:
    """

    
    Description
    -----------
    Fetch the exchange rate data from the appropriate URL and convert it to a pandas
    DataFrame, with columns TIME_PERIOD and OBS_VALUE, corresponding to values of
    generic:ObsDimension and generic:ObsValue tags from the XML.

    URL- 
        https://sdw-wsrest.ecb.europa.eu/service/data/EXR/M.GBP.EUR.SP00.A?detail=dataonly

        GBP- Source currency
        EUR- Target currency

    Parameters
    -----------
    source: str
        source currency e.g.- GBP

    target: str (optional, default value is EUR)
        destination currency e.g. - EUR

    Return 
    -----------
    Pandas Daraframe
        Pandas Dataframe (N x 2)

    Test Cases
    -----------
    >>> type(get_exchange_rate("GBP"))
    <class 'pandas.core.frame.DataFrame'>

    >>> get_exchange_rate("GBP").columns[0]
    'TIME_PERIOD'

    >>> get_exchange_rate("GBP").columns[1]
    'OBS_VALUE'

    >>> type(get_exchange_rate("GBP").loc[1].at["OBS_VALUE"])
    <class 'numpy.float64'>

    >>> get_exchange_rate("TUY")
    Traceback (most recent call last):
    requests.exceptions.HTTPError: Data is not available for given input

    """
    url = 'https://sdw-wsrest.ecb.europa.eu/service/data/EXR/M.GBP.EUR.SP00.A?detail=dataonly'
    url = url.replace("GBP.EUR", source+"."+target)
    
    data_frame = fetch_data_from_url(url)
    
    
    return data_frame

def get_raw_data(identifier: str) -> pd.DataFrame:
    """
    
    Description
    -----------
    It will access the REST API of the European Central Bank, using the URL below:
        https://sdw-wsrest.ecb.europa.eu/service/data/BP6/M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N?detail=dataonly
    
    In the URL above, M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N is the data identifier and can be
    replaced with any user-specified identifier.


    Parameters
    -----------
    identifier: str
        it's string parameter to be replaced in the url to get the desired data


    Return 
    -----------

    Pandas Daraframe
        Pandas Dataframe (N x 2)

    Test Cases

    -----------

    >>> type(get_raw_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N"))
    <class 'pandas.core.frame.DataFrame'>

    >>> get_raw_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N").columns[0]
    'TIME_PERIOD'

    >>> get_raw_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N").columns[1]
    'OBS_VALUE'

    >>> get_raw_data("TUY")
    Traceback (most recent call last):
    requests.exceptions.HTTPError: Data is not available for given input
    
    
    """
    url = 'https://sdw-wsrest.ecb.europa.eu/service/data/BP6/M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N?detail=dataonly'
    url = url.replace("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N", identifier)
    data_frame = fetch_data_from_url(url)

    return data_frame

def get_data(identifier: str, target_currency: str = None) -> pd.DataFrame:
    """
    
    Description
    -----------
    It will apply the currency exchange rate on the raw data.
    If the target_currency parameter is None, it will return raw data without any transformaion. 
    Otherwise convert the data from the source currency to the target one, 
    defined by the target_currency parameter

    Parameters
    -----------
    identifier: str
        it's string parameter to be replaced in the url to get the desired data
    
    target_currency: str (optional parameter)
        if present then decide the exchange rate on raw data

    Return 
    -----------

    Pandas Daraframe
        Pandas Dataframe (N x 2)

    Test Cases

    -----------

    
    >>> get_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.GBP._T.T.N", "EUR").columns[1]
    Traceback (most recent call last):
    requests.exceptions.HTTPError: Data is not available for given input

    >>> get_data("TUY")
    Traceback (most recent call last):
    requests.exceptions.HTTPError: Data is not available for given input
    
    """
    if target_currency == None:
        data_frame = get_raw_data(identifier)
        return data_frame
    
    else:
        source_currency = identifier.split(".")[12]
        print(source_currency)
        exchange_rate_data = get_exchange_rate(source_currency, target_currency)
        raw_data = get_raw_data(identifier)

        raw_data['OBS_VALUE'] = exchange_rate_data['OBS_VALUE']*raw_data['OBS_VALUE']
        
        return raw_data


if __name__ == "__main__":

    conversion_data_frame = get_exchange_rate("GBP", "EUR")
    print(conversion_data_frame.head(2))
    raw_data = get_raw_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N")
    print(raw_data.head(2))
    get_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N","EUR")
    print(get_data.head(2))

    