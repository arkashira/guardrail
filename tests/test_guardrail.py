from guardrail import Guardrail, EndpointTraffic
import pytest
from datetime import datetime, timedelta

@pytest.fixture
def guardrail():
    return Guardrail({})

def test_add_traffic(guardrail):
    guardrail.add_traffic('/api/endpoint', 10)
    assert len(guardrail.traffic_data['/api/endpoint']) == 1

def test_analyze_traffic(guardrail):
    guardrail.add_traffic('/api/endpoint', 10)
    guardrail.add_traffic('/api/endpoint', 20)
    guardrail.load_thresholds('{"/api/endpoint": {"baseline": 10, "threshold": 150}}')
    alerts = guardrail.analyze_traffic()
    assert len(alerts) == 1
    assert alerts[0].endpoint == '/api/endpoint'
    assert alerts[0].count == 30
    assert alerts[0].baseline == 10

def test_analyze_traffic_no_alert(guardrail):
    guardrail.add_traffic('/api/endpoint', 10)
    guardrail.load_thresholds('{"/api/endpoint": {"baseline": 10, "threshold": 150}}')
    alerts = guardrail.analyze_traffic()
    assert len(alerts) == 0

def test_load_thresholds(guardrail):
    guardrail.load_thresholds('{"/api/endpoint": {"baseline": 10, "threshold": 150}}')
    assert guardrail.thresholds == {"/api/endpoint": {"baseline": 10, "threshold": 150}}

def test_save_thresholds(guardrail):
    guardrail.load_thresholds('{"/api/endpoint": {"baseline": 10, "threshold": 150}}')
    assert guardrail.save_thresholds() == '{"/api/endpoint": {"baseline": 10, "threshold": 150}}'

def test_rolling_window(guardrail):
    guardrail.add_traffic('/api/endpoint', 10)
    guardrail.add_traffic('/api/endpoint', 20)
    rolling_window = guardrail._get_rolling_window(guardrail.traffic_data['/api/endpoint'])
    assert rolling_window == 30

def test_rolling_window_expired(guardrail):
    guardrail.add_traffic('/api/endpoint', 10)
    guardrail.traffic_data['/api/endpoint'][0] = (datetime.now() - timedelta(minutes=10), 10)
    rolling_window = guardrail._get_rolling_window(guardrail.traffic_data['/api/endpoint'])
    assert rolling_window == 0
