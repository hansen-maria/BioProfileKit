import pandas as pd
import numpy as np
from dataclasses import dataclass
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.pyplot import autoscale
from numpy import ndarray
from pandas.core.dtypes.common import is_numeric_dtype, infer_dtype_from_object
from pandas.api.types import infer_dtype
from .sequence_enum import Sequence
from .wrapper_utils import fast_check_sequence
import plotly.express as px
from scipy import stats

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
- cardinalities
x missing values 
- constant values
- duplicated columns
x duplicated rows
- correlation
- memory usage per column
- distribution <-- skewness
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
    describe_plot: str | None
    # skewness: bool | None
    #constant_values: bool
    #correlation: list[str] | None


@dataclass
class NumericColumns:
    min: float
    max: float
    mean: float
    median: float
    mode: float
    std: float
    sum: float
    kurtosis: float
    skewness: float
    coefficient_of_variation: ndarray
    mad: float
    mode: float
    #cardinalities: list[int]

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
        describe_plot=plot_overview(df[col]),
    )

def numeric_columns(df: pd.DataFrame, col) -> NumericColumns:
    return NumericColumns(
        min=round(df[col].min(),2),
        max=round(df[col].max(),2),
        mean=round(df[col].mean(),2),
        median=round(df[col].median(),2),
        mode=round(df[col].mode().iloc[0],2),
        std=round(df[col].std(),2),
        sum=round(df[col].sum(),2),
        kurtosis=round(df[col].kurtosis(),2),
        skewness=round(df[col].skew(),2),
        mad = stats.median_abs_deviation(df[col],nan_policy='omit'), #Ignore NaN values, set Warning
        coefficient_of_variation=round(stats.variation(df[col],nan_policy='omit'),2)
    )


# ToDo: move to plot_utils
def plot_overview(col):
    if col.dtype != 'object':
        bins = None if col.nunique() < 10 else 10
        fig = px.histogram(col, nbins=bins, height=350, color_discrete_sequence=['#0F65A0'])
        fig.update_layout(bargap=0.2, plot_bgcolor='white')
        fig.update_xaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey'
        )
        fig.update_yaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey'
        )
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    return None

# ToDo: move to sequence_utils
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
