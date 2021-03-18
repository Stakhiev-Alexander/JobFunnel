from datetime import date
import os
import pytest
from unittest import mock
from unittest.mock import patch

from jobfunnel.backend.jobfunnel import JobFunnel
from jobfunnel.config import get_config_manager, build_config_dict, parse_cli


@pytest.fixture
def jobfunnel():
    args = parse_cli(['load', '-s', os.path.dirname(os.path.realpath(__file__)) + '/tests_settings.yaml'])
    cfg_dict = build_config_dict(args)

    # Build config manager
    funnel_cfg = get_config_manager(cfg_dict)
    funnel_cfg.create_dirs()

    # Init
    return JobFunnel(funnel_cfg)


def test_jobfunnel_daily_cache_file(jobfunnel):
    daily_cache_file_path = os.path.join(
        'demo_job_search_results/cache',
        f"jobs_{date.today().strftime('%Y-%m-%d')}.pkl"
    )
    assert daily_cache_file_path == jobfunnel.daily_cache_file


@patch('jobfunnel.backend.jobfunnel.JobFunnel.run')
def test_jobfunnel_run(mock_run):
    args = parse_cli(['load', '-s', os.path.dirname(os.path.realpath(__file__)) + '/tests_settings.yaml'])
    cfg_dict = build_config_dict(args)

    # Build config manager
    funnel_cfg = get_config_manager(cfg_dict)
    funnel_cfg.create_dirs()

    # Init
    job_funnel = JobFunnel(funnel_cfg)
    job_funnel.run()
    assert job_funnel.run == mock_run
    assert mock_run.called


@patch('jobfunnel.backend.jobfunnel.JobFunnel.scrape')
def test_jobfunnel_scrape(mock_scrape):
    args = parse_cli(['load', '-s', os.path.dirname(os.path.realpath(__file__)) + '/tests_settings.yaml'])
    cfg_dict = build_config_dict(args)

    # Build config manager
    funnel_cfg = get_config_manager(cfg_dict)
    funnel_cfg.create_dirs()

    # Init
    job_funnel = JobFunnel(funnel_cfg)
    job_funnel.scrape()
    assert job_funnel.scrape == mock_scrape
    assert mock_scrape.called


@patch('jobfunnel.backend.jobfunnel.JobFunnel.recover')
def test_jobfunnel_recover(mock_recover):
    args = parse_cli(['load', '-s', os.path.dirname(os.path.realpath(__file__)) + '/tests_settings.yaml'])
    cfg_dict = build_config_dict(args)

    # Build config manager
    funnel_cfg = get_config_manager(cfg_dict)
    funnel_cfg.create_dirs()

    # Init
    job_funnel = JobFunnel(funnel_cfg)
    job_funnel.recover()
    assert job_funnel.recover == mock_recover
    assert mock_recover.called


@patch('jobfunnel.backend.jobfunnel.JobFunnel.load_cache')
def test_jobfunnel_load_cache(mock_load_cache):
    args = parse_cli(['load', '-s', os.path.dirname(os.path.realpath(__file__)) + '/tests_settings.yaml'])
    cfg_dict = build_config_dict(args)

    # Build config manager
    funnel_cfg = get_config_manager(cfg_dict)
    funnel_cfg.create_dirs()

    # Init
    job_funnel = JobFunnel(funnel_cfg)
    job_funnel.load_cache()
    assert job_funnel.load_cache == mock_load_cache
    assert mock_load_cache.called


@patch('jobfunnel.backend.jobfunnel.JobFunnel.write_cache')
def test_jobfunnel_write_cache(mock_write_cache):
    args = parse_cli(['load', '-s', os.path.dirname(os.path.realpath(__file__)) + '/tests_settings.yaml'])
    cfg_dict = build_config_dict(args)

    # Build config manager
    funnel_cfg = get_config_manager(cfg_dict)
    funnel_cfg.create_dirs()

    # Init
    job_funnel = JobFunnel(funnel_cfg)
    d = mock.Mock()
    job_funnel.write_cache(d)
    assert job_funnel.write_cache == mock_write_cache
    assert mock_write_cache.called


@patch('jobfunnel.backend.jobfunnel.JobFunnel.read_master_csv')
def test_jobfunnel_read_master_csv(mock_read_master_csv):
    args = parse_cli(['load', '-s', os.path.dirname(os.path.realpath(__file__)) + '/tests_settings.yaml'])
    cfg_dict = build_config_dict(args)

    # Build config manager
    funnel_cfg = get_config_manager(cfg_dict)
    funnel_cfg.create_dirs()

    # Init
    job_funnel = JobFunnel(funnel_cfg)
    job_funnel.read_master_csv()
    assert job_funnel.read_master_csv == mock_read_master_csv
    assert mock_read_master_csv.called


@patch('jobfunnel.backend.jobfunnel.JobFunnel.write_master_csv')
def test_jobfunnel_write_master_csv(mock_write_master_csv):
    args = parse_cli(['load', '-s', os.path.dirname(os.path.realpath(__file__)) + '/tests_settings.yaml'])
    cfg_dict = build_config_dict(args)

    # Build config manager
    funnel_cfg = get_config_manager(cfg_dict)
    funnel_cfg.create_dirs()

    # Init
    job_funnel = JobFunnel(funnel_cfg)
    job_funnel.write_master_csv()
    assert job_funnel.write_master_csv == mock_write_master_csv
    assert mock_write_master_csv.called


@patch('jobfunnel.backend.jobfunnel.JobFunnel.update_user_block_list')
def test_jobfunnel_update_user_block_list(mock_update_user_block_list):
    args = parse_cli(['load', '-s', os.path.dirname(os.path.realpath(__file__)) + '/tests_settings.yaml'])
    cfg_dict = build_config_dict(args)

    # Build config manager
    funnel_cfg = get_config_manager(cfg_dict)
    funnel_cfg.create_dirs()

    # Init
    job_funnel = JobFunnel(funnel_cfg)
    job_funnel.update_user_block_list()
    assert job_funnel.update_user_block_list == mock_update_user_block_list
    assert mock_update_user_block_list.called


@patch('jobfunnel.backend.jobfunnel.JobFunnel.update_duplicates_file')
def test_jobfunnel_update_duplicates_file(mock_update_duplicates_file):
    args = parse_cli(['load', '-s', os.path.dirname(os.path.realpath(__file__)) + '/tests_settings.yaml'])
    cfg_dict = build_config_dict(args)

    # Build config manager
    funnel_cfg = get_config_manager(cfg_dict)
    funnel_cfg.create_dirs()

    # Init
    job_funnel = JobFunnel(funnel_cfg)
    job_funnel.update_duplicates_file()
    assert job_funnel.update_duplicates_file == mock_update_duplicates_file
    assert mock_update_duplicates_file.called

