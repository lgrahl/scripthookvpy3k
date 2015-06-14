"""
Basic UI components that use primitives to be drawn.
"""
from gta.ui import ActivatableItem, AlterableItem
from gta.ui.primitive import Rectangle, Label

__all__ = ('Button', 'Spinner')


class Button(ActivatableItem):
    pass


class Spinner(AlterableItem):
    pass
