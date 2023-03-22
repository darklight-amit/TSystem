import pandas as pd
from xml.dom.minidom import parse
import xml.dom.minidom
import os
import requests
from requests import HTTPError

def fetch_data_from_url(url: str) -> pd.DataFrame:
    """
    Description
    -----------
    
    This function takes web url as an input and if data is available then
    return Pandas dataframe with two columns mapped with the xml output of url.
    
    Column1 - generic:ObsDimension
    Column2 - generic:ObsValue

    This is designed to parse only specific type xml response which should have generic:Obs
    tag in the API response for all other URL it will not return anything and will raise appropriate 
    exception.

    Parameters
    -----------
    
    url : String
        web url from where data needs to be requested 

    Returns
    ----------
    Dataframe 
        Pandas Dataframe (N x 2)

    Test Cases 
    ----------

    >>> type(fetch_data_from_url("https://sdw-wsrest.ecb.europa.eu/service/data/EXR/M.GBP.EUR.SP00.A?detail=dataonly"))
    <class 'pandas.core.frame.DataFrame'>

    >>> fetch_data_from_url("www")
    Traceback (most recent call last):
    requests.exceptions.HTTPError: Not a valid URL

    >>> fetch_data_from_url("https://sdw-wsrest.ecb.europa.eu/service/data1/EXR/M.GBP.EUR.SP00.A?detail=dataonly")
    Traceback (most recent call last):
    requests.exceptions.HTTPError: Data is not available for given input

    """
    try:
        xml_response = requests.get(url)
    except:
        raise HTTPError("Not a valid URL")

       
    if xml_response.status_code != 200:
        raise requests.HTTPError("Data is not available for given input")
    
    with open("input_file.xml", "wb") as f:
        f.write(xml_response.content)
    try:
        DOMTree = xml.dom.minidom.parse("input_file.xml")
    except:
        raise NotImplementedError("Parsing can't be done for this URL")
    
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
    

    os.remove("input_file.xml")

    return data_frame


if __name__ == "__main__":
    fetch_data_from_url("http://www.google.com")