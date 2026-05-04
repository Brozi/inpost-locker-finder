from src.ilf.locker import Locker

from unittest.mock import patch

def test_parse_schedule():
    """Test that the parse_schedule function works properly"""
MOCK_HOURS = {"operating_hours_extended": {
      "customer": {
        "monday": [{"start": 540,"end": 1020}],
        "tuesday": [{"start": 540,"end": 1020}],
        "wednesday": [{"start": 540,"end": 1020}],
        "thursday": [{"start": 540,"end": 1020}],
        "friday": [{"start": 540,"end": 1020}],
        "saturday": [],
        "sunday": []
      }
    }
}
result = Locker._parse_schedule(MOCK_HOURS)

expected = "MON-FRI: 09:00-17:00, SAT-SUN: Closed"

assert result == expected