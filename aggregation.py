"""
Excercise # 3 - Aggregation

Goal is to deduce the formula as per string input and apply calculcations accordingly
"""

import pandas as pd
from xml.dom.minidom import parse
from typing import Dict
import re

from web_downloader import fetch_data_from_url

def get_transactions(identifier: str) -> pd.DataFrame:
    """
    
    Description
    -----------
    Function will fetch the transaction data from the appropriate URL and convert it to a pandas DataFrame, with
    columns IDENTIFIER, TIME_PERIOD and OBS_VALUE, corresponding to values of the identifier parameter,
    generic:ObsDimension tag and generic:ObsValue tag from the XML. OBS_VALUE should be converted to
    float.

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

    >>> type(get_transactions("Q.N.I8.W1.S1.S1.T.A.FA.D.F._Z.EUR._T._X.N"))
    <class 'pandas.core.frame.DataFrame'>

    >>> get_transactions("Q.N.I8.W1.S1.S1.T.A.FA.D.F._Z.EUR._T._X.N").columns[0]
    'IDENTIFIER'

    >>> get_transactions("Q.N.I8.W1.S1.S1.T.A.FA.D.F._Z.EUR._T._X.N").columns[1]
    'TIME_PERIOD'

    >>> get_transactions("Q.N.I8.W1.S1.S1.T.A.FA.D.F._Z.EUR._T._X.N").columns[2]
    'OBS_VALUE'

    >>> type(get_transactions("Q.N.I8.W1.S1.S1.T.A.FA.D.F._Z.EUR._T._X.N").loc[2].at["OBS_VALUE"])
    <class 'numpy.float64'>

    >>> get_transactions("TUY")
    Traceback (most recent call last):
    requests.exceptions.HTTPError: Data is not available for given input
    
    """

    url = "https://sdw-wsrest.ecb.europa.eu/service/data/BP6/Q.N.I8.W1.S1.S1.T.A.FA.D.F._Z.EUR._T._X.N?detail=dataonly"
    url = url.replace("Q.N.I8.W1.S1.S1.T.A.FA.D.F._Z.EUR._T._X.N", identifier)
    transaction_data = fetch_data_from_url(url)
    transaction_data.insert(0, column= 'IDENTIFIER' , value = [identifier]*len(transaction_data))
    return transaction_data


def get_formula_data(formula: str) -> pd.DataFrame:
    """
    
    Description
    -----------
    This function first extract individual identifiers from the formula supplied
    and then get the transactions amount from the URL based on the identifiers

    Parameters
    -----------
    formula: str
        mathamatical formula in string

    Return 
    -----------

    Pandas Daraframe
        Pandas Dataframe (N x M)

    Test Cases

    -----------

    >>> type(get_formula_data("Q.N.I8.W1.S1.S1.T.A.FA.D.F._Z.EUR._T._X.N = \
                                    Q.N.I8.W1.S1P.S1.T.A.FA.D.F._Z.EUR._T._X.N + \
                                    Q.N.I8.W1.S1Q.S1.T.A.FA.D.F._Z.EUR._T._X.N"))
    <class 'pandas.core.frame.DataFrame'>

    >>> get_formula_data("Q.N.I8.W1.S1.S1.T.A.FA.D.F._Z.EUR._T._X.N = \
                          Q.N.I8.W1.S1P.S1.T.A.FA.D.F._Z.EUR._T._X.N + \
                          Q.N.I8.W1.S1Q.S1.T.A.FA.D.F._Z.EUR._T._X.N").columns[0]
    'TIME_PERIOD'

    >>> get_formula_data("Q.N.I8.W1.S1.S1.T.A.FA.D.F._Z.EUR._T._X.N = \
                          Q.N.I8.W1.S1P.S1.T.A.FA.D.F._Z.EUR._T._X.N + \
                          Q.N.I8.W1.S1Q.S1.T.A.FA.D.F._Z.EUR._T._X.N").columns[1]
    'Q.N.I8.W1.S1P.S1.T.A.FA.D.F._Z.EUR._T._X.N'

    >>> get_formula_data("Q.N.I8.W1.S1.S1.T.A.FA.D.F._Z.EUR._T._X.N = \
                          Q.N.I8.W1.S1P.S1.T.A.FA.D.F._Z.EUR._T._X.N + \
                          Q.N.I8.W1.S1Q.S1.T.A.FA.D.F._Z.EUR._T._X.N").columns[2]
    'Q.N.I8.W1.S1Q.S1.T.A.FA.D.F._Z.EUR._T._X.N'

    >>> type(get_formula_data("Q.N.I8.W1.S1.S1.T.A.FA.D.F._Z.EUR._T._X.N = \
                          Q.N.I8.W1.S1P.S1.T.A.FA.D.F._Z.EUR._T._X.N + \
                          Q.N.I8.W1.S1Q.S1.T.A.FA.D.F._Z.EUR._T._X.N").loc[2].at["Q.N.I8.W1.S1Q.S1.T.A.FA.D.F._Z.EUR._T._X.N"])
    <class 'numpy.float64'>

    >>> get_formula_data("TUY")
    Traceback (most recent call last):
    ValueError: formula syntax is not correct
    
    
    """
    
    identifier = re.split(r'[=+-]', formula)

    if len(identifier) < 3:
        raise ValueError("formula syntax is not correct")

    identifier_list = [content.strip(" ") for content in identifier][1:]
    
    dataframe_list = []
    for child_identifier in identifier_list:
        temp_data_frame = get_transactions(child_identifier)[['TIME_PERIOD','OBS_VALUE']].copy()
        dataframe_list.append(temp_data_frame)

        
    count = 0
    final_data_frame = dataframe_list[0]
    final_data_frame.rename(columns = {'OBS_VALUE':identifier_list[count]}, inplace = True)
    

    
    for data_frame in dataframe_list[1:]:
        count += 1
        data_frame.rename(columns = {'OBS_VALUE':identifier_list[count]}, inplace = True)
        final_data_frame = final_data_frame.merge(data_frame, on = 'TIME_PERIOD', how = 'left').fillna(0)
        
    
    

    return final_data_frame

