from __future__ import annotations

import pytest

from virtualenv import cli_run
from virtualenv.info import IS_PYPY
from virtualenv.util.subprocess import run_cmd


@pytest.mark.skipif(IS_PYPY, reason="setuptools distutils patching does not work")
def test_app_data_pinning(tmp_path):
    version = "19.3.1"
    result = cli_run([str(tmp_path), "--pip", version, "--activators", "", "--seeder", "app-data"])
    code, out, _ = run_cmd([str(result.creator.script("pip")), "list", "--disable-pip-version-check"])
    assert not code
    for line in out.splitlines():
        parts = line.split()
        if parts and parts[0] == "pip":
            assert parts[1] == version
            break
    else:
        assert not out
