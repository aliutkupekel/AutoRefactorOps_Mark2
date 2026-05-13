import pytest
from target_smelly import calculate_shipping

def test_member_short_distance_light_weight():
    assert calculate_shipping(40, 5, True) == 5

def test_member_short_distance_heavy_weight():
    assert calculate_shipping(40, 15, True) == 10

def test_member_long_distance_heavy_weight():
    assert calculate_shipping(100, 15, True) == 20

def test_non_member_short_distance_light_weight():
    assert calculate_shipping(40, 5, False) == 10

def test_non_member_long_distance_heavy_weight():
    assert calculate_shipping(100, 15, False) == 25