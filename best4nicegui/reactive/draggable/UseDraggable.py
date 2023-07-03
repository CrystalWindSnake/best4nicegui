from typing import Any, Callable, Optional
from dataclasses import dataclass
from nicegui.helpers import KWONLY_SLOTS
from nicegui.events import handle_event, EventArguments
from nicegui.dependencies import register_component
from nicegui.element import Element
from signe import createSignal, effect


register_component("UseDraggable", __file__, "UseDraggable.js")

_Update_Args = [
    "x",
    "y",
    "style",
]


@dataclass(**KWONLY_SLOTS)
class UseDraggableUpdateEventArguments(EventArguments):
    x: float
    y: float
    style: str


def use_draggable(element: Element, auto_bind_style=True):
    ud = UseDraggable(element)
    if auto_bind_style:
        ud.bind_style(element)

    return ud


class UseDraggable(Element):
    def __init__(self, element: Element) -> None:
        super().__init__("UseDraggable")
        self._props["elementId"] = str(element.id)

        self.__style_getter, self.__style_setter = createSignal("")

        def update(args: UseDraggableUpdateEventArguments):
            self.__style_setter(args.style)

        self.on_update(update)

    def bind_style(self, element: Element):
        @effect
        def _():
            element.style(self.__style_getter())
            element.update()

    def on_update(self, handler: Optional[Callable[..., Any]]):
        def inner_handler(args: dict):
            args = args["args"]
            handle_event(
                handler,
                UseDraggableUpdateEventArguments(
                    sender=self,
                    client=self.client,
                    x=args["x"],
                    y=args["y"],
                    style=args["style"],
                ),
            )

        self.on("update", inner_handler, args=_Update_Args)
