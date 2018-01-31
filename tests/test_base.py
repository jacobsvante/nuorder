import gzip
import subprocess

import pytest
import responses

from nuorder import NuOrder


@pytest.mark.parametrize('cmd', [
    ['nuorder'],
    ['nuorder', 'get'],
])
def test_entry_point_runnable(cmd):
    proc = subprocess.run(cmd + ['-h'], stdout=subprocess.PIPE)
    assert b'usage: ' in proc.stdout


def test_get_request(default_nuorder_kw):
    nu = NuOrder(**default_nuorder_kw)
    with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
        rsps.add(
            responses.GET,
            'https://wholesale.sandbox1.nuorder.com/api/products/season/fw17/list',
            body='["product1"]',
        )
        data = nu.get('/api/products/season/fw17/list')
        assert data == ["product1"]


def test_post_request(default_nuorder_kw):
    nu = NuOrder(**default_nuorder_kw)

    def request_callback(request):
        return (201, {}, request.body)

    with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
        rsps.add_callback(
            responses.POST,
            'https://wholesale.sandbox1.nuorder.com/api/product/product2',
            callback=request_callback,
            content_type='application/json',
        )
        data = nu.post(
            '/api/product/product2',
            {'name': 'My product', 'style_number': '12345'},
        )
        assert data == {'name': 'My product', 'style_number': '12345'}


def test_post_request_gzipped(default_nuorder_kw):
    nu = NuOrder(**default_nuorder_kw)

    def request_callback(request):
        return (201, {}, gzip.decompress(request.body))

    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add_callback(
            responses.POST,
            'https://wholesale.sandbox1.nuorder.com/api/product/product3',
            callback=request_callback,
            content_type='application/json',
        )
        args = [
            '/api/product/product3',
            '{"name": "L33T product", "style_number": "1337"}',
        ]
        data = nu.post(*args, gzip_data=True)
        assert data == {"name": "L33T product", "style_number": "1337"}
