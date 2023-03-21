"""
Part 1 - Retrieving exchange rates
"""
import pandas as pd
from xml.dom.minidom import parse
import xml.dom.minidom
import os
import requests



def fetch_data_from_url(url):
    """
    
    """

    xml_response = requests.get(url)
       
    if xml_response.status_code != 200:
        raise Exception("Data is not available for given input")
    
    with open("input_file.xml", "wb") as f:
        f.write(xml_response.content)
    
    DOMTree = xml.dom.minidom.parse("input_file.xml")
    collection = DOMTree.documentElement
    parent_tag = collection.getElementsByTagName("generic:Obs")

    conversion_dict = {'TIME_PERIOD':[], 'OBS_VALUE':[]}
    for element in parent_tag:
        obs_dimention = element.getElementsByTagName("generic:ObsDimension")
        obs_value = element.getElementsByTagName("generic:ObsValue")
        for value in obs_dimention:
            conversion_dict['TIME_PERIOD'].append(value.getAttribute("value"))
            
        for value in obs_value:
            conversion_dict['OBS_VALUE'].append(float(value.getAttribute("value")))
            
        
    data_frame = pd.DataFrame.from_dict(conversion_dict)
    print(data_frame.to_string(index=False))

    os.remove("input_file.xml")

    return data_frame

def get_exchange_rate(source: str, target: str = "EUR") -> pd.DataFrame:
    """
    
    """
    url = 'https://sdw-wsrest.ecb.europa.eu/service/data/EXR/M.GBP.EUR.SP00.A?detail=dataonly'
    url = url.replace("GBP.EUR", source+"."+target)
    print(url)
    
 
    data_frame = fetch_data_from_url(url)
    
    
    return data_frame

def get_raw_data(identifier: str) -> pd.DataFrame:
    """
    
    """
    url = 'https://sdw-wsrest.ecb.europa.eu/service/data/BP6/M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N?detail=dataonly'
    url = url.replace("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N", identifier)
    data_frame = fetch_data_from_url(url)

    return data_frame

def get_data(identifier: str, target_currency: str = None) -> pd.DataFrame:
    """
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
        print(raw_data.to_string(index=False))
        return raw_data


if __name__ == "__main__":

    conversion_data_frame = get_exchange_rate("GBP", "EUR")
    raw_data = get_raw_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N")
    get_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N","EUR")

    