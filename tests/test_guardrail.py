import time
import pytest
from guardrail import Guardrail, Request

def test_rate_limiting():
    guardrail = Guardrail(threshold=5, cooldown=10, max_failures=3)
    for _ in range(5):
        guardrail.handle_request(Request(time.time()))
    assert guardrail.is_rate_limited()

def test_circuit_breaker():
    guardrail = Guardrail(threshold=5, cooldown=10, max_failures=3)
    for _ in range(6):  # exceed threshold
        guardrail.handle_request(Request(time.time()))
    assert guardrail.is_circuit_open()

def test_recover():
    guardrail = Guardrail(threshold=5, cooldown=10, max_failures=3)
    guardrail.circuit_open = True
    guardrail.recover()
    assert not guardrail.is_circuit_open()

def test_handle_request_rate_limited():
    guardrail = Guardrail(threshold=1, cooldown=10, max_failures=3)
    guardrail.handle_request(Request(time.time()))
    exception = guardrail.handle_request(Request(time.time()))
    assert exception is not None
    assert str(exception) == "Rate limit exceeded"

def test_handle_request_circuit_open():
    guardrail = Guardrail(threshold=1, cooldown=10, max_failures=3)
    guardrail.circuit_open = True
    exception = guardrail.handle_request(Request(time.time()))
    assert exception is not None
    assert str(exception) == "Circuit is open"
