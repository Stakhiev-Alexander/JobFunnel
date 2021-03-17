from cerberus import Validator
import pytest

from jobfunnel.config.settings import JobFunnelSettingsValidator, SETTINGS_YAML_SCHEMA
from jobfunnel.resources import (LOG_LEVEL_NAMES, DelayAlgorithm, Locale, Provider, Remoteness)

TEST_STRUCTURE_MINIMUM = {
    'master_csv_file': 'sample',
    'block_list_file': 'sample',
    'cache_folder': 'sample',
    'duplicates_list_file': 'sample',
    'log_file': 'sample',
    'search': {
        'schema': {
            'locale': Locale.USA_ENGLISH.name,
            'province_or_state': 'Dakota',
            'city': 'Dakota',
            'keywords': ['aa', 'bb'],
        },
    },
}

TEST_STRUCTURE_FALSE = {
    'not': 'aha',
    'wont': 'validate'
}


# test validation
def test_settings():
    SettingsValidator = JobFunnelSettingsValidator(SETTINGS_YAML_SCHEMA)
    TrueValidator = Validator(SETTINGS_YAML_SCHEMA)

    assert SettingsValidator.validate(TEST_STRUCTURE_MINIMUM) == TrueValidator.validate(TEST_STRUCTURE_MINIMUM)
    assert SettingsValidator.validate(TEST_STRUCTURE_FALSE) == TrueValidator.validate(TEST_STRUCTURE_FALSE)


def test_ipv4_address_validation_true():
    SettingsValidator = JobFunnelSettingsValidator(SETTINGS_YAML_SCHEMA)
    assert SettingsValidator._validate_type_ipv4address('127.0.0.1') == True

def test_ipv4_address_validation_exception():
    SettingsValidator = JobFunnelSettingsValidator(SETTINGS_YAML_SCHEMA)
    with pytest.raises(Exception):
        SettingsValidator._validate_type_ipv4address('NULL')