def compute_aggregates(formula: str) -> pd.DataFrame:
    """
    
    
    Description
    -----------

    This will first deduce the formula based on the other functions and then apply it on the
    data and compute it.

    Parameters
    ----------

    formula: str
        mathamatical formula in string

    Return 
    -----------

    Pandas Daraframe
        Pandas Dataframe (N x M)

    Test Cases

    -----------

    >>> type(compute_aggregates("Q.N.I8.W1.S1.S1.T.A.FA.D.F._Z.EUR._T._X.N = \
                                  Q.N.I8.W1.S1P.S1.T.A.FA.D.F._Z.EUR._T._X.N + \
                                  Q.N.I8.W1.S1Q.S1.T.A.FA.D.F._Z.EUR._T._X.N"))
    <class 'pandas.core.frame.DataFrame'>

    >>> compute_aggregates("Q.N.I8.W1.S1.S1.T.A.FA.D.F._Z.EUR._T._X.N = \
                          Q.N.I8.W1.S1P.S1.T.A.FA.D.F._Z.EUR._T._X.N + \
                          Q.N.I8.W1.S1Q.S1.T.A.FA.D.F._Z.EUR._T._X.N").columns[0]
    'TIME_PERIOD'

    >>> compute_aggregates("Q.N.I8.W1.S1.S1.T.A.FA.D.F._Z.EUR._T._X.N = \
                          Q.N.I8.W1.S1P.S1.T.A.FA.D.F._Z.EUR._T._X.N + \
                          Q.N.I8.W1.S1Q.S1.T.A.FA.D.F._Z.EUR._T._X.N").columns[1]
    'Q.N.I8.W1.S1.S1.T.A.FA.D.F._Z.EUR._T._X.N'

   
    >>> type(compute_aggregates("Q.N.I8.W1.S1.S1.T.A.FA.D.F._Z.EUR._T._X.N = \
                          Q.N.I8.W1.S1P.S1.T.A.FA.D.F._Z.EUR._T._X.N + \
                          Q.N.I8.W1.S1Q.S1.T.A.FA.D.F._Z.EUR._T._X.N").loc[1].at["Q.N.I8.W1.S1.S1.T.A.FA.D.F._Z.EUR._T._X.N"])
    <class 'numpy.float64'>

    >>> compute_aggregates("TUY")
    Traceback (most recent call last):
    ValueError: formula syntax is not correct
    
    """
    identifier = re.split(r'[=+-]', formula)
    
    if len(identifier) < 3:
        raise ValueError("formula syntax is not correct")

    identifier_list = [content.strip(" ") for content in identifier][1:]

    compute_column = identifier[0].strip(" ")
    operators = []

    for char in formula:
        if char == '+':
            operators.append(char)
        if char == '-':
            operators.append(char)
    
    data_frame = get_formula_data(formula)
    
    count = 0
    data_frame[compute_column] = data_frame[identifier_list[count]]
    for operation in operators:
        if operation == "+":
            data_frame[compute_column] += data_frame[identifier_list[count+1]] 
        if operation == "-":
            data_frame[compute_column] -= data_frame[identifier_list[count+1]] 
        count += 1

    
    return pd.DataFrame(data_frame['TIME_PERIOD']).join(data_frame[compute_column])



if __name__ == "__main__":
    transasction_df = get_transactions("Q.N.I8.W1.S1.S1.T.A.FA.D.F._Z.EUR._T._X.N")
    print(transasction_df.to_string(index = False))

    formula_data = get_formula_data("Q.N.I8.W1.S1.S1.T.A.FA.D.F._Z.EUR._T._X.N = \
                                    Q.N.I8.W1.S1P.S1.T.A.FA.D.F._Z.EUR._T._X.N + \
                                    Q.N.I8.W1.S1Q.S1.T.A.FA.D.F._Z.EUR._T._X.N" )
    print(formula_data.head(2))


    compute_data_frame = compute_aggregates("Q.N.I8.W1.S1.S1.T.A.FA.D.F._Z.EUR._T._X.N = \
                                            Q.N.I8.W1.S1P.S1.T.A.FA.D.F._Z.EUR._T._X.N - \
                                            Q.N.I8.W1.S1Q.S1.T.A.FA.D.F._Z.EUR._T._X.N + \
                                            Q.N.I8.W1.S1.S1.T.A.FA.D.F._Z.EUR._T._X.N")
                                            
    print(compute_data_frame.head(2))
                                            


    