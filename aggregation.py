import pandas as pd
from xml.dom.minidom import parse
import xml.dom.minidom
import os
import requests
from typing import Dict
import re

from web_downloader import fetch_data_from_url

def get_transactions(identifier: str) -> pd.DataFrame:
    """
    
    """

    url = "https://sdw-wsrest.ecb.europa.eu/service/data/BP6/Q.N.I8.W1.S1.S1.T.A.FA.D.F._Z.EUR._T._X.N?detail=dataonly"
    url = url.replace("Q.N.I8.W1.S1.S1.T.A.FA.D.F._Z.EUR._T._X.N", identifier)
    transaction_data = fetch_data_from_url(url)
    transaction_data.insert(0, column= 'IDENTIFIER' , value = [identifier]*len(transaction_data))
    return transaction_data


def get_formula_data(formula: str) -> pd.DataFrame:
    """
    
    """
    
    identifier = re.split(r'[=+-]', formula)

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
    """
    identifier = re.split(r'[=+-]', formula)

    identifier_list = [content.strip(" ") for content in identifier][1:]

    compute_column = identifier[0].strip(" ")
    print(identifier_list)
    operators = []

    for char in formula:
        if char == '+':
            operators.append(char)
        if char == '-':
            operators.append(char)
    
    data_frame = get_formula_data(formula)
    
    count = 0
    data_frame[compute_column] = data_frame[identifier_list[count]]
    print(data_frame[compute_column].head(2))
    for operation in operators:
        print("in")
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
                                            


    