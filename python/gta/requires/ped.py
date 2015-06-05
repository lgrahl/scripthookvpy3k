import gta_native

from gta import exceptions

__all__ = ('get_vehicle',)


def get_vehicle(ped):
    """
    Return the vehicle a ped is using.

    Arguments:
        - `ped`: The id of the ped.
    """
    # Check if the ped is in a vehicle
    if gta_native.ped.is_ped_in_any_vehicle(ped, 0):
        return gta_native.ped.get_vehicle_ped_is_using(ped)
    else:
        raise exceptions.RequirementError('Vehicle of ped {}'.format(ped))
