#! usr/bin/env Python3

import pandas as pd
import pathlib
from functools import reduce


def read_file(file: str) -> pd.DataFrame:
    file = pathlib.Path(file).absolute()
    ext = pathlib.Path(file.__str__()).suffix
    if not ext in (".csv", ".tsv", ".json"):
        raise ValueError(f'File {file} is not a .csv or .tsv file')
    #ToDo: Index Col => determine if exist or not
    if ext == ".tsv":
        df = pd.read_csv(file.__str__(), header=0, index_col=0, sep="\t", low_memory=False)
        print(df.head())
        return df

    elif ext == ".csv":
        df = pd.read_csv(file.__str__(), header=0, index_col=0, sep=",", low_memory=False)
        return df

    elif ext == ".json":
        df = pd.read_json(file.__str__(), orient='values')
        cols = [i for i in df.columns if isinstance(df[i][0], dict)]
        if not cols:
            df = df.T
            cols = [i for i in df.columns if isinstance(df[i][0], dict)]
            if not cols:
                return df
            else:
                data_frames = list()
                for i in cols:
                    tmp = pd.json_normalize(df[i])
                    data_frames.append(tmp)
                df = reduce(lambda left, right: pd.merge(left, right, left_index=True, right_index=True), data_frames)

        return df

