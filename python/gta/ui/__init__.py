"""
UI components that can be used in GTA V.
"""
__all__ = ('Container', 'add', 'remove')

class _Item:
    """
    Abstract UI class all UI elements inherit.
    """
    def __init__(self, enabled=True, position=None, size=None, color=None):
        self.enabled = enabled
        self.position = position
        self.size = size
        self.color = color

    def draw(self):
        raise NotImplementedError()


class Container(_Item):
    """
    Contains a collection of UI items.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items = []

    def add(self, item):
        self.items.append(item)

    def __iadd__(self, item):
        self.add(item)

    def draw(self):
        for item in self.items:
            if item.enabled:
                item.draw()


class Rectangle(_Item):
    """
    A basic rectangle.
    """
    pass


def add(item):
    """
    Add an UI item to the view port.

    Arguments:
        - `item`: The :class:`Container` instance to be added.
    """
    raise NotImplementedError()


def remove(item):
    """
    Remove an UI item from the view port.

    Arguments:
        - `item`: The :class:`Container` instance to be removed.
    """
    raise NotImplementedError()
