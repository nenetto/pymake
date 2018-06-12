"""
pymake
-------------------------------
 - Eugenio Marinetto
 - nenetto@gmail.com
-------------------------------
Created 29-05-2018
"""
import pandas
from pymake.main import printer
import re

def normalize_str(instr):
    output = re.sub(r'[^\w]', ' ', instr).strip().lower()
    output = re.sub(' +', ' ', output)
    return output

def normalize_string(df, column):
    df[column] = df[column].apply(normalize_str)


if __name__ == "__main__":
    data = []
    for i in range(10):
        data.append({'i':i,
                     'mystr': 'ThIS  is,a CompliCA;ted'})

    df = pandas.DataFrame(data)
    normalize_string(df, 'mystr')

    printer.print_pandas_df(df)