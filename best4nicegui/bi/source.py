from signe import createSignal, effect, computed, batch
from signe.types import TGetter, TSetter
from nicegui import ui
from nicegui.element import Element
from typing import Optional, overload, List, Callable, cast, Dict, TypeVar, Any
import pandas as pd
from pandas.api.types import is_numeric_dtype
from typing_extensions import Literal
import operator
from .echarts.ECharts import echarts
import best4nicegui.utils.types as types_utils
from . import signature as cp_signature

_T = TypeVar("_T")

_TCpId = int
_TFilter = Callable[[pd.DataFrame], pd.Series]
_TFilterMap = Dict[_TCpId, _TFilter]

_TSliderOperators = Literal["<=", "==", ">=", "<", ">", "!="]
_slider_operator_map: Dict[_TSliderOperators, Any] = {
    "<=": operator.le,
    "==": operator.eq,
    ">=": operator.ge,
    "<": operator.lt,
    ">": operator.gt,
    "!=": operator.ne,
}


class DataFrameSource:
    def __init__(self, df: pd.DataFrame):
        self._org_df = df
        self.__get_filters, self._set_filters = createSignal(
            cast(_TFilterMap, {}), comp=False
        )

    def __getitem__(self, field: str):
        if field not in self._org_df.columns:
            raise KeyError(f"Field name[{field}] not exist in the source.")
        return FieldSource(self, field)

    def _get_filtered_df(self, element_id: _TCpId) -> pd.DataFrame:
        org_df = self._org_df
        filters_except_self = [
            f for id, f in self.__get_filters().items() if id != element_id
        ]

        for c in filters_except_self:
            org_df = org_df[c]  # type: ignore

        return org_df  # type: ignore

    def get_filtered_df(self, element: Element):
        return self._get_filtered_df(element.id)

    @types_utils.mirror_method(cp_signature.table)
    def table(self, *arg, **kws) -> ui.table:
        pagination = kws.get("pagination", cp_signature.Table_Defalut_pagination)

        element = ui.table([], [], *arg, **kws, pagination=pagination)
        element.classes("w-full")

        cols = [
            {"name": col, "field": col, "label": col} for col in self._org_df.columns
        ]

        element._props["columns"] = cols

        @effect
        def _():
            org_df = self._get_filtered_df(element.id)

            for col in org_df.select_dtypes(["datetime"]).columns:
                org_df[col] = org_df[col].dt.strftime("%Y-%m-%d")

            element.rows[:] = org_df.to_dict("records")  # type: ignore
            element.update()

        return element

    @types_utils.mirror_method(cp_signature.aggrid)
    def aggrid(self, *arg, **kws) -> ui.aggrid:
        element = ui.aggrid(
            {
                "pagination": True,
            },
            *arg,
            **kws,
        )

        @effect
        def _():
            org_df = self._get_filtered_df(element.id)
            for col in org_df.select_dtypes(["datetime"]).columns:
                org_df[col] = org_df[col].dt.strftime("%Y-%m-%d")

            element.options["columnDefs"] = [
                {"headerName": col, "field": col} for col in org_df.columns
            ]
            element.options["rowData"] = org_df.to_dict("records")  # type: ignore

            element.update()

        return element

    @types_utils.mirror_method(cp_signature.echarts)
    def echarts(self, *arg, **kws):
        return EChartsBinder(self, echarts({}, *arg, **kws))


