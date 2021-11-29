import prometheus_client
import time

from flask import request, Response
from prometheus_client import Counter, Histogram

registry = prometheus_client.CollectorRegistry()

REQUEST_COUNT = Counter('request_count', 'App Request Count',
                        ['method', 'endpoint', 'http_status'])

REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request Latency',
                            ['endpoint'])


def start_timer():
    request.start_time = time.time()


def stop_timer(response):
    resp_time = time.time() - request.start_time
    REQUEST_LATENCY.labels(request.path).observe(resp_time)
    return response


def record_request_data(response):
    REQUEST_COUNT.labels(request.method, request.path,
                         response.status_code).inc()
    return response

CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')


def setup(app):
    app.before_request(start_timer)
    app.after_request(record_request_data)
    app.after_request(stop_timer)
