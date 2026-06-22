import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections import defaultdict

@dataclass
class EndpointTraffic:
    endpoint: str
    count: int
    baseline: int

class Guardrail:
    def __init__(self, thresholds):
        self.thresholds = thresholds
        self.traffic_data = defaultdict(list)

    def add_traffic(self, endpoint, count):
        self.traffic_data[endpoint].append((datetime.now(), count))

    def analyze_traffic(self):
        alerts = []
        for endpoint, traffic in self.traffic_data.items():
            baseline = self.thresholds.get(endpoint, {}).get('baseline', 0)
            threshold = self.thresholds.get(endpoint, {}).get('threshold', 150)
            rolling_window = self._get_rolling_window(traffic)
            if rolling_window and rolling_window > baseline * threshold / 100:
                alerts.append(EndpointTraffic(endpoint, rolling_window, baseline))
        return alerts

    def _get_rolling_window(self, traffic):
        now = datetime.now()
        rolling_window = [count for timestamp, count in traffic if (now - timestamp) < timedelta(minutes=5)]
        return sum(rolling_window) if rolling_window else 0

    def load_thresholds(self, json_data):
        self.thresholds = json.loads(json_data)

    def save_thresholds(self):
        return json.dumps(self.thresholds)
