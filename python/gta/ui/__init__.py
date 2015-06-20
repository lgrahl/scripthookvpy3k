"""
UI components that can be used in GTA V.
"""
import enum
import collections

__all__ = ('Point', 'Color', 'Direction', 'Align',
           'Item', 'SelectableItem', 'ActivatableItem', 'AlterableItem', 'Container',
           'add', 'remove')


class Point(collections.namedtuple('Point', 'x, y')):
    """
    A 2D point containing x- and y-coordinates.

    Arguments:
        - `x`: The x-coordinate.
        - `y`: The y-coordinate.
    """
    pass


class Color(collections.namedtuple('Color', 'r, g, b, a')):
    """
    Represents an RGB (red, green, colour) value with an additional
    alpha channel.

    Arguments:
        - `r`: A red colour value between ``0`` and ``255``.
        - `g`: A green colour value between ``0`` and ``255``.
        - `b`: A blue colour value between ``0`` and ``255``.
        - `a`: An alpha channel value between ``0`` and ``1``. Defaults
          to ``1.0``.

    Alternatively, a single CSS-like hexadecimal colour string can be
    supplied.
    """
    def __new__(cls, *args, a=1.0, **kwargs):
        # Convert CSS-like hexadecimal colour to integer values
        color, *_ = args
        if isinstance(color, str) and len(color) == 7 and color[0] == '#':
            r, g, b = (color[i + 1:i + 3] for i in range(0, 6, 2))
            return super(Color, cls).__new__(cls, r, g, b, a)
        return super(Color, cls).__new__(cls, *args, a=a, **kwargs)


@enum.unique
class Direction(enum.Enum):
    """
    The direction of UI :class:`Container` child elements.
    """
    row = 0
    column = 1


@enum.unique
class Align(enum.Enum):
    """
    The alignment of UI :class:`Container` child elements.
    """
    left = 0
    center = 1
    right = 2


class Item:
    """
    Abstract UI element.

    Arguments:
        - `enabled`: Enable or disable the UI element.
        - `margin`: The margin of the UI element.
        - `padding`: The padding of the UI element.
        - `position`: The position of the UI element on the view port.
          Defaults to top left of the screen.
        - `size`: The size of the UI element.
        - `color`: The colour of the UI element. Defaults to `black`.
    """
    def __init__(self, enabled=True, position=None, size=None, color=None):
        self._settings = {}
        self.enabled = enabled
        self.margin = margin
        self.padding = padding
        self.position = Point(0.0, 0.0) if position is None else position
        self.size = size  # TODO: Does this need to be applied on the abstract element?
        self.color = Color('#000000') if color is None else color

    @property
    def enabled(self):
        return self._settings.get('enabled')

    @enabled.setter
    def enabled(self, value):
        self._settings['enabled'] = value

    @property
    def margin(self):
        return self._settings.get('margin')

    @margin.setter
    def margin(self, value):
        self._settings['margin'] = value

    @property
    def padding(self):
        return self._settings.get('padding')

    @padding.setter
    def padding(self, value):
        self._settings['padding'] = value

    @property
    def position(self):
        return self._settings.get('position')

    @position.setter
    def position(self, value):
        self._settings['position'] = value

    @property
    def size(self):
        return self._settings.get('size')

    @size.setter
    def size(self, value):
        self._settings['size'] = value

    @property
    def color(self):
        return self._settings.get('color')

    @color.setter
    def color(self, value):
        self._settings['color'] = value

    def draw(self, offset=None, **settings):
        """
        Draw the element.

        Arguments:
            - `offset`: An offset that needs to be considered when
              calculating the draw position.
            - `settings`: Fallback settings that can be applied when a
              property has been set to ``None``.
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

    Arguments:
        - `direction`: The direction the UI elements are placed.
        - `align`: The alignment of the UI elements.
    """
    def __init__(self, *args, direction=Direction.row, align=Align.left, **kwargs):
        super().__init__(*args, **kwargs)
        self.direction = direction
        self.align = align
        self._items = []

    def __iadd__(self, item):
        self.add(item)

    def __isub__(self, item):
        self.remove(item)

    @property
    def direction(self):
        return self._settings.get('direction')

    @direction.setter
    def direction(self, value):
        self._settings['direction'] = value

    @property
    def align(self):
        return self._settings.get('align')

    @align.setter
    def align(self, value):
        self._settings['align'] = value

    def add(self, item):
        """
        Add an UI item to the container.

        Arguments:
            - `item`: The :class:`Item` instance to be added.
        """
        self._items.append(item)

    def remove(self, item):
        """
        Remove an UI item from the container.

        Arguments:
            - `item`: The :class:`Item` instance to be removed.
        """
        self._items.append(item)

    def draw(self, offset=None, **settings):
        """
        Draw the UI elements of the container.

        Arguments:
            - `offset`: The starting offset of the UI container.
            - `settings`: Fallback settings that will be passed to the
              UI elements.
        """
        offset = Point(0.0, 0.0) if offset is None else offset
        # Override default settings
        settings.update(self._settings)

        # Draw each item
        i = 0
        for item in self._items:
            if item.enabled:
                # Draw the item when it is enabled with the calculated offset
                item_offset = offset + self.get_offset(i, item)
                item.draw(offset=item_offset, **settings)
                i += 1

    def get_offset(self, nr, item):
        """
        Calculate the offset for an UI element.

        Arguments:
            - `nr`: The sequence number of the UI element.
            - `item`: The UI element :class:`Item` instance.
        """
        raise NotImplementedError()


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
