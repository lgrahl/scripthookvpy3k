import sys
import unittest.mock

import gta


class GTANativeMock(unittest.mock.MagicMock):
    pass


def main():
    # Create fake native module
    sys.modules['_gta_native'] = GTANativeMock()

    # noinspection PyProtectedMember
    gta._init(console=True)

if __name__ == '__main__':
    main()
