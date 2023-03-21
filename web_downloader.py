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
        raise ValueError("Data is not available for given input")
    
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
    # print(data_frame.to_string(index=False))

    os.remove("input_file.xml")

    return data_frame