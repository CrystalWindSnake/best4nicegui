from typing import TypeVar, Generic, cast
from signe import createSignal, effect
from signe.types import TGetter, TSetter
from best4nicegui.utils.signals import ReadonlyRef, Ref
from nicegui import ui

T = TypeVar("T")

TWidget = TypeVar("TWidget")


class RefUi(Ref[T], Generic[T, TWidget]):
    def __init__(self, value: T, element: TWidget) -> None:
        getter, setter = createSignal(value)
        super().__init__(getter, setter)
        self.__element = element

    @property
    def element(self):
        return self.__element


class BindableUi(RefUi[T, TWidget]):
    def __init__(self, value: T, element: TWidget) -> None:
        super().__init__(value, element)

    def bind_prop(self, prop: str, ref_ui: RefUi):
        @effect
        def _():
            cast(ui.element, self.element)._props[prop] = ref_ui.value


class LabelBindableUi(BindableUi[str, TWidget]):
    def __init__(self, value: str, element: TWidget) -> None:
        super().__init__(value, element)

    def bind_text(self, ref_ui: RefUi):
        pass
