import gta

__all__ = ('tick', 'key')


# Import wrapper events into this package
# noinspection PyProtectedMember
tick = gta._tick
# noinspection PyProtectedMember
key = gta._key
