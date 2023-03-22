"""
Part 1 - Retrieving exchange rates
"""
import pandas as pd
from xml.dom.minidom import parse
import xml.dom.minidom
import os
import requests
from web_downloader import fetch_data_from_url

def get_exchange_rate(source: str, target: str = "EUR") -> pd.DataFrame:
    """

    Description
    -----------


    Parameters
    -----------

    Return 
    -----------

    Test Cases

    -----------
    
    """
    url = 'https://sdw-wsrest.ecb.europa.eu/service/data/EXR/M.GBP.EUR.SP00.A?detail=dataonly'
    url = url.replace("GBP.EUR", source+"."+target)
    print(url)
    
 
    data_frame = fetch_data_from_url(url)
    
    
    return data_frame

def get_raw_data(identifier: str) -> pd.DataFrame:
    """
    
    Description
    -----------


    Parameters
    -----------

    Return 
    -----------

    Test Cases

    -----------
    
    
    """
    url = 'https://sdw-wsrest.ecb.europa.eu/service/data/BP6/M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N?detail=dataonly'
    url = url.replace("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N", identifier)
    data_frame = fetch_data_from_url(url)

    return data_frame

def get_data(identifier: str, target_currency: str = None) -> pd.DataFrame:
    """
    
    Description
    -----------


    Parameters
    -----------

    Return 
    -----------

    Test Cases

    -----------
    
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
        #print(raw_data.to_string(index=False))
        return raw_data


if __name__ == "__main__":

    conversion_data_frame = get_exchange_rate("GBP", "EUR")
    raw_data = get_raw_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N")
    get_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N","EUR")

    