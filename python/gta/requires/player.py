import gta_native

from gta import exceptions
from gta.requires import ped

__all__ = ('get_id', 'get_ped', 'get_vehicle')

def get_id(check_ped=True):
    """
    Return the player id.

    Arguments:
        - `check_ped`: If ``True``, make sure that the player's
          ped entity exists.
    """
    if check_ped:
        get_ped()
    return gta_native.player.player_id()


def get_ped():
    """
    Return the player ped.
    """
    # Check if the player ped and entity exists
    player_ped = gta_native.player.player_ped_id()
    if gta_native.entity.does_entity_exist(player_ped):
        return player_ped
    else:
        raise exceptions.RequirementError('Player entity')


def get_vehicle():
    """
    Return the vehicle the player is using.
    """
    return ped.get_vehicle(get_ped())
