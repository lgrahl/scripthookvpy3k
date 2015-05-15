import sys
import unittest.mock
import time
import threading

import gta


class GTANativeMock(unittest.mock.MagicMock):
    pass


def main(stop_after=10.0):
    # Create fake native module
    sys.modules['_gta_native'] = GTANativeMock()

    # Run in thread
    threading.Thread(target=run, args=(stop_after,)).start()

    # noinspection PyProtectedMember
    gta._init(console=True)


def run(stop_after):
    # Stop
    if stop_after > 0:
        time.sleep(stop_after)
        # noinspection PyProtectedMember
        gta._exit()


if __name__ == '__main__':
    main()
