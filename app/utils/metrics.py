from collections import defaultdict
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class MetricsCollector:
    def __init__(self):
        self.requests_total = 0
        self.urls_created = 0
        self.urls_expired = 0
        self.redirects = defaultdict(int)
        self.hourly_stats = defaultdict(int)
    
    def track_request(self):
        self.requests_total += 1
        current_hour = datetime.utcnow().strftime("%Y-%m-%d-%H")
        self.hourly_stats[current_hour] += 1
    
    def track_url_creation(self):
        self.urls_created += 1
    
    def track_url_expiry(self):
        self.urls_expired += 1
    
    def track_redirect(self, short_code: str):
        self.redirects[short_code] += 1
    
    def get_stats(self):
        current_hour = datetime.utcnow().strftime("%Y-%m-%d-%H")
        return {
            "total_requests": self.requests_total,
            "urls_created": self.urls_created,
            "urls_expired": self.urls_expired,
            "requests_this_hour": self.hourly_stats[current_hour],
            "top_redirects": dict(sorted(self.redirects.items(), key=lambda x: x[1], reverse=True)[:5])
        }

# Global metrics collector instance
metrics = MetricsCollector()