from signe import createSignal, effect, computed
from signe.types import TSetter, TGetter
from typing import TypeVar, Generic, overload, Union, Callable, cast
from nicegui import ui

T = TypeVar("T")


class ReadonlyRef(Generic[T]):
    def __init__(self, getter: TGetter[T]) -> None:
        self.___getter = getter

    @property
    def value(self):
        return self.___getter()


class Ref(ReadonlyRef[T]):
    def __init__(self, getter: TGetter[T], setter: TSetter[T]) -> None:
        super().__init__(getter)
        self.___setter = setter

    @property
    def value(self):
        return super().value

    @value.setter
    def value(self, value: T):
        self.___setter(value)


def ref(value: T):
    comp = False if isinstance(value, (list, dict)) else None
    getter, setter = createSignal(value, comp)
    return cast(Ref[T], Ref(getter, setter))


def ref_computed(fn: Callable[[], T]):
    getter = computed(fn)

    return ReadonlyRef(getter)


def effect_refreshable(func):
    re_func = ui.refreshable(func)

    first = True

    @effect
    def runner():
        nonlocal first
        if first:
            re_func()
            first = False
            return

        re_func.refresh()

    return runner
