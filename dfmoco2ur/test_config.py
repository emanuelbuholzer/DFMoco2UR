import  pytest
from dfmoco2ur.config import Configuration


def test_given_value():
    config = Configuration({"ur": { "hans": "192.168.5.42" }})
    ur_host = config.get("ur.hans")
    assert ur_host == "192.168.5.42"


def test_hard_coded_value():
    config = Configuration({})
    ur_host = config.get("ur.host")
    assert ur_host == "192.168.5.42"

def test_array_without_string_name():
    va = {"va": 1 }
    bla = {"bla": 2 }
    config = Configuration({ "hal": [va, bla]})
    va = config.get("hal.0.va")
    assert va == 1

def test_parent_access():
    config = Configuration({ "hal": { "va": 1, "bla": 2 }}) 
    hal = config.get("hal")
    print(hal)
    assert hal == { "va": 1, "bla": 2 }


def test_key_not_found():
    with pytest.raises(AttributeError):
        config = Configuration({})
        config.get("halli.galli")