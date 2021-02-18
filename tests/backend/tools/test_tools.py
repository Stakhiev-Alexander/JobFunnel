# FIXME

from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import pytest

from jobfunnel.backend.tools.tools import calc_post_date_from_relative_str


# test calc_post_date_from_relative_str
def test_hours_ago():
    post_date_str = "5 hours ago"
    true_post_time = (datetime.now() - timedelta(hours=5)).replace(hour=0, minute=0, second=0, microsecond=0)
    assert calc_post_date_from_relative_str(post_date_str) == true_post_time


def test_years_ago():
    post_date_str = "2 years ago"
    true_post_time = (datetime.now() - relativedelta(years=2)).replace(hour=0, minute=0, second=0, microsecond=0)
    assert calc_post_date_from_relative_str(post_date_str) == true_post_time


def test_months_ago():
    post_date_str = "3 months ago"
    true_post_time = (datetime.now() - relativedelta(months=3)).replace(hour=0, minute=0, second=0, microsecond=0)
    assert calc_post_date_from_relative_str(post_date_str) == true_post_time


def test_today():
    post_date_str = "today"
    true_post_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    assert calc_post_date_from_relative_str(post_date_str) == true_post_time


def test_yesterday():
    post_date_str = "yesterday"
    true_post_time = (datetime.now() - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    assert calc_post_date_from_relative_str(post_date_str) == true_post_time


def test_just_posted():
    post_date_str = "just posted"
    true_post_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    assert calc_post_date_from_relative_str(post_date_str) == true_post_time


def test_wrong_format():
    post_date_str = "########"
    with pytest.raises(ValueError):
        calc_post_date_from_relative_str(post_date_str)

