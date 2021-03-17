# FIXME

from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import pytest

from jobfunnel.backend.tools.tools import calc_post_date_from_relative_str

# test calc_post_date_from_relative_str
# try parametrized testing
@pytest.mark.parametrize("test_input,expected", [
    ("5 hours ago", (datetime.now() - timedelta(hours=5)).replace(hour=0, minute=0, second=0, microsecond=0)),
    ("2 years ago", (datetime.now() - relativedelta(years=2)).replace(hour=0, minute=0, second=0, microsecond=0)),
    ("3 months ago", (datetime.now() - relativedelta(months=3)).replace(hour=0, minute=0, second=0, microsecond=0)),
    ("today", (datetime.now().replace(hour=0, minute=0, second=0, microsecond=0))),
    ("yesterday", (datetime.now() - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)),
    ("just posted", datetime.now().replace(hour=0, minute=0, second=0, microsecond=0))
])
def test_calc_post_date_from_relative_str(test_input, expected):
    print(test_input, " ", expected)
    assert calc_post_date_from_relative_str(test_input) == expected


def test_wrong_format():
    post_date_str = "########"
    with pytest.raises(ValueError):
        calc_post_date_from_relative_str(post_date_str)
