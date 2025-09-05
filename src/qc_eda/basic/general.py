import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


def correlation_heatmap(df: pd.DataFrame):
    corr_matrix = df.select_dtypes(include=['float64', 'int64']).corr()
    corr_matrix = round(corr_matrix, 3)
    fig = px.imshow(corr_matrix, text_auto=True, labels=dict(color="Correlation"), color_continuous_scale="RdBu_r", aspect="auto")
    fig.update_layout(title="Correlation Heatmap")
    return fig


def missing_matrix(df: pd.DataFrame):
    missing_values = df.isnull().astype(int)
    row_wise_missing = missing_values.sum(axis=1)
    row_wise_missing.sort_values(ascending=False, inplace=True)

    fig = px.imshow(
        missing_values,
        labels=dict(color="Missing Values"),
        aspect="auto",
        color_continuous_scale="blues_r",
        title="Missing Values Matrix"
    )
    fig.update_xaxes(
        tickangle=-45,
        row=1,
        col=1,
        showgrid=False
    )
    fig.update_layout(coloraxis_showscale=False)
    fig.update_yaxes(tickvals=[1, df.index[-1]])
    return fig

def boxplot(df: pd.DataFrame):
    df = df.select_dtypes(include=['float64', 'int64'])
    fig = go.Figure()

    for col in df:
        fig.add_trace(go.Box(y=df[col].values, name=df[col].name))
    fig.update_yaxes(type="log", title="Logarithmic",showticklabels=False)
    fig.update_layout(
        title="Boxplot",
        xaxis_title="Columns",
        yaxis_title="Values",
        legend_title="Columns"
    )

    return fig
