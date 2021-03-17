from jobfunnel.backend.jobfunnel import JobFunnel
from jobfunnel.config import get_config_manager, build_config_dict, parse_cli


def test_run():
    args = parse_cli(['load', '-s', 'tests_settings.yaml'])
    cfg_dict = build_config_dict(args)

    # Build config manager
    funnel_cfg = get_config_manager(cfg_dict)
    funnel_cfg.create_dirs()

    # Init
    job_funnel = JobFunnel(funnel_cfg)
    job_funnel.run()
    assert True
