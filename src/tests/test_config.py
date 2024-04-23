import os
import pytest

from config import Config, ConfigurationError

@pytest.fixture
def set_env_variables():
    os.environ["MODE"] = "cost_provisioning"
    os.environ["PERSISTENT_FILE"] = "metrics_store.json"
    os.environ["TAGS_DISCOVERY_URL"] = "http://localhost:3000"
    os.environ["SCHEDULE_MINUTE"] = "10"
    os.environ["SCHEDULE_HOUR"] = "23"
    yield
    del os.environ["MODE"]
    del os.environ["PERSISTENT_FILE"]
    del os.environ["TAGS_DISCOVERY_URL"]
    del os.environ["SCHEDULE_MINUTE"]
    del os.environ["SCHEDULE_HOUR"]

def test_valid_mode(set_env_variables):
    config = Config()
    assert config.mode == Config.COST_PROVISIONING

def test_invalid_mode(set_env_variables):
    os.environ["MODE"] = "invalid_mode"
    with pytest.raises(ConfigurationError):
        config = Config()

def test_cost_provisioning_parameters(set_env_variables):
    config = Config()
    assert config.persistent_file_path == "metrics_store.json"
    assert config.tags_host == "http://localhost:3000"
    assert config.is_cost_provisioning() == True

def test_tag_provisioning_parameters(set_env_variables):
    os.environ["MODE"] = "tag_provisioning"
    config = Config()
    assert config.tags_list == ["team", "service"]
    assert config.is_tag_provisioning() == True

def test_nonexistent_file(set_env_variables):
    os.environ["PERSISTENT_FILE"] = "nonexistent_file.json"
    with pytest.raises(ConfigurationError):
        config = Config()

def test_schedule_parameters(set_env_variables):
    config = Config()
    assert config.schedule_minute == "10"
    assert config.schedule_hour == "23"
