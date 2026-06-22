import json
from guardrail import Guardrail, APIKey

def test_register_api_key():
    guardrail = Guardrail()
    guardrail.register_api_key("key1", "AWS")
    assert len(guardrail.api_keys) == 1

def test_register_api_key_duplicate():
    guardrail = Guardrail()
    guardrail.register_api_key("key1", "AWS")
    try:
        guardrail.register_api_key("key1", "GCP")
        assert False
    except ValueError as e:
        assert str(e) == "API key already registered"

def test_validate_connectivity():
    guardrail = Guardrail()
    guardrail.register_api_key("key1", "AWS")
    assert guardrail.validate_connectivity("key1")

def test_monitor_api_key():
    guardrail = Guardrail()
    guardrail.register_api_key("key1", "AWS")
    guardrail.monitor_api_key("key1")
    assert guardrail.get_api_key_status("key1") == "active"

def test_get_api_key_status():
    guardrail = Guardrail()
    guardrail.register_api_key("key1", "AWS")
    assert guardrail.get_api_key_status("key1") == "protected"

def test_to_json():
    guardrail = Guardrail()
    guardrail.register_api_key("key1", "AWS")
    guardrail.register_api_key("key2", "GCP")
    data = json.loads(guardrail.to_json())
    assert len(data["api_keys"]) == 2
