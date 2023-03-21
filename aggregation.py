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

    url = "https://sdw-wsrest.ecb.europa.eu/service/data/BP6/Q.N.I8.W1.S1.S1.T.A.FA.D.F._Z.EUR._T._X.N?detail=dataonly"
    ulr = url.replace("Q.N.I8.W1.S1.S1.T.A.FA.D.F._Z.EUR._T._X.N", identifier)
    transaction_data = fetch_data_from_url(url)
    transaction_data.insert(0, column= 'IDENTIFIER' , value = [identifier]*len(transaction_data))
    return transaction_data

if __name__ == "__main__":
    transasction_df = get_transactions("Q.N.I8.W1.S1.S1.T.A.FA.D.F._Z.EUR._T._X.N")
    print(transasction_df.head(5))