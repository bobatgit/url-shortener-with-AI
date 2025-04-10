from typing import Optional, Any
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class URLCache:
    def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600):
        self.max_size = max_size
        self.ttl = ttl_seconds
        self.cache = {}
        self.access_times = {}
    
    def get(self, key: str) -> Optional[Any]:
        if key not in self.cache:
            return None
        
        if self._is_expired(key):
            self._remove(key)
            return None
        
        self.access_times[key] = datetime.utcnow()
        return self.cache[key]
    
    def set(self, key: str, value: Any) -> None:
        if len(self.cache) >= self.max_size:
            self._evict_oldest()
        
        self.cache[key] = value
        self.access_times[key] = datetime.utcnow()
    
    def _is_expired(self, key: str) -> bool:
        access_time = self.access_times.get(key)
        if not access_time:
            return True
        return (datetime.utcnow() - access_time) > timedelta(seconds=self.ttl)
    
    def _remove(self, key: str) -> None:
        self.cache.pop(key, None)
        self.access_times.pop(key, None)
    
    def _evict_oldest(self) -> None:
        if not self.access_times:
            return
        
        oldest_key = min(self.access_times.items(), key=lambda x: x[1])[0]
        self._remove(oldest_key)

# Global cache instance
url_cache = URLCache()