"""
test seller.py from olistpackage
"""
import pandas as pd
from olistpackage.seller import Seller, main

s = Seller()

# test get_seller_features()
def test_type_get_seller_features():
    assert isinstance(s.get_seller_features(), pd.core.frame.DataFrame)
def test_len_get_seller_features():
    assert len(s.get_seller_features().columns) == 3
def test_columns_get_seller_features():
    columns = ['seller_id', 'seller_city', 'seller_state']
    for c in columns:
        assert c in s.get_seller_features()

# test get_seller_delay_wait_time()
def test_type_get_seller_delay_wait_time():
    assert isinstance(s.get_seller_delay_wait_time(), pd.core.frame.DataFrame)
def test_len_get_seller_delay_wait_time():
    assert len(s.get_seller_delay_wait_time().columns) == 3
def test_columns_get_seller_delay_wait_time():
    columns = ['seller_id', 'delay_to_carrier', 'wait_time']
    for c in columns:
        assert c in s.get_seller_delay_wait_time()

# test get_active_dates()
def test_type_get_active_dates():
    assert isinstance(s.get_active_dates(), pd.core.frame.DataFrame)
def test_len_get_active_dates():
    assert len(s.get_active_dates().columns) == 4
def test_columns_get_active_dates():
    columns = ['seller_id', 'date_first_sale', 'date_last_sale', 'months_on_olist']
    for c in columns:
        assert c in s.get_active_dates()

# test get_quantity()
def test_type_get_quantity():
    assert isinstance(s.get_quantity(), pd.core.frame.DataFrame)
def test_len_get_quantity():
    assert len(s.get_quantity().columns) == 4
def test_columns_get_quantity():
    columns = ['seller_id', 'n_orders', 'quantity', 'quantity_per_order']
    for c in columns:
        assert c in s.get_quantity()

# test get_sales()
def test_type_get_sales():
    assert isinstance(s.get_sales(), pd.core.frame.DataFrame)
def test_len_get_sales():
    assert len(s.get_sales().columns) == 2
def test_columns_get_sales():
    columns = ['seller_id', 'sales']
    for c in columns:
        assert c in s.get_sales()

# test get_review_score()
def test_type_get_review_score():
    assert isinstance(s.get_review_score(), pd.core.frame.DataFrame)
def test_len_get_review_score():
    assert len(s.get_review_score().columns) == 5
def test_columns_get_review_score():
    columns = ['seller_id', 'share_of_five_stars', 'share_of_one_stars',
               'review_score', 'cost_of_reviews']
    for c in columns:
        assert c in s.get_review_score()

# test get_training_data()
def test_type_get_training_data():
    assert isinstance(s.get_training_data(), pd.core.frame.DataFrame)
def test_len_get_training_data():
    assert len(s.get_training_data().columns) == 18
def test_columns_get_training_data():
    columns = ['seller_id', 'seller_city', 'seller_state', 'delay_to_carrier',
        'wait_time', 'date_first_sale', 'date_last_sale', 'months_on_olist',
        'share_of_one_stars', 'share_of_five_stars', 'review_score',
        'cost_of_reviews', 'n_orders', 'quantity', 'quantity_per_order',
        'sales', 'revenues', 'profits']
    for c in columns:
        assert c in s.get_training_data()


def test_ping():
    assert s.ping() == "PONG"


def test_main():
    assert main() == None
