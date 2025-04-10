from prometheus_client import Counter, Histogram, Gauge, generate_latest
import time
from typing import Callable
from fastapi import Request, Response
from functools import wraps

# Define metrics
REQUESTS = Counter(
    "url_shortener_requests_total",
    "Total number of requests",
    ["method", "endpoint", "status"]
)

REQUESTS_LATENCY = Histogram(
    "url_shortener_request_latency_seconds",
    "Request latency in seconds",
    ["method", "endpoint"]
)

ACTIVE_URLS = Gauge(
    "url_shortener_active_urls",
    "Number of active (non-expired) URLs"
)

REDIRECTS = Counter(
    "url_shortener_redirects_total",
    "Total number of URL redirects",
    ["short_code"]
)

async def metrics_middleware(request: Request, call_next: Callable):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    REQUESTS.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    REQUESTS_LATENCY.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)
    
    return response

def track_redirect(short_code: str):
    REDIRECTS.labels(short_code=short_code).inc()

def update_active_urls_count(count: int):
    ACTIVE_URLS.set(count)

def get_metrics():
    return Response(
        generate_latest(),
        media_type="text/plain"
    )