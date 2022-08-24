"""
test order.py from olistpackage
"""
import pandas as pd
from olistpackage.order import Order, main

o = Order()

# test get_wait_time() with no argument
def test_type_get_wait_time_no_argument():
    assert isinstance(o.get_wait_time(), pd.core.frame.DataFrame)

def test_len_get_wait_time_no_argument():
    assert len(o.get_wait_time()) == len(o.get_wait_time().query("order_status=='delivered'"))

def test_len_columns_get_wait_time_no_argument():
    assert len(o.get_wait_time().columns) == 5

def test_columns_get_wait_time_no_argument():
    for c in ['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected', 'order_status']:
        assert c in o.get_wait_time().columns


# test get_wait_time(is_delivered=True)
def test_type_get_wait_time_is_delivered_True():
    assert isinstance(o.get_wait_time(is_delivered=True), pd.core.frame.DataFrame)

def test_len_get_wait_time_is_delivered_True():
    assert len(o.get_wait_time(is_delivered=True)) == len(o.get_wait_time().query("order_status=='delivered'"))

def test_len_columns_get_wait_time_is_delivered_True():
    assert len(o.get_wait_time(is_delivered=True).columns) == 5

def test_columns_get_wait_time_is_delivered_True():
    for c in ['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected', 'order_status']:
        assert c in o.get_wait_time(is_delivered=True).columns


# test get_wait_time(is_delivered=False)
def test_type_get_wait_time_is_delivered_False():
    assert isinstance(o.get_wait_time(is_delivered=False), pd.core.frame.DataFrame)

def test_len_get_wait_time_is_delivered_False():
    assert len(o.get_wait_time(is_delivered=False)) != len(o.get_wait_time().query("order_status=='delivered'"))

def test_len_columns_get_wait_time_is_delivered_False():
    assert len(o.get_wait_time(is_delivered=False).columns) == 5

def test_columns_get_wait_time_is_delivered_False():
    for c in ['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected', 'order_status']:
        assert c in o.get_wait_time(is_delivered=False).columns


# test get_review_score()
def test_type_get_review_score():
    assert isinstance(o.get_review_score(), pd.core.frame.DataFrame)

def test_len_columns_get_review_score():
    assert len(o.get_review_score().columns) == 4

def test_columns_get_review_score():
    for c in ['order_id', 'dim_is_five_star', 'dim_is_one_star', 'review_score']:
        assert c in o.get_review_score()


# test get_number_products()
def test_type_get_number_products():
    assert isinstance(o.get_number_products(), pd.core.frame.DataFrame)

def test_len_columns_get_number_products():
    assert len(o.get_number_products().columns) == 2

def test_columns_get_number_products():
    for c in ['order_id', 'number_of_products']:
        assert c in o.get_number_products()


# test get_number_sellers():
def test_type_get_number_sellers():
    assert isinstance(o.get_number_sellers(), pd.core.frame.DataFrame)

def test_len_columns_get_number_sellers():
    assert len(o.get_number_sellers().columns) == 2

def test_columns_get_number_sellers():
    for c in ['order_id', 'number_of_sellers']:
        assert c in o.get_number_sellers()


# test get_price_and_freight()
def test_type_get_price_and_freight():
    assert isinstance(o.get_price_and_freight(), pd.core.frame.DataFrame)

def test_len_get_price_and_freight():
    assert len(o.get_price_and_freight().columns) == 3

def test_columns_get_price_and_freight():
    for c in ['order_id', 'price', 'freight_value']:
        assert c in o.get_price_and_freight()


# test get_distance_seller_customer()
def test_type_get_distance_seller_customer():
    assert isinstance(o.get_distance_seller_customer(), pd.core.frame.DataFrame)

def test_len_get_distance_seller_customer():
    assert len(o.get_distance_seller_customer().columns) == 2

def test_columns_get_distance_seller_customer():
    for c in ['order_id', 'distance_seller_customer']:
        assert c in o.get_distance_seller_customer()


# test get_training_data()
def test_type_get_training_data():
    assert isinstance(o.get_training_data(), pd.core.frame.DataFrame)

def test_len_get_training_data():
    assert len(o.get_training_data().columns) == 12

def test_columns_get_training_data():
    columns = ['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected',
    'order_status', 'dim_is_five_star', 'dim_is_one_star', 'review_score',
    'number_of_products', 'number_of_sellers', 'price', 'freight_value']
    for c in columns:
        assert c in o.get_training_data()

def test_len_get_training_data_with_distance_seller_customer():
    assert len(o.get_training_data(with_distance_seller_customer=True).columns) == 13

def test_columns_get_training_data_with_distance_seller_customer():
    columns = ['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected',
    'order_status', 'dim_is_five_star', 'dim_is_one_star', 'review_score',
    'number_of_products', 'number_of_sellers', 'price', 'freight_value',
    'distance_seller_customer']
    for c in columns:
        assert c in o.get_training_data(with_distance_seller_customer=True)


def test_ping():
    assert o.ping() == "PONG"


def test_main():
    assert main() == None
