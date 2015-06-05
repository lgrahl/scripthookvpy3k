import sys
import os
import unittest.mock
import time


class GTANativeMock(unittest.mock.MagicMock):
    pass

# Create fake native module
sys.modules['_gta_native'] = GTANativeMock()
import gta


def main(stop_after=10.0):
    # We are running this from the 'python' directory, so we need to go up
    os.chdir('../')

    # noinspection PyProtectedMember
    gta._init(console=True)

    # Stop
    if stop_after > 0:
        time.sleep(stop_after)
    # noinspection PyProtectedMember
    gta._exit()


if __name__ == '__main__':
    main()
