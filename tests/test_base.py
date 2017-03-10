import subprocess

import pytest


@pytest.mark.parametrize('cmd', [
    ['nuorder'],
    ['nuorder', 'get'],
])
def test_entry_point_runnable(cmd):
    proc = subprocess.run(cmd + ['-h'], stdout=subprocess.PIPE)
    assert b'usage: ' in proc.stdout
