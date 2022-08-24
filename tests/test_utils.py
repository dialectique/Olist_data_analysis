"""
test utils.py from olistpackage
"""

import pandas as pd
from olistpackage.utils import ping, main


def test_ping():
    assert ping() == "PONG"

def test_main():
    assert main() == None
