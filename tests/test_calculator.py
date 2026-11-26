from datetime import date
import pytest
from calculator import calculate_days

@pytest.mark.parametrize('birth,today,expected', [
    (date(2024,2,28),date(2024,3,1),2),
    (date(2023,2,28),date(2023,3,1),1),
    (date(1900,2,28),date(1900,3,1),1),
    (date(2000,2,28),date(2000,3,1),2),
    (date(2024,2,29),date(2024,3,1),1),
    (date(2024,1,1),date(2024,1,1),0),
])
def test_days(birth,today,expected):
    assert calculate_days(birth,today)==expected

def test_future():
    with pytest.raises(ValueError):
        calculate_days(date(2025,1,1),date(2024,1,1))
