from typing import Any, Callable, Optional
import best4nicegui.utils.types as types_utils
from nicegui import ui
from .ref import RefUi


@types_utils.mirror_func(ui.label)
def label(*arg, **kws) -> RefUi[str, ui.label]:
    element = ui.label(*arg, **kws)

    r = RefUi(element.text, element)

    def on_update():
        print("color change:", element.value)
        r.value = element.value

    element.on("update:modelValue", on_update)
    return r


def color_picker(init_color="rgba(88, 152, 212,1)") -> RefUi[str, ui.color_picker]:
    def on_pick(e):
        r.value = e.color

    with ui.card().tight():
        element = ui.color_picker(on_pick=on_pick)

        ui.button(on_click=element.open, icon="colorize")

    r = RefUi(init_color, element)

    return r
