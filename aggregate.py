import math
import geojson

from utm import from_latlon, to_latlon, OutOfRangeError

PRECISION = 6  # Maximum precision of lat/lon coordinates of output


def getUtmFromCoordinates(lat, lon, span):
    """

    :synopsis: Convert lat/lon coordinates to UTM string
    :param float lat: Latitude
    :param float lon: Longitude
    :param span: (optional) Size of the UTM box (see below)
    :returns: UTM string with the correct resolution

    Convert lat/lon coordinates into a UTM string using the :py:obj:`UTM`
    package. If :py:obj:`span` is specified, the output resolution is degraded
    via the :py:obj:`floor` function.

    :py:obj:`span` accepts the values 'geo_10km', 'geo_1km', or the size of
    the UTM box in meters (should be a power of 10).

    This will NOT filter the location based on precision of the input
    coordinates.

    """

    span = _floatSpan(span)

    try:
        loc = from_latlon(lat, lon)
    except OutOfRangeError:
        # Catchall for any location that cannot be geocoded
        return None

    x, y, zonenum, zoneletter = loc
    x = myFloor(x, span)
    y = myFloor(y, span)

    if not x or not y or not zonenum:
        print('WARNING: Cannot get UTM for', lat, lon)
        return None

    utm = '{} {} {} {}'.format(x, y, zonenum, zoneletter)
    return utm


def _floatSpan(span):

    if span == 'geo_1km' or span == '1km' or span == 1000:
        span = 1000
    elif span == 'geo_10km' or span == '10km' or span == 10000:
        span = 10000
    else:
        raise TypeError('Invalid span value ' + str(span))

    return span


def myFloor(x, multiple):
    """

    :synopsis: Round down to a multiple of 10/100/1000...
    :param float x: A number
    :param int multiple: Power of 10 indicating how many places to round
    :returns: int

    This emulates the `math.floor` function but
    rounding down a positive power of 10 (i.e. 10, 100, 1000...)

    For example, myFloor(1975,100) returns 1900.

    """

    y = x/multiple
    return int(math.floor(y) * multiple)
