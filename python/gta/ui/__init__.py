"""
UI components that can be used in GTA V.
"""
import enum
import collections
import weakref

__all__ = ('Point', 'Color', 'Direction', 'Align',
           'Item', 'SelectableItem', 'ActivatableItem', 'AlterableItem', 'Container',
           'add', 'remove')


class Point(collections.namedtuple('Point', 'x, y')):
    """
    A 2D point containing `x`- and `y`-coordinates.

    Arguments:
        - `x`: A `x`-coordinate value between ``0`` and ``1``.
        - `y`: A `y`-coordinate value between ``0`` and ``1``.
    """
    Zero = TopLeft = TopRight = BottomLeft = BottomRight = Center = None
    __slots__ = ()

# Point shorthands
Point.Zero = Point(0.0, 0.0)
Point.TopLeft = Point(0.0, 0.0)
Point.TopRight = Point(1.0, 0.0)
Point.BottomLeft = Point(0.0, 1.0)
Point.BottomRight = Point(1.0, 1.0)
Point.Center = Point(0.5, 0.5)


class Dimension(collections.namedtuple('Dimension', 'width, height')):
    """
    A 2D dimension containing width and height.

    Arguments:
        - `width`: A width value between ``0`` and ``1``.
        - `height`: A height value between ``0`` and ``1``.
    """
    Zero = Quarter = Half = Full = None
    __slots__ = ()

# Dimension shorthands
Dimension.Zero = Dimension(0.0, 0.0)
Dimension.Quarter = Dimension(0.25, 0.25)
Dimension.Half = Dimension(0.5, 0.5)
Dimension.Full = Dimension(1.0, 1.0)


class Distance(collections.namedtuple('Distance', 'top, right, bottom, left')):
    """
    Represents the space around an UI element.

    Arguments:
        - `top`: Space around the top.
        - `right`: Space around the right.
        - `bottom`: Space around the bottom.
        - `left:`: Space around the left.

    Alternatively, a single CSS-like margin string can be supplied
    with support for one to four values.
    """
    Zero = None
    __slots__ = ()

    def __new__(cls, *args, **kwargs):
        # Convert CSS-like margin string
        distance, *_ = args
        if isinstance(distance, str):
            values = [float(value) for value in distance.strip().split(' ')]
            top, right, bottom, left = [0.0] * 4
            length = len(values)
            if length == 1:
                top = right = bottom = left = values[0]
            elif length == 2:
                top, right = values
                bottom = top
                left = right
            elif length == 3:
                top, right, bottom = values
                left = right
            elif length == 4:
                top, right, bottom, left = values
            return super().__new__(cls, top, right, bottom, left)
        return super().__new__(cls, *args, **kwargs)

# Distance shorthands
Distance.Zero = Distance('0')


