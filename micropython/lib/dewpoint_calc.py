"""Utility to calculate the dew point."""

import math

def dewpoint(temp_c, humidity):
    """Return dew point in Celsius for given temperature and relative humidity."""
    a, b = 17.27, 237.7
    alpha = ((a * temp_c) / (b + temp_c)) + math.log(humidity / 100.0)
    return (b * alpha) / (a - alpha)
