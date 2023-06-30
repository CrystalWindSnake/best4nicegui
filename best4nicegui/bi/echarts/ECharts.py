from typing import Callable, Optional

from nicegui import app, ui
from nicegui.dependencies import register_component
from nicegui.element import Element
from pathlib import Path

register_component("ECharts", __file__, "ECharts.js")


class echarts(Element):
    def __init__(self, options: dict, *, on_change: Optional[Callable] = None) -> None:
        super().__init__("ECharts")
        self._props["options"] = options
        self.on("change", on_change)

    def update_options(self, opts: dict, notMerge=False):
        self.run_method("updateOptions", opts, notMerge)
        self.update()
        return self