class Color(collections.namedtuple('Color', 'r, g, b, a')):
    """
    Represents an RGB (red, green, colour) value with an additional
    alpha channel.

    Arguments:
        - `r`: A red colour value between ``0`` and ``255``.
        - `g`: A green colour value between ``0`` and ``255``.
        - `b`: A blue colour value between ``0`` and ``255``.
        - `a`: An alpha channel value between ``0`` and ``255``.
          Defaults to ``255``.

    Alternatively, a single CSS-like hexadecimal colour string can be
    supplied.
    """
    Aqua = AliceBlue = AntiqueWhite = Black = Blue = Cyan = DarkBlue = DarkCyan =\
        DarkGreen = DarkTurquoise = DeepSkyBlue = Green = Lime = MediumBlue =\
        MediumSpringGreen = Navy = SpringGreen = Teal = MidnightBlue = DodgerBlue =\
        LightSeaGreen = ForestGreen = SeaGreen = DarkSlateGray = DarkSlateGrey =\
        LimeGreen = MediumSeaGreen = Turquoise = RoyalBlue = SteelBlue = DarkSlateBlue\
        = MediumTurquoise = Indigo = DarkOliveGreen = CadetBlue = CornflowerBlue =\
        MediumAquamarine = DimGray = DimGrey = SlateBlue = OliveDrab = SlateGray =\
        SlateGrey = LightSlateGray = LightSlateGrey = MediumSlateBlue = LawnGreen =\
        Aquamarine = Chartreuse = Gray = Grey = Maroon = Olive = Purple = LightSkyBlue =\
        SkyBlue = BlueViolet = DarkMagenta = DarkRed = SaddleBrown = DarkSeaGreen =\
        LightGreen = MediumPurple = DarkViolet = PaleGreen = DarkOrchid = YellowGreen\
        = Sienna = Brown = DarkGray = DarkGrey = GreenYellow = LightBlue = PaleTurquoise\
        = LightSteelBlue = PowderBlue = FireBrick = DarkGoldenrod = MediumOrchid =\
        RosyBrown = DarkKhaki = Silver = MediumVioletRed = IndianRed = Peru = Chocolate\
        = Tan = LightGray = LightGrey = Thistle = Goldenrod = Orchid = PaleVioletRed =\
        Crimson = Gainsboro = Plum = BurlyWood = LightCyan = Lavender = DarkSalmon =\
        PaleGoldenrod = Violet = Azure = Honeydew = Khaki = LightCoral = SandyBrown =\
        Beige = MintCream = Wheat = WhiteSmoke = GhostWhite = LightGoldenrodYellow =\
        Linen = Salmon = OldLace = Bisque = BlancheDalmond = Coral = CornSilk =\
        DarkOrange = DeepPink = FloralWhite = Fuchsia = Gold = HotPink = Ivory =\
        LavenderBlush = LemonChiffon = LightPink = LightSalmon = LightYellow = Magenta\
        = MistyRose = Moccasin = NavajoWhite = Orange = OrangeRed = PapayaWhip =\
        PeachPuff = Pink = Red = Seashell = Snow = Tomato = White = Yellow =\
        RebeccaPurple = None
    __slots__ = ()

    def __new__(cls, *args, a=255, **kwargs):
        # Convert CSS-like hexadecimal colour to integer values
        if len(args) > 0 and isinstance(args[0], str):
            color = args[0]
            r, g, b = (int(color[i + 1:i + 3], base=16) for i in range(0, 6, 2))
            return super(Color, cls).__new__(cls, r, g, b, a)
        return super(Color, cls).__new__(cls, *args, a=a, **kwargs)

    def alpha(self, value):
        """
        Return a new instance of the current colour with a different
        alpha value.

        Arguments:
            - `value`: An alpha channel value between ``0`` and
              ``255``.
        """
        return Color(self.r, self.g, self.b, a=value)

    @property
    def rgba(self):
        """
        Return the instances RGBA values as a tuple.
        """
        return tuple(self)

