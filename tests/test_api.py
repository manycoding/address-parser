import os
import tempfile

from api import *
from tests.addresses import *
import pytest


@pytest.mark.parametrize("address, expected", inputs_outs)
def test_parse(address, expected):
    with app.test_client() as c:
        rv = c.post("/parse", json={"address": address})
        assert rv.get_json() == expected
        assert rv.status_code == 200


@pytest.mark.parametrize(
    "address, expected",
    [
        ("", None),
        (
            [
                ("5760", "house_number"),
                ("teredo st.", "road"),
                ("sechelt", "city"),
                ("bc", "state"),
                ("canada", "country"),
                ("von 3a0", "postcode"),
            ],
            {
                "city": "Sechelt",
                "state": "BC",
                "street_address": "5760, Teredo St.",
                "postcode": "VON 3A0",
                "country": "Canada",
            },
        ),
        (
            [
                ("28", "house_number"),
                ("e 3rd ave", "road"),
                ("suite 201", "unit"),
                ("san mateo", "road"),
                ("94401", "postcode"),
                ("california", "state"),
            ],
            {
                # todo
                # "city": "San Mateo",
                "state": "CALIFORNIA",
                "street_address": "28, E 3Rd Ave, Suite 201",
                "postcode": "94401",
            },
        ),
        (
            [
                ("639", "house_number"),
                ("s spring st", "road"),
                ("los angeles", "city"),
                ("ca", "state"),
                ("90014", "postcode"),
                ("united states", "country"),
            ],
            {
                "city": "Los Angeles",
                "state": "CA",
                "street_address": "639, S Spring St",
                "postcode": "90014",
                "country": "United States",
            },
        ),
    ],
)
def test_get_address(address, expected):
    assert get_address(address) == expected


@pytest.mark.parametrize(
    "inp, expected",
    [
        (None, ""),
        (["e 3rd avenue", "san mateo",], "e 3rd avenue",),
        (["e 3rd avenue",], "e 3rd avenue",),
    ],
)
def test_get_first(inp, expected):
    assert get_first(inp) == expected
