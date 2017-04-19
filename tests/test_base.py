import gzip
import subprocess

import pytest
import responses

import nuorder


@pytest.mark.parametrize('cmd', [
    ['nuorder'],
    ['nuorder', 'get'],
])
def test_entry_point_runnable(cmd):
    proc = subprocess.run(cmd + ['-h'], stdout=subprocess.PIPE)
    assert b'usage: ' in proc.stdout


def test_get_request():
    with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
        rsps.add(
            responses.GET,
            'https://wholesale.sandbox1.nuorder.com/api/products/season/fw17/list',
            body='["product1"]',
        )
        data = nuorder.request(
            method='GET',
            endpoint='/api/products/season/fw17/list',
            hostname='wholesale.sandbox1.nuorder.com',
        )
        assert data == ["product1"]


def test_post_request():
    def request_callback(request):
        return (201, {}, request.body)

    with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
        rsps.add_callback(
            responses.POST,
            'https://wholesale.sandbox1.nuorder.com/api/product/product2',
            callback=request_callback,
            content_type='application/json',
        )
        data = nuorder.request(
            method='POST',
            endpoint='/api/product/product2',
            hostname='wholesale.sandbox1.nuorder.com',
            data='{"name": "My product", "style_number": "12345"}'
        )
        assert data == {"name": "My product", "style_number": "12345"}


def test_post_request_gzipped():
    def request_callback(request):
        return (201, {}, gzip.decompress(request.body))

    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add_callback(
            responses.POST,
            'https://wholesale.sandbox1.nuorder.com/api/product/product3',
            callback=request_callback,
            content_type='application/json',
        )
        kwargs = dict(
            method='POST',
            endpoint='/api/product/product3',
            hostname='wholesale.sandbox1.nuorder.com',
            data='{"name": "L33T product", "style_number": "1337"}',
        )
        data = nuorder.request(**kwargs, gzip_data=True)
        assert data == {"name": "L33T product", "style_number": "1337"}

        with pytest.raises(OSError) as exception_info:
            data = nuorder.request(**kwargs)
        assert 'Not a gzipped file' in str(exception_info.value)
