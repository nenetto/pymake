"""
pymake
-------------------------------
 - Eugenio Marinetto
 - nenetto@gmail.com
-------------------------------
Created 29-05-2018
"""
import pandas as pd
from pymake.main import printer as pm
import numpy as np


def separate_numeric_column(df, column_name, verbose=True):
    """
    This function try to convert a column to a numeric. Those values where a number is not found are set to nans

    :param df: dataframe for input
    :type df: pandas.DataFrame
    :param column_name: name of the column to be fixed
    :type column_name: str
    """
    if verbose:
        pm.print_info('Fixing column {0}'.format(column_name))
        pm.print_info('Number of rows {0}'.format(df.shape[0]))

    # Copy column of interest
    dfx = df[[column_name]].copy()

    # Create type variable
    dfx[column_name + '_type'] = 'num'

    for i, row in dfx.iterrows():
        try:
            _ = float(row[column_name])
        except ValueError:
            dfx.loc[i, column_name + '_type'] = row[column_name]
            dfx.loc[i, column_name] = np.nan

    if verbose:
        pm.print_info('Number of different types reduces from {0} to {1}'.format(len(df[column_name].unique()),
                                                                                 len(dfx[column_name + '_type'].unique())))

        pm.print_info('Classification:')
        for e in dfx[column_name + '_type'].unique():

            n = dfx[dfx[column_name + '_type'] == e].shape[0]

            pm.print_info_2('{0} # {1}'.format(e, n), padding=1)

    if column_name + '_type' not in df.columns:
        df[column_name] = dfx[column_name].copy()
        df[column_name + '_type'] = dfx[column_name + '_type'].copy()
    else:
        pm.print_warning('Seems to be numeric, please revise')

