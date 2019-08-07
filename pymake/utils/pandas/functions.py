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
import os


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


def lxml_available():
    try:
        from lxml.etree import LXML_VERSION
        LXML = LXML_VERSION >= (3, 3, 1, 0)
        if not LXML:
            import warnings
            warnings.warn("The installed version of lxml is too old to be used with openpyxl")
            return False  # we have it, but too old
        else:
            return True  # we have it, and recent enough
    except ImportError:
        return False  # we don't even have it


def lxml_env_set():
    return os.environ.get("OPENPYXL_LXML", "True") == "True"


"""
def append_df_to_excel(filename, df, sheet_name='Sheet1', startrow=None,
                       truncate_sheet=False,
                       **to_excel_kwargs):
    
    Append a DataFrame [df] to existing Excel file [filename]
    into [sheet_name] Sheet.
    If [filename] doesn't exist, then this function will create it.

    Parameters:
      filename : File path or existing ExcelWriter
                 (Example: '/path/to/file.xlsx')
      df : dataframe to save to workbook
      sheet_name : Name of sheet which will contain DataFrame.
                   (default: 'Sheet1')
      startrow : upper left cell row to dump data frame.
                 Per default (startrow=None) calculate the last row
                 in the existing DF and write to the next row...
      truncate_sheet : truncate (remove and recreate) [sheet_name]
                       before writing DataFrame to Excel file
      to_excel_kwargs : arguments which will be passed to `DataFrame.to_excel()`
                        [can be dictionary]

    Returns: None
    
    LXML = lxml_available() and lxml_env_set()


    # ignore [engine] parameter if it was passed
    if 'engine' in to_excel_kwargs:
        to_excel_kwargs.pop('engine')

    writer = pandas.ExcelWriter(filename, engine='openpyxl')

    # Python 2.x: define [FileNotFoundError] exception if it doesn't exist
    try:
        FileNotFoundError
    except NameError:
        FileNotFoundError = IOError

    try:
        # try to open an existing workbook
        writer.book = load_workbook(filename,
                                    read_only=False,
                                    keep_vba=False,
                                    data_only=True,
                                    guess_types=False,
                                    keep_links=False)

        # get the last row in the existing Excel sheet
        # if it was not specified explicitly
        if startrow is None and sheet_name in writer.book.sheetnames:
            startrow = writer.book[sheet_name].max_row

        # truncate sheet
        if truncate_sheet and sheet_name in writer.book.sheetnames:
            # index of [sheet_name] sheet
            idx = writer.book.sheetnames.index(sheet_name)
            # remove [sheet_name]
            writer.book.remove(writer.book.worksheets[idx])
            # create an empty sheet [sheet_name] using old index
            writer.book.create_sheet(sheet_name, idx)

        # copy existing sheets
        writer.sheets = {ws.title:ws for ws in writer.book.worksheets}
    except FileNotFoundError:
        # file does not exist yet, we will create it
        pass

    if startrow is None:
        startrow = 0

    # write out the new sheet
    df.to_excel(writer, sheet_name, startrow=startrow, **to_excel_kwargs)

    # save the workbook
    writer.save()


if __name__ == "__main__":
    data = []
    for i in range(10):
        data.append({'i': i,
                     'mystr': 'ThIS  is,a CompliCA;ted, ,,,,,s,tr,i,ng'})

    df = pandas.DataFrame(data)
    normalize_string(df, 'mystr')

    printer.print_pandas_df(df)

"""
