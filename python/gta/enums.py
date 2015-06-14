"""
Various enumerators for GTA V and events.
"""
import enum

__all__ = ('Key', 'Font')


@enum.unique
class Key(enum.Enum):
    """
    Map virtual-key codes to names.

    See `MSDN Virtual-Key Codes <https://msdn.microsoft.com/en-us/library/windows/desktop/dd375731(v=vs.85).aspx>`_
    for further information.
    """
    LBUTTON = 1  # Left mouse button
    RBUTTON = 2  # Right mouse button
    CANCEL = 3  # Control-break processing
    MBUTTON = 4  # Middle mouse button (three-button mouse)
    BACK = 8  # BACKSPACE key
    TAB = 9  # TAB key
    CLEAR = 12  # CLEAR key
    RETURN = 13  # ENTER key
    SHIFT = 16  # SHIFT key
    CONTROL = 17  # CTRL key
    MENU = 18  # ALT key
    PAUSE = 19  # PAUSE key
    CAPITAL = 20  # CAPS LOCK key
    ESCAPE = 27  # ESC key
    SPACE = 32  # SPACEBAR
    PRIOR = 33  # PAGE UP key
    NEXT = 34  # PAGE DOWN key
    END = 35  # END key
    HOME = 36  # HOME key
    LEFT = 37  # LEFT ARROW key
    UP = 38  # UP ARROW key
    RIGHT = 39  # RIGHT ARROW key
    DOWN = 40  # DOWN ARROW key
    SELECT = 41  # SELECT key
    PRINT = 42  # PRINT key
    EXECUTE = 43  # EXECUTE key
    SNAPSHOT = 44  # PRINT SCREEN key
    INSERT = 45  # INS key
    DELETE = 46  # DEL key
    HELP = 47  # HELP key
    N0 = 48  # 0 key
    N1 = 49  # 1 key
    N2 = 50  # 2 key
    N3 = 51  # 3 key
    N4 = 52  # 4 key
    N5 = 53  # 5 key
    N6 = 54  # 6 key
    N7 = 55  # 7 key
    N8 = 56  # 8 key
    N9 = 57  # 9 key
    A = 65
    B = 66
    C = 67
    D = 68
    E = 69
    F = 70
    G = 71
    H = 72
    I = 73
    J = 74
    K = 75
    L = 76
    M = 77
    N = 78
    O = 79
    P = 80
    Q = 81
    R = 82
    S = 83
    T = 84
    U = 85
    V = 86
    W = 87
    X = 88
    Y = 89
    Z = 90
    LWIN = 91  # Left Windows key (Natural keyboard)
    RWIN = 92  # Right Windows key (Natural keyboard)
    APPS = 93  # Applications key (Natural keyboard)
    NUMPAD0 = 96  # Numeric keypad 0 key
    NUMPAD1 = 97  # Numeric keypad 1 key
    NUMPAD2 = 98  # Numeric keypad 2 key
    NUMPAD3 = 99  # Numeric keypad 3 key
    NUMPAD4 = 100  # Numeric keypad 4 key
    NUMPAD5 = 101  # Numeric keypad 5 key
    NUMPAD6 = 102  # Numeric keypad 6 key
    NUMPAD7 = 103  # Numeric keypad 7 key
    NUMPAD8 = 104  # Numeric keypad 8 key
    NUMPAD9 = 105  # Numeric keypad 9 key
    MULTIPLY = 106  # Multiply key
    ADD = 107  # Add key
    SEPARATOR = 108  # Separator key
    SUBTRACT = 109  # Subtract key
    DECIMAL = 110  # Decimal key
    DIVIDE = 111  # Divide key
    F1 = 112
    F2 = 113
    F3 = 114
    F4 = 115
    F5 = 116
    F6 = 117
    F7 = 118
    F8 = 119
    F9 = 120
    F10 = 121
    F11 = 122
    F12 = 123
    F13 = 124
    F14 = 125
    F15 = 126
    F16 = 127
    F17 = 128
    F18 = 129
    F19 = 130
    F20 = 131
    F21 = 132
    F22 = 133
    F23 = 134
    F24 = 135
    NUMLOCK = 144  # NUM LOCK key
    SCROLL = 145  # SCROLL LOCK key
    LSHIFT = 160  # Left SHIFT key
    RSHIFT = 161  # Right SHIFT key
    LCONTROL = 162  # Left CONTROL key
    RCONTROL = 163  # Right CONTROL key
    LMENU = 164  # Left MENU key
    RMENU = 165  # Right MENU key
    OEM_1 = 186  # May vary, US: ';:' key
    OEM_PLUS = 187  # '+' key
    OEM_COMMA = 188  # ',' key
    OEM_MINUS = 189  # '-' key
    OEM_PERIOD = 190  # '.' key
    OEM_2 = 191  # May vary, US: '/?' key
    OEM_3 = 192  # May vary, US: '~' key
    OEM_4 = 219  # May vary, US: '[{' key
    OEM_5 = 220  # May vary, US: '\|' key
    OEM_6 = 221  # May vary, US: ']}' key
    OEM_7 = 222  # May vary, US: single-quote/double-quote key
