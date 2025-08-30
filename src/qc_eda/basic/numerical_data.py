from dataclasses import dataclass

import pandas as pd
import plotly.express as px
from numpy import ndarray
from pandas.api.types import infer_dtype
from scipy import stats
from iteration_utilities import deepflatten

from .sequence_enum import Sequence
from .taxonomy_validator import validate_taxonomy
from .wrapper_utils import fast_check_sequence

"""
ToDo Numerical data:
x quantiles 
- cardinalities --> später
x constant values
- duplicated columns --> später
x correlation
x memory usage per column
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
    constant: bool
    # constant_values: bool
    correlation: list[str] | None
    top_10: pd.Series
    taxonomy: bool


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
    coefficient_of_variation: float
    mad: float
    mode: float
    quantiles: ndarray
    memory: int
    # cardinalities: list[int]


def overview(df: pd.DataFrame, file) -> NumericalData:
    return NumericalData(
        filename=file,
        rows=df.shape[0],
        cols=df.shape[1],
        nulls=sum(df.isnull().sum()),
        nulls_percentage=round(sum(df.isnull().sum()) * 100 / df.size, 2),
        dup_row=int(df.duplicated().sum()),
        dup_col=int(df.columns.duplicated().sum()),
        memory=int(df.memory_usage(deep=True).sum()),
        alerts=0
    )


def column_overview(df: pd.DataFrame, col) -> ColumnOverview:
    return ColumnOverview(
        name=col,
        number=int(df[col].notnull().sum()),
        unique=df[col].nunique(),
        missing=int(df[col].isnull().sum()),
        missing_per=round(float(df[col].isnull().sum() * 100 / df[col].size), 2),
        type=str(df[col].dtype),
        sequence=check_sequence(df, col),
        describe_plot=plot_overview(df[col]),
        constant=True if (df[col].nunique() == 1) else False,
        correlation=get_correlation(df, col),
        top_10=df[col].value_counts().head(10),
        taxonomy=rank_taxonomy(df, col)
    )


def numeric_columns(df: pd.DataFrame, col) -> NumericColumns:
    return NumericColumns(
        min=round(df[col].min(), 2),
        max=round(df[col].max(), 2),
        mean=round(df[col].mean(), 2),
        median=round(df[col].median(), 2),
        mode=round(df[col].mode().iloc[0], 2),
        std=round(df[col].std(), 2),
        sum=round(df[col].sum(), 2),
        kurtosis=round(df[col].kurtosis(), 2),
        skewness=round(df[col].skew(), 2),
        mad=stats.median_abs_deviation(df[col], nan_policy='omit'),  # Ignore NaN values, set Warning
        coefficient_of_variation=round(stats.variation(df[col], nan_policy='omit'), 2),
        quantiles=stats.quantile(df[col], [0.25, 0.5, 0.75]),
        memory=df[col].memory_usage(deep=True)
    )


def get_correlation(df: pd.DataFrame, col) -> list | None:
    ncols = df.select_dtypes(include='number').columns
    if col in ncols:
        corr = df[ncols].corrwith(df[col], method='pearson')
        corr.drop(labels=col, inplace=True)
        corr = corr.drop(corr[corr < .3].index)
        if corr.empty:
            return None
        return list(zip(corr.index, corr))
    return None


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


def rank_taxonomy(df, col):
    if df[col].dtype != 'object':
        return False

    results = df[col].astype(str).apply(lambda x: validate_taxonomy(x))
    results = results[~results.str.len().eq(0)]

    if not results.empty:
        results = set(deepflatten(results.value_counts().index.tolist(), depth=1))
        print(results)

    return False