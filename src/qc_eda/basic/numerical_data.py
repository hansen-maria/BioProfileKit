import pandas as pd
import numpy as np
from dataclasses import dataclass

from pandas.core.dtypes.common import is_numeric_dtype, infer_dtype_from_object
from pandas.api.types import infer_dtype
from .sequence_enum import Sequence
from .wrapper_utils import fast_check_sequence

"""
Numerical data:
- min/max/mean/median-range
- quartiles
- mode
- std
- sum
- median absolute deviation
- coefficient of variation
- kurtosis
- skewness
"""
@dataclass
class NumericalData:
    filename: str
    rows: int
    cols: int
    nulls: int
    nulls_percentage: float
    dup_row: int
    dup_col: int
    memory: float
    alerts: int

@dataclass
class ColumnOverview:
    name: str
    number: int
    unique: int
    missing: int
    missing_per: float
    type: str
    sequence: str

def overview(df: pd.DataFrame, file)-> NumericalData:

    return NumericalData(
        filename=file,
        rows = df.shape[0],
        cols = df.shape[1],
        nulls = sum(df.isnull().sum()),
        nulls_percentage = round(sum(df.isnull().sum())  * 100 / df.size, 2),
        dup_row = int(df.duplicated().sum()),
        dup_col = int(df.columns.duplicated().sum()),
        memory = int(df.memory_usage().sum()),
        alerts = 0
    )

def column_overview(df: pd.DataFrame, col) -> ColumnOverview:
    return ColumnOverview(
        name=col,
        number=int(df[col].notnull().sum()),
        unique=df[col].nunique(),
        missing=int(df[col].isnull().sum()),
        missing_per = round(float(df[col].isnull().sum()  * 100 / df[col].size),2),
        type=str(df[col].dtype),
        sequence=check_sequence(df, col),
    )

def check_sequence(df, col):
    if df[col].name in df.select_dtypes(include='number').columns or infer_dtype(df[col]).__contains__('mixed'):
        return "None"

    values = df[col].dropna().astype(str).tolist()

    if all(len(x) > 1 for x in values):
        if fast_check_sequence(values, Sequence.DNA.value):
            return "dna"
        elif fast_check_sequence(values, Sequence.RNA.value):
            return "rna"
        elif fast_check_sequence(values, Sequence.PROTEIN.value):
            return "protein"

    return "None"
