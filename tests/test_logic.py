import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "src"))
)
from models import Endpoint


def test_increment_on_success_status():
    endpoint = Endpoint(url="https://example.com", count=0)
    status_code = 201
    if 200 <= status_code < 300:
        endpoint.count += 1
    assert endpoint.count == 1


def test_no_increment_on_error_status():
    endpoint = Endpoint(url="https://example.com", count=5)
    status_code = 404
    if 200 <= status_code < 300:
        endpoint.count += 1
    assert endpoint.count == 5
