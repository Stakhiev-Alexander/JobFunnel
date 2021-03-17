# FIXME: need to break down config manager testing a bit more
from unittest import mock
from unittest.mock import patch

import pytest

from jobfunnel.backend import jobfunnel
from jobfunnel.config import JobFunnelConfigManager, SearchConfig
from jobfunnel.resources import Provider, Locale


@pytest.mark.parametrize('pass_del_cfg', (True, False))
def test_config_manager_init(mocker, pass_del_cfg):
    """NOTE: unlike other configs this one validates itself on creation
    """
    # Mocks
    patch_del_cfg = mocker.patch('jobfunnel.config.manager.DelayConfig')
    patch_os = mocker.patch('jobfunnel.config.manager.os')
    patch_os.path.exists.return_value = False  # check it makes all paths
    mock_master_csv = mocker.Mock()
    mock_block_list = mocker.Mock()
    mock_dupe_list = mocker.Mock()
    mock_cache_folder = mocker.Mock()
    mock_search_cfg = mocker.Mock()
    mock_proxy_cfg = mocker.Mock()
    mock_del_cfg = mocker.Mock()

    # FUT
    cfg = JobFunnelConfigManager(
        master_csv_file=mock_master_csv,
        user_block_list_file=mock_block_list,
        duplicates_list_file=mock_dupe_list,
        cache_folder=mock_cache_folder,
        search_config=mock_search_cfg,
        delay_config=mock_del_cfg if pass_del_cfg else None,
        proxy_config=mock_proxy_cfg,
        log_file='',  # TODO optional?
    )

    # Assertions


def test_manager_config_scrapers():
    search = mock.Mock()
    search.locale = Locale.CANADA_ENGLISH
    search.providers = [Provider.INDEED]
    mng = JobFunnelConfigManager("a", "b", "c", "d", search, "e")
    result = mng.scraper_names
    expected_result = ["IndeedScraperCANEng"]
    assert result == expected_result


def test_manager_config_scrapers_exception():
    search = mock.Mock()
    # search.locale = Locale.CANADA_ENGLISH
    search.providers = ["Wrong Provider"]
    mng = JobFunnelConfigManager("a", "b", "c", "d", search, "e")
    with pytest.raises(ValueError, match="No scraper available for unknown provider"):
        result = mng.scrapers



@patch('jobfunnel.config.JobFunnelConfigManager.validate')
def test_manager_validate_ip_positive(mock_validate):
    search = mock.Mock()
    mng = JobFunnelConfigManager("a", "b", "c", "d", search, "e")
    mng.validate()
    assert mng.validate == mock_validate
    assert mock_validate.called
