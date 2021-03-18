import pytest

from datetime import datetime

from jobfunnel.resources import (JobField, JobStatus, Locale, Remoteness)
from jobfunnel.backend.job import Job


@pytest.fixture(params=['2021-03-14'])
def job(request):
    return Job(
        title='Senior Software Developer (Computer Vision)',
        company='Miovision',
        location='Kitchener, ON',
        description='description',
        url='https://job-openings.monster.ca/senior-software-developer-computer-vision-kitchener-on-ca-miovision/5f6d9426-83c3-41b2-ab75-0bba95593665',
        locale=Locale.CANADA_ENGLISH,
        query='Python',
        provider='MonsterScraperCANEng',
        status=JobStatus.NEW,
        key_id='5f6d9426-83c3-41b2-ab75-0bba95593665',
        scrape_date=None,
        short_description='',
        post_date=datetime.fromisoformat(request.param),
        raw=None,
        wage='',
        tags=None,
        remoteness=Remoteness.UNKNOWN
    )


@pytest.fixture
def json_entry():
    return {
        'title': 'Senior Software Developer (Computer Vision)',
        'company': 'Miovision',
        'post_date': '2021-03-14',
        'description': 'description',
        'status': JobStatus.NEW.name,
    }


@pytest.fixture
def newer_job():
    return Job(
        title='Senior Software Developer (Computer Vision)',
        company='Miovision',
        location='Kitchener, ON',
        description='',
        url='https://job-openings.monster.ca/senior-software-developer-computer-vision-kitchener-on-ca-miovision/5f6d9426-83c3-41b2-ab75-0bba95593665',
        locale=Locale.CANADA_ENGLISH,
        query='Python',
        provider='MonsterScraperCANEng',
        status=JobStatus.NEW,
        key_id='5f6d9426-83c3-41b2-ab75-0bba95593665',
        scrape_date=None,
        short_description='',
        post_date=datetime.fromisoformat('2021-03-16'),
        raw=None,
        wage='',
        tags=None,
        remoteness=Remoteness.UNKNOWN
    )


def test_is_remove_status(job):
    assert job.is_remove_status is False


def test_update_if_newer(job, newer_job):
    newer_job.company = 'New Company'
    job.update_if_newer(newer_job)

    assert job.company == newer_job.company


@pytest.mark.parametrize(
    'job',
    ['2021-03-14'],
    indirect=True
)
@pytest.mark.parametrize(
    'date, equals',
    [('2021-03-13', False), ('2021-03-15', True)]
)
def test_is_old(job, date, equals):
    assert job.is_old(datetime.fromisoformat(date)) is equals


def test_as_json_entry(job, json_entry):
    assert job.as_json_entry == json_entry


def test_validate(job):
    job.validate()
