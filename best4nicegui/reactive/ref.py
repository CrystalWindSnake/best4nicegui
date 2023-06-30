from typing import TypeVar, Generic, cast
from signe import createSignal, effect
from signe.types import TGetter, TSetter
from best4nicegui.utils.signals import ReadonlyRef, Ref
from nicegui import ui
from nicegui.elements.mixins.text_element import TextElement
from nicegui.elements.mixins.value_element import ValueElement
from nicegui.elements.mixins.color_elements import (
    TextColorElement,
    QUASAR_COLORS,
    TAILWIND_COLORS,
)

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

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "visible":
            return self.bind_visible(ref_ui)

        @effect
        def _():
            element = cast(ui.element, self.element)
            element._props[prop] = ref_ui.value
            # element.update()

        return self

    def bind_visible(self, ref_ui: ReadonlyRef[bool]):
        @effect
        def _():
            element = cast(ui.element, self.element)
            element.set_visibility(ref_ui.value)

        return self


class TextColorElementBindableUi(BindableUi[T, TWidget]):
    def __init__(self, value: T, element: TWidget) -> None:
        super().__init__(value, element)

        ele = cast(TextColorElement, element)

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "name":
            return self.bind_name(ref_ui)

        if prop == "color":
            return self.bind_color(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_color(self, ref_ui: ReadonlyRef):
        @effect
        def _():
            ele = cast(TextColorElement, self.element)
            color = ref_ui.value

            if color in QUASAR_COLORS:
                ele._props[ele.TEXT_COLOR_PROP] = color
            elif color in TAILWIND_COLORS:
                ele._classes.append(f"text-{color}")
            elif color is not None:
                ele._style["color"] = color
            ele._props["name"] = ref_ui.value
            ele.update()

        return self

    def bind_name(self, ref_ui: ReadonlyRef):
        @effect
        def _():
            ele = cast(TextColorElement, self.element)
            ele._props["name"] = ref_ui.value
            ele.update()

        return self


class ValueElementBindableUi(BindableUi[T, TWidget]):
    def __init__(self, value: T, element: TWidget) -> None:
        super().__init__(value, element)

        def onValueChanged(args):
            self.value = args["args"]

        ele = cast(ValueElement, element)

        @effect
        def _():
            ele.value = self.value

        ele.on("update:modelValue", handler=onValueChanged)

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "value":
            return self.bind_text(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_text(self, ref_ui: ReadonlyRef):
        @effect
        def _():
            cast(ValueElement, self.element).on_value_change(ref_ui.value)

        return self


class TextElementBindableUi(BindableUi[str, TWidget]):
    def __init__(self, value: str, element: TWidget) -> None:
        super().__init__(value, element)

    def bind_prop(self, prop: str, ref_ui: ReadonlyRef):
        if prop == "text":
            return self.bind_text(ref_ui)

        return super().bind_prop(prop, ref_ui)

    def bind_text(self, ref_ui: ReadonlyRef):
        @effect
        def _():
            cast(TextElement, self.element).on_text_change(ref_ui.value)

        return self
