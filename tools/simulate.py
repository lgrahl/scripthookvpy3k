import sys
import unittest.mock
import time

import gta


class GTANativeMock(unittest.mock.MagicMock):
    pass


def main(stop_after=10.0):
    # Create fake native module
    sys.modules['_gta_native'] = GTANativeMock()

    # noinspection PyProtectedMember
    gta._init(console=True)

    # Stop
    if stop_after > 0:
        time.sleep(stop_after)
    # noinspection PyProtectedMember
    gta._exit()


if __name__ == '__main__':
    main()
