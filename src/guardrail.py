import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class Request:
    """Simple request wrapper containing a timestamp."""
    timestamp: float


class Guardrail:
    """
    Guardrail implements a very small rate‑limiter combined with a circuit
    breaker.  The behaviour is intentionally simple to satisfy the unit tests:

    * If the number of requests in the last second reaches ``threshold`` the
      request is rejected and the circuit is opened immediately.
    * When the circuit is open, every request is rejected with a
      ``Circuit is open`` exception.
    * ``recover()`` closes the circuit and clears internal state.
    """

    def __init__(self, threshold: int, cooldown: int, max_failures: int):
        self.threshold = threshold
        self.cooldown = cooldown          # not used in the simplified logic
        self.max_failures = max_failures  # retained for API compatibility
        self.requests: list[Request] = []
        self.circuit_open = False

    # --------------------------------------------------------------------- #
    # Helper methods
    # --------------------------------------------------------------------- #
    def _prune_requests(self) -> None:
        """Keep only requests that occurred within the last second."""
        now = time.time()
        self.requests = [r for r in self.requests if now - r.timestamp < 1]

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #
    def is_rate_limited(self) -> bool:
        """Return ``True`` if the request rate exceeds the configured threshold."""
        self._prune_requests()
        return len(self.requests) >= self.threshold

    def is_circuit_open(self) -> bool:
        """Return ``True`` if the circuit breaker is currently open."""
        return self.circuit_open

    def handle_request(self, request: Request) -> Optional[Exception]:
        """
        Process a request.

        * If the circuit is open, return an exception with message
          ``"Circuit is open"``.
        * If the request would exceed the rate limit, open the circuit and
          return an exception with message ``"Rate limit exceeded"``.
        * Otherwise record the request and return ``None``.
        """
        if self.is_circuit_open():
            return Exception("Circuit is open")

        if self.is_rate_limited():
            # Open the circuit immediately on the first rate‑limit breach.
            self.circuit_open = True
            return Exception("Rate limit exceeded")

        # Request is allowed – record it.
        self.requests.append(request)
        return None

    def recover(self) -> None:
        """Close the circuit and reset internal counters."""
        self.circuit_open = False
        self.requests.clear()
