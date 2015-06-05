import sys
import os
import unittest.mock
import time


class GTANativeMock(unittest.mock.MagicMock):
    pass

# Create fake native module
sys.modules['_gta_native'] = GTANativeMock()
import gta


# noinspection PyProtectedMember
def main(stop_after=10.0):
    # We are running this from the 'python' directory, so we need to go up
    os.chdir('../')

    # Initialise
    gta._init(console=True)
    gta._tick()
    time.sleep(1.0)

    # Inject some keys and ticks
    gta._tick()
    gta._key(gta.Key.ADD.value, False, alt=False, ctrl=False, shift=False)
    time.sleep(0.2)
    gta._tick()
    time.sleep(0.3)
    gta._key(gta.Key.ADD.value, False, alt=False, ctrl=False, shift=True)
    gta._tick()
    time.sleep(0.5)
    gta._tick()
    gta._key(gta.Key.SUBTRACT.value, False, alt=False, ctrl=False, shift=False)
    gta._tick()
    gta._tick()

    # Stop
    if stop_after > 0:
        time.sleep(stop_after)
    # noinspection PyProtectedMember
    gta._exit()


if __name__ == '__main__':
    main()
