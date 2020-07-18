"""
Functions for if you need to dummy up data for testing purposes.
"""
import json
import pytest

@pytest.fixture
def conversations_list():
    data = {

    }
    return json.dumps(data)

@pytest.fixture
def conversations_