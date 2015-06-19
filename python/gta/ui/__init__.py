"""
UI components that can be used in GTA V.
"""
__all__ = ('Item', 'SelectableItem', 'ActivatableItem', 'AlterableItem', 'Container',
           'add', 'remove')

class Item:
    """
    Abstract UI element.
    """
    def __init__(self, enabled=True, position=None, size=None, color=None):
        self.enabled = enabled
        self.position = position
        self.size = size
        self.color = color

    def draw(self):
        """
        Draw the element.
        """
        raise NotImplementedError()


class SelectableItem(Item):
    """
    Abstract selectable UI element.

    Example: A menu item that can be selected by pressing `down` or
    `up`.
    """
    def select(self):
        """
        Called when the element is selected.
        """
        raise NotImplementedError()

    def deselect(self):
        """
        Called when the element is unselected.
        """
        raise NotImplementedError()


class ActivatableItem(SelectableItem):
    """
    Abstract activatable UI element.

    Example: A menu item that can be selected and activated by pressing
    `enter`.
    """
    def activate(self):
        """
        Called when the element has been activated.
        """
        raise NotImplementedError()


class AlterableItem(SelectableItem):
    """
    Abstract alterable UI element.

    Example: A menu item with a value that can be selected and altered
    by pressing `left` or `right`.
    """
    def next(self):
        """
        Called when requesting the next value.
        """
        raise NotImplementedError()

    def previous(self):
        """
        Called when requesting the previous value.
        """
        raise NotImplementedError()


class Container(Item):
    """
    Contains a collection of UI items.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items = []

    def __iadd__(self, item):
        self.add(item)

    def __isub__(self, item):
        self.remove(item)

    def add(self, item):
        """
        Add an UI item to the container.

        Arguments:
            - `item`: The :class:`Item` instance to be added.
        """
        self.items.append(item)

    def remove(self, item):
        """
        Remove an UI item from the container.

        Arguments:
            - `item`: The :class:`Item` instance to be removed.
        """
        self.items.append(item)

    def draw(self):
        """
        Draw all UI items of the container.
        """
        for item in self.items:
            if item.enabled:
                item.draw()


def add(item):
    """
    Add an UI item to the view port.

    Arguments:
        - `item`: The :class:`Item` instance to be added.
    """
    raise NotImplementedError()


def remove(item):
    """
    Remove an UI item from the view port.

    Arguments:
        - `item`: The :class:`Item` instance to be removed.
    """
    raise NotImplementedError()
