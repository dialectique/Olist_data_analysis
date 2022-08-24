"""
test data.py from olistpackage
"""

from olistpackage.data import Olist, main

o = Olist()

def test_root_absolute_path():
    assert isinstance(o.root_absolute_path(), str)

def test_csv_path():
    assert isinstance(o.csv_path(), str)

def test_csv_files_exist():
    assert isinstance(o.csv_files_exist(), bool)

def test_download_data():
    assert o.download_data() == None

def test_get_data():
    assert len(o.get_data()) == 9

def test_ping():
    assert o.ping() == "PONG"

def test_main():
    assert main() == None
