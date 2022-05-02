import io

import pandas as pd


def parse_inmemory_excel_to_dataframe(excel_file):
    in_file = io.BytesIO(excel_file.read())
    df = pd.read_excel(in_file, sheet_name=0)
    df = df.dropna()
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    return df
