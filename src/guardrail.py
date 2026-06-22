import json
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class APIKey:
    key: str
    service: str
    status: str = "protected"

class Guardrail:
    def __init__(self):
        self.api_keys = {}

    def register_api_key(self, key: str, service: str) -> None:
        if key in self.api_keys:
            raise ValueError("API key already registered")
        self.api_keys[key] = APIKey(key, service)

    def validate_connectivity(self, key: str) -> bool:
        # Simulate connectivity validation
        return key in self.api_keys

    def monitor_api_key(self, key: str) -> None:
        if key not in self.api_keys:
            raise ValueError("API key not registered")
        self.api_keys[key].status = "active"

    def get_api_key_status(self, key: str) -> str:
        if key not in self.api_keys:
            raise ValueError("API key not registered")
        return self.api_keys[key].status

    def to_json(self) -> str:
        data = {
            "api_keys": [
                {"key": key, "service": api_key.service, "status": api_key.status}
                for key, api_key in self.api_keys.items()
            ]
        }
        return json.dumps(data)
