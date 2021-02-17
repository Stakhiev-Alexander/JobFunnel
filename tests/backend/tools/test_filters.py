import pytest
from datetime import date

from jobfunnel.backend import Job
from jobfunnel.backend.tools.filters import JobFilter, DuplicatedJob
from jobfunnel.resources import JobStatus, DuplicateType, Locale, Remoteness

job_test = Job("title1",
               "company1",
               "location1",
               "description1",
               "url1",
               Locale.USA_ENGLISH,
               "query1",
               "provider1",
               JobStatus.NEW,
               '1',
               post_date=date.today())


@pytest.mark.parametrize("job", (job_test,))
def test_is_duplicate_true(job):
    duplicate_jobs_dict = {}
    duplicate_job = DuplicatedJob(
        original=None,
        duplicate=job,
        type=DuplicateType.EXISTING_TFIDF,
    )
    duplicate_jobs_dict.update({
        duplicate_job.duplicate.key_id: duplicate_job.duplicate.as_json_entry
    })

    job_filter_with_dub_list = JobFilter(duplicate_jobs_dict=duplicate_jobs_dict, log_file='jf_wd.log')
    assert job_filter_with_dub_list.is_duplicate(job) is True


@pytest.mark.parametrize("job", (job_test,))
def test_is_duplicate_false(job):
    job_filter = JobFilter(log_file='jf.log')
    assert job_filter.is_duplicate(job) is False


@pytest.mark.parametrize("job", (job_test,))
def test_filterable_true_status(job):
    job.status = JobStatus.OLD
    job_filter = JobFilter(log_file='jf.log')
    assert job_filter.filterable(job) is True


@pytest.mark.parametrize("job", (job_test,))
def test_filterable_true_duplicate(job):
    job.status = JobStatus.NEW
    duplicate_jobs_dict = {}
    duplicate_job = DuplicatedJob(
        original=None,
        duplicate=job,
        type=DuplicateType.EXISTING_TFIDF,
    )
    duplicate_jobs_dict.update({
        duplicate_job.duplicate.key_id: duplicate_job.duplicate.as_json_entry
    })

    job_filter_with_dub_list = JobFilter(duplicate_jobs_dict=duplicate_jobs_dict, log_file='jf_wd.log')
    assert job_filter_with_dub_list.filterable(job) is True


@pytest.mark.parametrize("job", (job_test,))
def test_filterable_true_blocked_company(job):
    job.status = JobStatus.NEW

    blocked_company_names_list = [job.company]

    job_filter_with_dub_list = JobFilter(blocked_company_names_list=blocked_company_names_list, log_file='jf_bc.log')
    assert job_filter_with_dub_list.filterable(job) is True


@pytest.mark.parametrize("job", (job_test,))
def test_filterable_true_user_block_jobs_dict(job):
    job.status = JobStatus.NEW
    user_block_jobs_dict = [job.key_id]

    job_filter_with_dub_list = JobFilter(user_block_jobs_dict=user_block_jobs_dict, log_file='jf_bc.log')
    assert job_filter_with_dub_list.filterable(job) is True


@pytest.mark.parametrize("job", (job_test,))
def test_filterable_true_remoteness(job):
    job.status = JobStatus.NEW
    job.remoteness = Remoteness.FULLY_REMOTE

    desired_remoteness = Remoteness.IN_PERSON

    job_filter_with_dub_list = JobFilter(desired_remoteness=desired_remoteness, log_file='jf_bc.log')
    assert job_filter_with_dub_list.filterable(job) is True


@pytest.mark.parametrize("job", (job_test,))
def test_filterable_false_duplicate(job):
    job.status = JobStatus.NEW
    duplicate_jobs_dict = {}
    duplicate_job = DuplicatedJob(
        original=None,
        duplicate=job,
        type=DuplicateType.EXISTING_TFIDF,
    )
    duplicate_jobs_dict.update({
        duplicate_job.duplicate.key_id: duplicate_job.duplicate.as_json_entry
    })

    job_filter_with_dub_list = JobFilter(duplicate_jobs_dict=duplicate_jobs_dict, log_file='jf_wd.log')
    assert job_filter_with_dub_list.filterable(job, check_existing_duplicates=False) is False


@pytest.mark.parametrize("job", (job_test,))
def test_filterable_false(job):
    job.status = JobStatus.NEW
    job_filter = JobFilter(log_file='jf.log')
    assert job_filter.filterable(job) is False
