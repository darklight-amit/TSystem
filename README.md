# TSystem
Project contains three excercise solutions and each excercise has 3 parts in it.

To support resuability principle web_downloader.py has introduced which will be used in all
three excercise solution

Each and every function has description in docstring and test cases are also covered there as well

run test cases for any python source file

    python3 -m doctest -v <filename.py>

example - to test web_downloader.py run below command

    python3 -m doctest -v web_downloader.py


Excercise # 1 : currency_conversion

This is having three functions conversion_data_frame, get_raw_data and get_data, which are 
returing the required dataframe, to see the output please execute below

    python3 currency_conversion.py

it will show first two rows of data frames got from each function.

It has total 11 test cases and with below command we can execute test suits-
    python3 -m doctest -v currency_conversion.py

remark - There is no positive test cases for #part3 because none of the API is providing data
         though I have tseted code with some other inputs

Excercise # 2 : asymmetry_check


To run the code please use below command-
    python3 asymmetry_check.py

It has total 13 test cases and with below command we can execute test suits-
    python3 -m doctest -v asymmetry_check.py

Excercise # 3: Aggregation

to run the code please use below command-
    python3 aggregation.py

it has total 17 test cases and with below command we can execute test suits-
    python3 -m doctest -v aggregation.py

