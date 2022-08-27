"""
test products.py from olistpackage
"""
import pandas as pd
from olistpackage.product import Product, main

p = Product()

# test get_product_features()
def test_type_get_product_features():
    assert isinstance(p.get_product_features(), pd.core.frame.DataFrame)
def test_len_get_product_features():
    assert len(p.get_product_features().columns) == 9
def test_columns_get_product_features():
    columns = ['product_id', 'category', 'product_name_length',
       'product_description_length', 'product_photos_qty', 'product_weight_g',
       'product_length_cm', 'product_height_cm', 'product_width_cm']
    for c in columns:
        assert c in p.get_product_features()

# test get_price()
def test_type_get_price():
    assert isinstance(p.get_price(), pd.core.frame.DataFrame)
def test_len_get_price():
    assert len(p.get_price().columns) == 2
def test_columns_get_price():
    columns = ['product_id', 'price']
    for c in columns:
        assert c in p.get_price()

# test get_wait_time()
def test_type_get_wait_time():
    assert isinstance(p.get_wait_time(), pd.core.frame.DataFrame)
def test_len_get_wait_time():
    assert len(p.get_wait_time().columns) == 2
def test_columns_get_wait_time():
    columns = ['product_id', 'wait_time']
    for c in columns:
        assert c in p.get_wait_time()

# test get_quantity()
def test_type_get_quantity():
    assert isinstance(p.get_quantity(), pd.core.frame.DataFrame)
def test_len_get_quantity():
    assert len(p.get_quantity().columns) == 3
def test_columns_get_quantity():
    columns = ['product_id', 'n_orders', 'quantity']
    for c in columns:
        assert c in p.get_quantity()

# test get_sales()
def test_type_get_sales():
    assert isinstance(p.get_sales(), pd.core.frame.DataFrame)
def test_len_get_sales():
    assert len(p.get_sales().columns) == 2
def test_columns_get_sales():
    columns = ['product_id', 'sales']
    for c in columns:
        assert c in p.get_sales()

# test get_review_score()
def test_type_get_review_score():
    assert isinstance(p.get_review_score(), pd.core.frame.DataFrame)
def test_len_get_review_score():
    assert len(p.get_review_score().columns) == 5
def test_columns_get_review_score():
    columns = ['product_id', 'share_of_five_stars', 'share_of_one_stars',
        'review_score', 'cost_of_reviews']
    for c in columns:
        assert c in p.get_review_score()

# test get_training_data()
def test_type_get_training_data():
    assert isinstance(p.get_training_data(), pd.core.frame.DataFrame)
def test_len_get_training_data():
    assert len(p.get_training_data().columns) == 20
def test_columns_get_training_data():
    columns = ['product_id', 'product_name_length', 'product_description_length',
        'product_photos_qty', 'product_weight_g', 'product_length_cm',
        'product_height_cm', 'product_width_cm', 'category', 'wait_time',
        'price', 'share_of_one_stars', 'share_of_five_stars', 'review_score',
        'cost_of_reviews', 'n_orders', 'quantity', 'sales', 'revenues',
        'profits']
    for c in columns:
        assert c in p.get_training_data()

# test get_product_cat()
def test_type_get_product_cat():
    assert isinstance(p.get_product_cat(), pd.core.frame.DataFrame)
def test_len_get_product_cat():
    assert len(p.get_product_cat().columns) == 18
def test_columns_get_product_cat():
    columns = ['product_name_length', 'product_description_length',
       'product_photos_qty', 'product_weight_g', 'product_length_cm',
       'product_height_cm', 'product_width_cm', 'wait_time', 'price',
       'share_of_one_stars', 'share_of_five_stars', 'review_score',
       'cost_of_reviews', 'n_orders', 'quantity', 'sales', 'revenues',
       'profits']
    for c in columns:
        assert c in p.get_product_cat()
def test_type_get_product_cat_with_median():
    assert isinstance(p.get_product_cat("median"), pd.core.frame.DataFrame)
def test_len_get_product_cat_with_median():
    assert len(p.get_product_cat("median").columns) == 18
def test_columns_get_product_cat_with_median():
    columns = ['product_name_length', 'product_description_length',
       'product_photos_qty', 'product_weight_g', 'product_length_cm',
       'product_height_cm', 'product_width_cm', 'wait_time', 'price',
       'share_of_one_stars', 'share_of_five_stars', 'review_score',
       'cost_of_reviews', 'n_orders', 'quantity', 'sales', 'revenues',
       'profits']
    for c in columns:
        assert c in p.get_product_cat("median")

def test_ping():
    assert p.ping() == "PONG"


def test_main():
    assert main() == None