# Colour shorthands
Color.Aqua = Color(0, 255, 255)
Color.AliceBlue = Color(240, 248, 255)
Color.AntiqueWhite = Color(250, 235, 215)
Color.Black = Color(0, 0, 0)
Color.Blue = Color(0, 0, 255)
Color.Cyan = Color(0, 255, 255)
Color.DarkBlue = Color(0, 0, 139)
Color.DarkCyan = Color(0, 139, 139)
Color.DarkGreen = Color(0, 100, 0)
Color.DarkTurquoise = Color(0, 206, 209)
Color.DeepSkyBlue = Color(0, 191, 255)
Color.Green = Color(0, 128, 0)
Color.Lime = Color(0, 255, 0)
Color.MediumBlue = Color(0, 0, 205)
Color.MediumSpringGreen = Color(0, 250, 154)
Color.Navy = Color(0, 0, 128)
Color.SpringGreen = Color(0, 255, 127)
Color.Teal = Color(0, 128, 128)
Color.MidnightBlue = Color(25, 25, 112)
Color.DodgerBlue = Color(30, 144, 255)
Color.LightSeaGreen = Color(32, 178, 170)
Color.ForestGreen = Color(34, 139, 34)
Color.SeaGreen = Color(46, 139, 87)
Color.DarkSlateGray = Color(47, 79, 79)
Color.DarkSlateGrey = Color(47, 79, 79)
Color.LimeGreen = Color(50, 205, 50)
Color.MediumSeaGreen = Color(60, 179, 113)
Color.Turquoise = Color(64, 224, 208)
Color.RoyalBlue = Color(65, 105, 225)
Color.SteelBlue = Color(70, 130, 180)
Color.DarkSlateBlue = Color(72, 61, 139)
Color.MediumTurquoise = Color(72, 209, 204)
Color.Indigo = Color(75, 0, 130)
Color.DarkOliveGreen = Color(85, 107, 47)
Color.CadetBlue = Color(95, 158, 160)
Color.CornflowerBlue = Color(100, 149, 237)
Color.MediumAquamarine = Color(102, 205, 170)
Color.DimGray = Color(105, 105, 105)
Color.DimGrey = Color(105, 105, 105)
Color.SlateBlue = Color(106, 90, 205)
Color.OliveDrab = Color(107, 142, 35)
Color.SlateGray = Color(112, 128, 144)
Color.SlateGrey = Color(112, 128, 144)
Color.LightSlateGray = Color(119, 136, 153)
Color.LightSlateGrey = Color(119, 136, 153)
Color.MediumSlateBlue = Color(123, 104, 238)
Color.LawnGreen = Color(124, 252, 0)
Color.Aquamarine = Color(127, 255, 212)
Color.Chartreuse = Color(127, 255, 0)
Color.Gray = Color(128, 128, 128)
Color.Grey = Color(128, 128, 128)
Color.Maroon = Color(128, 0, 0)
Color.Olive = Color(128, 128, 0)
Color.Purple = Color(128, 0, 128)
Color.LightSkyBlue = Color(135, 206, 250)
Color.SkyBlue = Color(135, 206, 235)
Color.BlueViolet = Color(138, 43, 226)
Color.DarkMagenta = Color(139, 0, 139)
Color.DarkRed = Color(139, 0, 0)
Color.SaddleBrown = Color(139, 69, 19)
Color.DarkSeaGreen = Color(143, 188, 143)
Color.LightGreen = Color(144, 238, 144)
Color.MediumPurple = Color(147, 112, 219)
Color.DarkViolet = Color(148, 0, 211)
Color.PaleGreen = Color(152, 251, 152)
Color.DarkOrchid = Color(153, 50, 204)
Color.YellowGreen = Color(154, 205, 50)
Color.Sienna = Color(160, 82, 45)
Color.Brown = Color(165, 42, 42)
Color.DarkGray = Color(169, 169, 169)
Color.DarkGrey = Color(169, 169, 169)
Color.GreenYellow = Color(173, 255, 47)
Color.LightBlue = Color(173, 216, 230)
Color.PaleTurquoise = Color(175, 238, 238)
Color.LightSteelBlue = Color(176, 196, 222)
Color.PowderBlue = Color(176, 224, 230)
Color.FireBrick = Color(178, 34, 34)
Color.DarkGoldenrod = Color(184, 134, 11)
Color.MediumOrchid = Color(186, 85, 211)
Color.RosyBrown = Color(188, 143, 143)
Color.DarkKhaki = Color(189, 183, 107)
Color.Silver = Color(192, 192, 192)
Color.MediumVioletRed = Color(199, 21, 133)
Color.IndianRed = Color(205, 92, 92)
Color.Peru = Color(205, 133, 63)
Color.Chocolate = Color(210, 105, 30)
Color.Tan = Color(210, 180, 140)
Color.LightGray = Color(211, 211, 211)
Color.LightGrey = Color(211, 211, 211)
Color.Thistle = Color(216, 191, 216)
Color.Goldenrod = Color(218, 165, 32)
Color.Orchid = Color(218, 112, 214)
Color.PaleVioletRed = Color(219, 112, 147)
Color.Crimson = Color(220, 20, 60)
Color.Gainsboro = Color(220, 220, 220)
Color.Plum = Color(221, 160, 221)
Color.BurlyWood = Color(222, 184, 135)
Color.LightCyan = Color(224, 255, 255)
Color.Lavender = Color(230, 230, 250)
Color.DarkSalmon = Color(233, 150, 122)
Color.PaleGoldenrod = Color(238, 232, 170)
Color.Violet = Color(238, 130, 238)
Color.Azure = Color(240, 255, 255)
Color.Honeydew = Color(240, 255, 240)
Color.Khaki = Color(240, 230, 140)
Color.LightCoral = Color(240, 128, 128)
Color.SandyBrown = Color(244, 164, 96)
Color.Beige = Color(245, 245, 220)
Color.MintCream = Color(245, 255, 250)
Color.Wheat = Color(245, 222, 179)
Color.WhiteSmoke = Color(245, 245, 245)
Color.GhostWhite = Color(248, 248, 255)
Color.LightGoldenrodYellow = Color(250, 250, 210)
Color.Linen = Color(250, 240, 230)
Color.Salmon = Color(250, 128, 114)
Color.OldLace = Color(253, 245, 230)
Color.Bisque = Color(255, 228, 196)
Color.BlancheDalmond = Color(255, 235, 205)
Color.Coral = Color(255, 127, 80)
Color.CornSilk = Color(255, 248, 220)
Color.DarkOrange = Color(255, 140, 0)
Color.DeepPink = Color(255, 20, 147)
Color.FloralWhite = Color(255, 250, 240)
Color.Fuchsia = Color(255, 0, 255)
Color.Gold = Color(255, 215, 0)
Color.HotPink = Color(255, 105, 180)
Color.Ivory = Color(255, 255, 240)
Color.LavenderBlush = Color(255, 240, 245)
Color.LemonChiffon = Color(255, 250, 205)
Color.LightPink = Color(255, 182, 193)
Color.LightSalmon = Color(255, 160, 122)
Color.LightYellow = Color(255, 255, 224)
Color.Magenta = Color(255, 0, 255)
Color.MistyRose = Color(255, 228, 225)
Color.Moccasin = Color(255, 228, 181)
Color.NavajoWhite = Color(255, 222, 173)
Color.Orange = Color(255, 165, 0)
Color.OrangeRed = Color(255, 69, 0)
Color.PapayaWhip = Color(255, 239, 213)
Color.PeachPuff = Color(255, 218, 185)
Color.Pink = Color(255, 192, 203)
Color.Red = Color(255, 0, 0)
Color.Seashell = Color(255, 245, 238)
Color.Snow = Color(255, 250, 250)
Color.Tomato = Color(255, 99, 71)
Color.White = Color(255, 255, 255)
Color.Yellow = Color(255, 255, 0)
Color.RebeccaPurple = Color(102, 51, 153)


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
        - `margin`: The margin of the UI element. Use a
          :class:`Distance` instance to provide a margin.
        - `padding`: The padding of the UI element.
        - `position`: The position of the UI element on the view port.
          Defaults to top left of the screen.
        - `size`: The size of the UI element. Defaults to zero.
        - `color`: The colour of the UI element. Defaults to `black`.
    """
    def __init__(self, enabled=True, margin=Distance.Zero, position=Point.TopLeft,
                 size=Dimension.Zero, color=Color.Black):
        self._settings = {}
        self.enabled = enabled
        self.margin = margin
        self.position = position
        self.size = size  # TODO: Does this need to be applied on the abstract element?
        self.color = color

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

    def get_coordinates(self, offset):
        """
        Return the relative `x` and `y` coordinates. Takes account
        to `margin`, it's own `position` and the passed `offset`.

        Arguments:
            - `offset`: An offset for the item's position.
        """
        x = self.position.x + self.margin.left + offset.x
        y = self.position.y + self.margin.top + offset.y
        return x, y

    def get_dimension(self):
        """
        Return the relative dimension.
        """
        return self.size.width, self.size.height

    def draw(self, offset=Point.Zero, **settings):
        """
        Draw the element.

        Arguments:
            - `offset`: An offset that needs to be considered when
              calculating the draw position.
            - `settings`: Fallback settings that can be applied when a
              property has been set to ``None``.
        """
        raise NotImplementedError()


# noinspection PyAbstractClass
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


# noinspection PyAbstractClass
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


# noinspection PyAbstractClass
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

    def draw(self, offset=Point.Zero, **settings):
        """
        Draw the UI elements of the container.

        Arguments:
            - `offset`: The starting offset of the UI container.
            - `settings`: Fallback settings that will be passed to the
              UI elements.
        """
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


def _new_viewport():
    """
    Create and return a new viewport set.
    """
    return weakref.WeakSet()

_viewport = _new_viewport()


def add(item):
    """
    Add an UI item to the view port.

    .. note:: UI elements from scripts will be automatically removed
              when the script returns. But there will be a small delay
              until the garbage collector removes the elements.

    Arguments:
        - `item`: The :class:`Item` instance to be added.
    """
    _viewport.add(item)


def remove(item):
    """
    Remove an UI item from the view port.

    Arguments:
        - `item`: The :class:`Item` instance to be removed.
    """
    _viewport.remove(item)


def reset():
    """
    Reset the viewport instance.

    .. warning:: Do not call this function from a script!
    """
    global _viewport
    _viewport = _new_viewport()


def draw():
    """
    Draw all UI items on the viewport.

    .. warning:: Do not call this function from a script!
    """
    for item in _viewport:
        if item.enabled:
            item.draw()
