#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A simple example of a test file using a function.
NOTE: All test file names must have one of the two forms.
- `test_<XYY>.py`
- '<XYZ>_test.py'

Docs: https://docs.pytest.org/en/latest/
      https://docs.pytest.org/en/latest/goodpractices.html#conventions-for-python-test-discovery
"""

import math
import pytest

import rplidar_plot as rp


# test init
@pytest.mark.parametrize(
    "index, theta, radius, quality",
    [
        (0, 0.28, 2013.00, 188),  # theta: 0.28 Dist: 02013.00 Q: 188
        (1, 0.59, 2013.00, 188),  # theta: 0.59 Dist: 02013.00 Q: 188
        (2, 0.89, 2013.00, 188),  # theta: 0.89 Dist: 02013.00 Q: 188
        (3, 1.20, 2013.00, 188),  # theta: 1.20 Dist: 02013.00 Q: 188
        (-4, 358.73, 2014.00, 188),  # theta: 358.73 Dist: 02014.00 Q: 188
        (-3, 359.10, 2013.00, 188),  # theta: 359.10 Dist: 02013.00 Q: 188
        (-2, 359.48, 2012.00, 188),  # theta: 359.48 Dist: 02012.00 Q: 188
        (-1, 359.95, 2013.00, 188),  # theta: 359.95 Dist: 02013.00 Q: 188
    ],
)
def test_value_change(data_dir, index, theta, radius, quality):
    container = rp.RpData(data_dir / "data.txt")
    dp1 = container.data[index]
    # 0.28 Dist: 02013.00 Q: 188
    assert dp1.theta == math.pi*theta/180.0
    assert dp1.radius == radius
    assert dp1.quality == quality


@pytest.mark.parametrize(
    "r, theta, x, y",
    [
        (math.sqrt(2.0), math.pi/4.0, 1.0, 1.0),  # 45
        (math.sqrt(2.0), 3.0*math.pi/4.0, -1.0, 1.0),  # 135
        (math.sqrt(2.0), 5.0*math.pi/4.0, -1.0, -1.0),  # 225
        (math.sqrt(2.0), 7.0*math.pi/4.0, 1.0, -1.0),  # 315
    ],
)
def test_xy_convert(data_dir, r, theta, x, y):
    dp = rp.DataPoint(theta=theta, radius=r, quality=188)
    assert dp.x == pytest.approx(x, 0.001)
    assert dp.y == pytest.approx(y, 0.001)


def test_plot(data_dir):
    dp = rp.RpData(filename=data_dir/"data.txt")
    dp.plot()
