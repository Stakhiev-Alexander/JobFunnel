import os
from unittest.mock import patch

from jobfunnel.backend.jobfunnel import JobFunnel
from jobfunnel.config import get_config_manager, build_config_dict, parse_cli


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