class FieldSource:
    def __init__(self, df_source: DataFrameSource, field: str) -> None:
        self._df_source = df_source
        self.__field = field

    @types_utils.mirror_method(cp_signature.select)
    def select(self, *arg, **kws) -> ui.select:
        element = ui.select([], *arg, **kws)
        element._props["label"] = self.__field
        element.style("min-width:10rem")

        def on_update(args):
            value = args["args"]

            if value is None:
                value = []

            if isinstance(value, dict):
                value = [value]

            values = [v["label"] for v in value]

            @self._df_source._set_filters
            def _(filters_map: _TFilterMap):
                if len(values) == 0 and element.id in filters_map:
                    del filters_map[element.id]
                else:
                    filters_map[element.id] = lambda x: x[self.__field].isin(values)
                return filters_map

        element.on("update:model-value", handler=on_update)

        @effect
        def _():
            org_df = self._df_source._get_filtered_df(element.id)

            element.options = list(org_df[self.__field].drop_duplicates())
            element.update()

        return element

    @types_utils.mirror_method(ui.toggle)
    def toggle(self, *arg, **kws) -> ui.toggle:
        element = ui.toggle(*arg, **kws)

        def on_update(args):
            value = args["args"]

            if isinstance(value, int):
                value = element.options[value]

            @self._df_source._set_filters
            def _(filters_map: _TFilterMap):
                if value is None and element.id in filters_map:
                    del filters_map[element.id]
                else:
                    filters_map[element.id] = lambda x: x[self.__field] == value
                return filters_map

        element.on("update:model-value", handler=on_update)

        @effect
        def _():
            org_df = self._df_source._get_filtered_df(element.id)
            element.options = list(org_df[self.__field].drop_duplicates())

            element.update()

        return element

    @types_utils.mirror_method(ui.radio)
    def radio(self, *arg, **kws) -> ui.radio:
        element = ui.radio(*arg, **kws)

        def on_update(args):
            value = args["args"]

            if isinstance(value, int):
                value = element.options[value]

            @self._df_source._set_filters
            def _(filters_map: _TFilterMap):
                if value is None and element.id in filters_map:
                    del filters_map[element.id]
                else:
                    filters_map[element.id] = lambda x: x[self.__field] == value
                return filters_map

        element.on("update:model-value", handler=on_update)

        @effect
        def _():
            org_df = self._df_source._get_filtered_df(element.id)

            element.options = list(org_df[self.__field].drop_duplicates())
            element.update()

        return element

    @types_utils.mirror_method(ui.slider)
    def slider(self, operators: _TSliderOperators = "==", *arg, **kws) -> ui.slider:
        element = ui.slider(*arg, **kws)

        if not is_numeric_dtype(self._df_source._org_df[self.__field]):
            raise TypeError("The column type must be a number")

        element.classes(replace="my-4")

        def set_options(df: pd.DataFrame):
            element._props["min"], element._props["max"] = (
                df[self.__field].min(),
                df[self.__field].max(),
            )

            element._props["marker-labels"] = [
                {"value": element._props["min"], "label": f'{element._props["min"]}'},
                {"value": element._props["max"], "label": f'{element._props["max"]}'},
            ]

        element.props("label markers label-always")

        set_options(self._df_source._org_df)

        def on_update(args):
            value = args["args"]

            element._props["label-value"] = f"{self.__field} {operators} {value}"

            @self._df_source._set_filters
            def _(filters_map: _TFilterMap):
                if value is None and element.id in filters_map:
                    del filters_map[element.id]
                else:
                    filters_map[element.id] = lambda x: _slider_operator_map[operators](
                        x[self.__field], value
                    )
                return filters_map

        element.on("change", handler=on_update)

        @effect
        def _():
            filtered_df = self._df_source._get_filtered_df(element.id)
            set_options(filtered_df)
            element.update()

        return element


class EChartsBinder:
    def __init__(self, data_source: DataFrameSource, element: echarts) -> None:
        self.__element = element
        self.__ds = data_source
        self.__effect_fn: Optional[Callable] = None

    @property
    def element(self):
        return self.__element

    def force_refresh(self):
        if self.__effect_fn:
            self.__effect_fn()

    def build_options(self, fn: Callable[[pd.DataFrame], Dict]):
        """创建图表配置字典
        Args:
            fn (Callable[[pd.DataFrame], Dict]): 创建字典的函数。当数据源变动，此函数将被执行

        函数模板:
            ```python
            def opts(df:pd.DataFrame):

                # 使用 df 生成配置并返回
                opt_dict = {}
                return opt_dict
            ```

        """

        def update_options_callback():
            org_df = self.__ds.get_filtered_df(self.element)
            assert isinstance(org_df, pd.DataFrame)
            opts = fn(org_df)

            self.element.update_options(opts, True)

        self.__effect_fn = update_options_callback
        effect(self.__effect_fn)

        self.element._props["options"] = fn(self.__ds.get_filtered_df(self.element))  # type: ignore

        return self.element

    def build_options_pyecharts(self, fn: Callable[[pd.DataFrame], Any]):
        """使用 pyecharts 创建图表配置字典
        Args:
            fn (Callable[[pd.DataFrame], Any]): 创建字典的函数。当数据源变动，此函数将被执行

        函数模板:
            ```python
        def on_df_changed(df:pd.DataFrame):
            c = (
                Bar()
                .add_xaxis(df['x'])
                .add_yaxis("系列1", df['value'])
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(title_opts=opts.TitleOpts(title="Bar-堆叠数据（部分）"))
            )
            return c
            ```

        """

        import simplejson as json

        @self.build_options
        def opts(df: pd.DataFrame):
            chartbase = fn(df)
            opt_dict = json.loads(chartbase.dump_options())
            return opt_dict

        return self.element
