import pandas as pd
from xml.dom.minidom import parse
import xml.dom.minidom
import os
import requests
from typing import Dict

from currency_conversion import fetch_data_from_url

def get_transactions(identifier: str) -> pd.DataFrame:
    """
    
    """

    url = "https://sdw-wsrest.ecb.europa.eu/service/data/BSI/Q.HR.N.A.A20.A.1.AT.2000.Z01.E?detail=dataonly"
    ulr = url.replace("Q.DE.N.A.A20.A.1.AT.2000.Z01.E", identifier)
    transaction_data = fetch_data_from_url(url)
    transaction_data.insert(0, column= 'IDENTIFIER' , value = [identifier]*len(transaction_data))
    return transaction_data


def get_symmetric_identifier(identifier: str, swap_components: Dict[int,int]) -> str:
    """
    """
    list_str = identifier.split(".")
    
    for key, value in swap_components.items():
        list_str[key], list_str[value] = list_str[value], list_str[key]
    
    return ".".join(list_str)

def get_asymmetries(identifier: str, swap_components: Dict[int, int]) -> pd.DataFrame:
    """
    """
    symmetric_identifier = get_symmetric_identifier(identifier, swap_components)
    provided_df  = get_transactions(identifier)
    symmetric_df = get_transactions(symmetric_identifier)
    final_df = pd.DataFrame()
    final_df['TIME_PERIOD'] = symmetric_df['TIME_PERIOD']
    final_df['PROVIDED_ID'] = [identifier]*len(symmetric_df) 
    final_df["SYMMETRIC_ID"] = [symmetric_identifier]* len(symmetric_df)
    final_df["DELTA"] = provided_df['OBS_VALUE'] - symmetric_df['OBS_VALUE']

    return final_df

if __name__ == "__main__":
    transaction_data = get_transactions("Q.DE.N.A.A20.A.1.AT.2000.Z01.E")
    print(transaction_data.to_string(index = False))
    symmetric_identifier = get_symmetric_identifier("Q.HR.N.A.A20.A.1.AT.2000.Z01.E", {1: 7, 2: 3})
    print(symmetric_identifier)
    delta = get_asymmetries("Q.HR.N.A.A20.A.1.AT.2000.Z01.E", {1: 7})
    print(delta)



