from datetime import date

import pytest

from jobfunnel.backend import Job
from jobfunnel.backend.tools.filters import JobFilter, DuplicatedJob
from jobfunnel.resources import JobStatus, DuplicateType, Locale, Remoteness

job_test0 = Job("title0",
                "company0",
                "location0",
                "description0",
                "url0",
                Locale.USA_ENGLISH,
                "query0",
                "provider0",
                JobStatus.NEW,
                '0',
                post_date=date.today())

job_test1 = Job("title1",
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

job_test2 = Job("title2",
                "company2",
                "location2",
                "description2",
                "url2",
                Locale.USA_ENGLISH,
                "query2",
                "provider2",
                JobStatus.NEW,
                '2',
                post_date=date.today())


@pytest.mark.parametrize("job", (job_test0,))
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


@pytest.mark.parametrize("job", (job_test0,))
def test_is_duplicate_false(job):
    job_filter = JobFilter(log_file='jf.log')
    assert job_filter.is_duplicate(job) is False


@pytest.mark.parametrize("job", (job_test0,))
def test_filterable_true_status(job):
    job.status = JobStatus.OLD
    job_filter = JobFilter(log_file='jf.log')
    assert job_filter.filterable(job) is True


@pytest.mark.parametrize("job", (job_test0,))
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


@pytest.mark.parametrize("job", (job_test0,))
def test_filterable_true_blocked_company(job):
    job.status = JobStatus.NEW

    blocked_company_names_list = [job.company]

    job_filter_with_dub_list = JobFilter(blocked_company_names_list=blocked_company_names_list, log_file='jf_bc.log')
    assert job_filter_with_dub_list.filterable(job) is True


@pytest.mark.parametrize("job", (job_test0,))
def test_filterable_true_user_block_jobs_dict(job):
    job.status = JobStatus.NEW
    user_block_jobs_dict = [job.key_id]

    job_filter_with_dub_list = JobFilter(user_block_jobs_dict=user_block_jobs_dict, log_file='jf_bc.log')
    assert job_filter_with_dub_list.filterable(job) is True


@pytest.mark.parametrize("job", (job_test0,))
def test_filterable_true_remoteness(job):
    job.status = JobStatus.NEW
    job.remoteness = Remoteness.FULLY_REMOTE

    desired_remoteness = Remoteness.IN_PERSON

    job_filter_with_dub_list = JobFilter(desired_remoteness=desired_remoteness, log_file='jf_bc.log')
    assert job_filter_with_dub_list.filterable(job) is True


@pytest.mark.parametrize("job", (job_test0,))
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


existing_jobs_dict = {job_test0.key_id: job_test0, job_test2.key_id: job_test2}
incoming_jobs_dict = {job_test1.key_id: job_test1, job_test2.key_id: job_test2}
duplicated_jobs = [DuplicatedJob(
    original=job_test2,
    duplicate=job_test2,
    type=DuplicateType.KEY_ID,
)]


@pytest.mark.parametrize("existing_jobs_dict", (existing_jobs_dict,))
@pytest.mark.parametrize("incoming_jobs_dict", (incoming_jobs_dict,))
@pytest.mark.parametrize("duplicated_jobs", (duplicated_jobs,))
def test_find_duplicates(existing_jobs_dict, incoming_jobs_dict, duplicated_jobs):
    jobFilter = JobFilter(log_file='jf_fd.log')
    duplicate_jobs_list = jobFilter.find_duplicates(existing_jobs_dict, incoming_jobs_dict)
    for job in duplicated_jobs:
        assert job in duplicate_jobs_list


existing_jobs_dict = {job_test0.key_id: job_test0, job_test2.key_id: job_test2}
incoming_jobs_dict = {job_test1.key_id: job_test1, job_test2.key_id: job_test2}
duplicated_jobs = [DuplicatedJob(
    original=job_test1,
    duplicate=job_test2,
    type=DuplicateType.NEW_TFIDF,
)]


@pytest.mark.parametrize("existing_jobs_dict", (existing_jobs_dict,))
@pytest.mark.parametrize("incoming_jobs_dict", (incoming_jobs_dict,))
@pytest.mark.parametrize("duplicated_jobs", (duplicated_jobs,))
def test_tfidf_filter(existing_jobs_dict, incoming_jobs_dict, duplicated_jobs):
    jobFilter = JobFilter(log_file='jf_tf.log')
    duplicate_jobs_list = jobFilter.tfidf_filter(existing_jobs_dict, incoming_jobs_dict)
    for job in duplicated_jobs:
        assert job in duplicate_jobs_list
