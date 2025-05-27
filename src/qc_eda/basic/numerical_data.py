import pandas as pd
from dataclasses import dataclass

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



def overview(df: pd.DataFrame, file)-> NumericalData:

    return NumericalData(
        filename=file,
        rows = df.shape[0],
        cols = df.shape[1],
        nulls = sum(df.isnull().sum()),
        nulls_percentage = (sum(df.isnull().sum())  * 100 / df.size),
        dup_row = df.duplicated().sum(),
        dup_col = df.columns.duplicated().sum(),
        memory = df.memory_usage().sum(),
        alerts = 0
    )