from numpy import gradient
from pandas.core.arrays.categorical import contains
from pandas.core.frame import DataFrame
import metrics
import fire
import pandas as pd
import re
from enum import Enum
from functools import reduce

class TransactionType(Enum):
    OPTION_BOUGHT = 1
    OPTION_SOLD = 2
    OPTION_EXPIRED = 3
    OPTION_ASSIGNED = 4
    STOCK_BOUGHT = 5
    STOCK_SOLD = 6

# Adds a column saying what kind of transaction it is.
def categorize_transactions(df: pd.DataFrame) -> pd.DataFrame:
    df['TransactionType'] = None

    return df

def match_group_1(rgx, string):
    p = re.compile(rgx)
    m = p.search(string)
    if m:
        return m.group(1)
    
    return None

def prototype(csv_files: list):
    # TODO: add stuff that filters the bs Fidelity adds to their exported CSVs
    dfs = []
    for file in csv_files:
        df: DataFrame = pd.read_csv(file, index_col="Run Date")
        dfs.append(df)
    
    df_merged = reduce(lambda  left,right: pd.merge(left,right,
                                            how='outer'), dfs)
    df_merged.sort_index()
    # df = categorize_transactions(df_merged)
    pd.set_option('display.max_columns', None)
    # print(df)

    # Tell me:
    # - Gross revenue from sell to open options
    # - Gross expense from buy to close options
    # - which symbols I've netted the most on
    symbols = df_merged['Action'].map(lambda s: match_group_1(r"\(([A-Z]+)\)", s)).dropna().unique()
    total_rev = 0
    total_expense = 0
    for symbol in symbols:
        contains_this_symbol = df_merged['Action'].str.contains(symbol)
        sold_to_open = df_merged['Action'].str.contains('SOLD OPENING')
        bought_to_close = df_merged['Action'].str.contains('BOUGHT CLOSING')
        gross_revenue = df_merged[sold_to_open & contains_this_symbol]['Amount'].sum()
        gross_expense = df_merged[bought_to_close & contains_this_symbol]['Amount'].sum()
        total_rev += gross_revenue
        total_expense += gross_expense
        if gross_revenue or gross_expense:
            print("-- {}: --".format(symbol))
            print("Revenue from selling to open {}: ${}".format(symbol, gross_revenue))
            print("Expense from buying to close {}: ${}".format(symbol, gross_expense))

    print("-- TOTAL --")
    print("Gross revenue: ${}".format(total_rev))
    print("Gross expense: ${}".format(total_expense))
    print("Net: ${}".format(total_rev + total_expense))


if __name__ == '__main__':
    # take cli args (files)
    fire.Fire(
        prototype
    )
