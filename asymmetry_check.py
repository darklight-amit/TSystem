"""
Excercise # 2 - Asymmetry Check

It will check the recocilation status for the transaction happened between two countries
"""

import pandas as pd
from xml.dom.minidom import parse
from typing import Dict

from currency_conversion import fetch_data_from_url

def get_transactions(identifier: str) -> pd.DataFrame:
    """
    
    Description
    -----------
    It fetch the transaction data from the appropriate URL and convert it to a pandas DataFrame,
    with columns IDENTIFIER, TIME_PERIOD and OBS_VALUE, corresponding to values of the identifier
    parameter, generic:ObsDimension tag and generic:ObsValue tag from the XML.

    Parameters
    -----------
    identifier: str
        it's string parameter to be replaced in the url to get the desired data

    Return 
    -----------

    Pandas Daraframe
        Pandas Dataframe (N x 3)

    Test Cases

    -----------

    >>> type(get_transactions("Q.DE.N.A.A20.A.1.AT.2000.Z01.E"))
    <class 'pandas.core.frame.DataFrame'>

    >>> get_transactions("Q.DE.N.A.A20.A.1.AT.2000.Z01.E").columns[0]
    'IDENTIFIER'

    >>> get_transactions("Q.DE.N.A.A20.A.1.AT.2000.Z01.E").columns[1]
    'TIME_PERIOD'

    >>> get_transactions("Q.DE.N.A.A20.A.1.AT.2000.Z01.E").columns[2]
    'OBS_VALUE'

    >>> type(get_transactions("Q.DE.N.A.A20.A.1.AT.2000.Z01.E").loc[2].at["OBS_VALUE"])
    <class 'numpy.float64'>

    >>> get_transactions("TUY")
    Traceback (most recent call last):
    requests.exceptions.HTTPError: Data is not available for given input
    
    """

    url = "https://sdw-wsrest.ecb.europa.eu/service/data/BSI/Q.HR.N.A.A20.A.1.AT.2000.Z01.E?detail=dataonly"
    url = url.replace("Q.HR.N.A.A20.A.1.AT.2000.Z01.E", identifier)
    transaction_data = fetch_data_from_url(url)
    transaction_data.insert(0, column= 'IDENTIFIER' , value = [identifier]*len(transaction_data))
    return transaction_data


def get_symmetric_identifier(identifier: str, swap_components: Dict[int,int]) -> str:
    """

    
    Description
    -----------
    The function will return a new identifier, obtained from the provided one, by swapping components, as
    indicated by the key-value pairs in the provided dictionary. The pairs represent 0-based indices of
    components to swap.

    Parameters
    -----------
    identifier: str
        it's string parameter to be replaced in the url to get the desired data
    
    swap_components: Dict[int,int]
        keys and values both are index in the identifer and will get swapped 
    

    Return 
    -----------

    str

    Test Cases

    -----------

    >>> get_symmetric_identifier("Q.HR.N.A.A20.A.1.AT.2000.Z01.E", {1: 7, 2: 3})
    'Q.AT.A.N.A20.A.1.HR.2000.Z01.E'
    
    """
    list_str = identifier.split(".")
    
    for key, value in swap_components.items():
        list_str[key], list_str[value] = list_str[value], list_str[key]
    
    return ".".join(list_str)

def get_asymmetries(identifier: str, swap_components: Dict[int, int]) -> pd.DataFrame:
    """
    
    Description
    -----------
    It will first get the symmetric identifier and then fetch the data for both identifiers
    and finally calculate the Delta.

    Parameters
    -----------
    identifier: str
        it's string parameter to be replaced in the url to get the desired data
    
    swap_components: Dict[int,int]
        keys and values both are index in the identifer and will get swapped 
    

    Return 
    -----------

    Dataframe 
        Pandas Dataframe (N x 4)

    Test Cases

    -----------

    >>> type(get_asymmetries("Q.HR.N.A.A20.A.1.AT.2000.Z01.E", {1: 7}))
    <class 'pandas.core.frame.DataFrame'>

    >>> get_asymmetries("Q.HR.N.A.A20.A.1.AT.2000.Z01.E", {1: 7}).columns[0]
    'TIME_PERIOD'

    >>> get_asymmetries("Q.HR.N.A.A20.A.1.AT.2000.Z01.E", {1: 7}).columns[1]
    'PROVIDED_ID'

    >>> get_asymmetries("Q.HR.N.A.A20.A.1.AT.2000.Z01.E", {1: 7}).columns[2]
    'SYMMETRIC_ID'

    >>> get_asymmetries("Q.HR.N.A.A20.A.1.AT.2000.Z01.E", {1: 7}).columns[3]
    'DELTA'

    
    >>> get_asymmetries("Q.HR.N.A.A20.A.1.AT.2000.Z01.E", {1: 2})
    Traceback (most recent call last):
    requests.exceptions.HTTPError: Data is not available for given input
    
    """
    symmetric_identifier = get_symmetric_identifier(identifier, swap_components)
    provided_df  = get_transactions(identifier)
    symmetric_df = get_transactions(symmetric_identifier)
    # final_df = pd.DataFrame()
    # final_df['TIME_PERIOD'] = symmetric_df['TIME_PERIOD']
    # final_df['PROVIDED_ID'] = [identifier]*len(symmetric_df) 
    # final_df["SYMMETRIC_ID"] = [symmetric_identifier]* len(symmetric_df)
    # final_df["DELTA"] = provided_df['OBS_VALUE'] - symmetric_df['OBS_VALUE']
    # final_df.to_csv("output.csv")

    final_df = pd.merge(provided_df, 
                        symmetric_df[['TIME_PERIOD', 'IDENTIFIER','OBS_VALUE']],
                        on = 'TIME_PERIOD',
                        how = 'left').dropna()
    
    final_df['DELTA'] = final_df['OBS_VALUE_y'] - final_df['OBS_VALUE_x']
    final_df.rename(columns = {'IDENTIFIER_x': 'PROVIDED_ID', 'IDENTIFIER_y': 'SYMMETRIC_ID'}, inplace=True)
    final_df = final_df.drop(['OBS_VALUE_x', 'OBS_VALUE_y'], axis=1)
    final_df = final_df.iloc[:,[1,0,2,3]]
    return final_df

if __name__ == "__main__":
    transaction_data = get_transactions("Q.DE.N.A.A20.A.1.AT.2000.Z01.E")
    print(transaction_data.to_string(index = False))
    symmetric_identifier = get_symmetric_identifier("Q.HR.N.A.A20.A.1.AT.2000.Z01.E", {1: 7, 2: 3})
    print(symmetric_identifier)
    delta = get_asymmetries("Q.HR.N.A.A20.A.1.AT.2000.Z01.E", {1: 7})
    print(delta)



