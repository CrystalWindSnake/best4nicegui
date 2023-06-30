from .source import DataFrameSource
import pandas as pd


def create_source(df: pd.DataFrame):
    return DataFrameSource(df)


__all__ = ["create_source"]
