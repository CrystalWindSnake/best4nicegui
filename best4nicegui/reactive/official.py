from typing import Any, Callable, Optional
import best4nicegui.utils.types as types_utils
from nicegui import ui
from .ref import (
    BindableUi,
    TextElementBindableUi,
    ValueElementBindableUi,
    TextColorElementBindableUi,
)
from signe import effect


@types_utils.mirror_func(ui.label)
def label(*arg, **kws) -> TextElementBindableUi[ui.label]:
    element = ui.label(*arg, **kws)
    r = TextElementBindableUi(element.text, element)
    return r


@types_utils.mirror_func(ui.input)
def input(*arg, **kws) -> ValueElementBindableUi[str, ui.input]:
    element = ui.input(*arg, **kws)
    r = ValueElementBindableUi(element.value, element)
    return r


@types_utils.mirror_func(ui.checkbox)
def checkbox(*arg, **kws) -> ValueElementBindableUi[bool, ui.checkbox]:
    element = ui.checkbox(*arg, **kws)
    r = ValueElementBindableUi(element.value, element)
    return r


@types_utils.mirror_func(ui.icon)
def icon(*arg, **kws) -> TextColorElementBindableUi[str, ui.icon]:
    element = ui.icon(*arg, **kws)
    r = TextColorElementBindableUi(element._props["name"], element)
    return r


def color_picker(init_color="rgba(88, 152, 212,1)") -> BindableUi[str, ui.color_picker]:
    def on_pick(e):
        r.value = e.color

    with ui.card().tight():
        element = ui.color_picker(on_pick=on_pick)

        ui.button(on_click=element.open, icon="colorize")

    r = BindableUi(init_color, element)

    return r
