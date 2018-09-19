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
import unidecode
import random
import numpy as np


def normalize_str(instr):
    output = re.sub(r'[^\w]', ' ', instr).strip().lower()
    output = re.sub(' +', ' ', output)
    output = output.title()
    return output


def normalize_str_nosp(instr):
    output = re.sub(r'[^\w]', ' ', instr).strip().lower()
    output = re.sub(' +', ' ', output)
    output = unidecode.unidecode(output).replace(' ', '_')
    return output


def normalize_string(df, column):
    df[column] = df[column].apply(normalize_str)


def print_category_info(df, column, n_rows=None, sort=True):
    printer.print_info('Número de {1} diferentes: {0}'.format(len(df[column].unique()), column))
    df = df.copy()
    df['####'] = 0
    dfx = df[[column, '####']].groupby(by=[column]).count()
    dfx.columns = ['N']
    dfx['%'] = 100 * dfx.N / dfx.N.sum()
    number_missings = df[column].isnull().sum()
    dfx = dfx.append(pandas.Series([number_missings, 100 * number_missings / df.shape[0]], index=dfx.columns, name='NaNs'))
    dfx = dfx.append(
        pandas.Series([df.shape[0], 100], index=dfx.columns, name='Total'))
    if sort:
        dfx.sort_values(by='N', inplace=True, ascending=False)
    printer.print_pandas_df(dfx, n_rows)


def read_csv_random_sample(filename, nsamples):
    n = sum(1 for line in open(filename)) - 1  # number of records in file (excludes header)
    s = 10000  # desired sample size
    skip = sorted(random.sample(range(1, n + 1), n - s))  # the 0-indexed header will not be included in the skip list
    df = pandas.read_csv(filename, skiprows=skip)

    return df

if __name__ == "__main__":
    data = []
    for i in range(10):
        data.append({'i': i,
                     'mystr': 'ThIS  is,a CompliCA;ted, ,,,,,s,tr,i,ng'})

    df = pandas.DataFrame(data)
    normalize_string(df, 'mystr')

    printer.print_pandas_df(df)


