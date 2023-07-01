from .source import DataFrameSource
import pandas as pd
from .source import BuildOptionsArgs
from echarts.ECharts import EChartsClickEventArguments


def create_source(df: pd.DataFrame):
    return DataFrameSource(df)


__all__ = ["create_source", "BuildOptionsArgs", "EChartsClickEventArguments"]
