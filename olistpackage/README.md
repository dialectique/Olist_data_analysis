## Olist Classes

This folder contains Olist Classes that handle the logic of data cleaning for this project.

For example, the below returns data as a Python dictionary using the `get_data` method from the `Olist` class:

```python
from olistpackage.data import Olist
olist = Olist()
data = olist.get_data()
```

### Data

```python
from olistpackage.data import Olist
```

Main methods:

- `get_data`: returns all Olist datasets as DataFrames within a Python dict.

### Order

```python
from olistpackage.order import Order
```

Main method:
- `get_training_data`: returns a DataFrame with:
   - `order_id` (unique)
   - `wait_time`
   - `expected_wait_time`
   - `delay_vs_expected`
   -  `order_status`
   - `dim_is_five_star`
   - `dim_is_one_star`
   - `review_score`
   - `number_of_products`
   - `number_of_sellers`
   - `price`
   - `freight_value`
   - `distance_seller_customer`

### Seller

```python
from olistpackage.seller import Seller
```

Main method:
- `get_training_data`: returns a DataFrame with:
   - `seller_id` (unique)
   - `seller_city`
   - `seller_state`
   - `delay_to_carrier`
   - `wait_time`
   - `date_first_sale`
   - `date_last_sale`
   - `months_on_olist`
   - `share_of_one_stars`
   - `share_of_five_stars`
   - `review_score`
   - `cost_of_reviews`
   - `n_orders`
   - `quantity`
   - `quantity_per_order`
   - `sales`
   - `revenues`
   - `profits`

### Product

```python
from olistpackage.product import Product
```

Main method:
- `get_training_data`: returns a DataFrame with
   - `product_id` (unique)
   - `product_name_length`
   - `product_description_length`
   - `product_photos_qty`
   - `product_weight_g`
   - `product_length_cm`
   - `product_height_cm`
   - `product_width_cm`
   - `category`
   - `wait_time`
   - `price`
   - `share_of_one_stars`
   - `share_of_five_stars`
   - `review_score`
   - `cost_of_reviews`
   - `n_orders`
   - `quantity`
   - `sales`
   - `revenues`
   - `profits`

### Utils

Utility functions to help during the project.

```python
from olist.utils import *
```
