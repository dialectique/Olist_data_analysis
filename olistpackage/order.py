import pandas as pd
import numpy as np
from haversine import haversine

from olistpackage.data import Olist


class Order:
    """
    DataFrames containing all orders
    and various properties of these orders as columns
    """

    def __init__(self):
        """
        Attribute "data" : dict of dataframes (from Olist csv files)
        """
        self.data = Olist().get_data()


    def get_wait_time(self, is_delivered: bool = True) -> pd.core.frame.DataFrame:
        """
        Returns a DataFrame with the following columns:
        order_id, wait_time, expected_wait_time, delay_vs_expected, order_status
        and filters out non-delivered orders unless specified
        :param is_delivered: if True, filters out non-delivered orders
        :type is_delivered: bool
        :return: a DataFrame with the specified columns
        :rtype: pd.core.frame.DataFrame
        """
        # create a copy of the "orders" dataframe
        orders = self.data['orders'].copy()

        # filter delivered orders if is_delivered is True
        if is_delivered:
            orders = orders.query("order_status == 'delivered'").copy()

        # Convert dates from str to pandas.datetime
        columns = [
        "order_purchase_timestamp",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
        ]
        for c in columns:
            orders.loc[:, c] = pd.to_datetime(orders[c])

        # Compute wait_time, expected_wait_time and delay_vs_expected, in days
        one_day_delta = np.timedelta64(24, 'h')
        orders.loc[:, 'wait_time'] = \
            (orders['order_delivered_customer_date'] -
             orders['order_purchase_timestamp']) / one_day_delta
        orders.loc[:, 'expected_wait_time'] = \
            (orders['order_estimated_delivery_date'] -
             orders['order_purchase_timestamp']) / one_day_delta
        orders.loc[:, 'delay_vs_expected'] = \
            (orders['order_delivered_customer_date'] -
             orders['order_estimated_delivery_date']) / one_day_delta

        # Set negative values to zero
        orders.loc[:,'delay_vs_expected'] = orders['delay_vs_expected'].clip(0)

        # Return the following dataframe
        return orders[['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected', 'order_status']]


    def get_review_score(self) -> pd.core.frame.DataFrame:
        """
        Returns a DataFrame with the following columns:
        order_id, dim_is_five_star, dim_is_one_star, review_score
        :return: a DataFrame with the specified columns
        :rtype: pd.core.frame.DataFrame
        """
        reviews = self.data['order_reviews'].copy()
        reviews['dim_is_five_star'] = (reviews['review_score'] == 5) * 1
        reviews['dim_is_one_star'] = (reviews['review_score'] == 1) * 1
        return reviews[['order_id', 'dim_is_five_star', 'dim_is_one_star', 'review_score']]


    def get_number_products(self) -> pd.core.frame.DataFrame:
        """
        Returns a DataFrame with the following columns:
        order_id, number_of_products
        :return: a DataFrame with the specified columns
        :rtype: pd.core.frame.DataFrame
        """
        items = self.data['order_items'].copy()
        items = items.groupby('order_id').count().product_id.reset_index()
        return items.rename(columns = {'product_id': 'number_of_products'})


    def get_number_sellers(self) -> pd.core.frame.DataFrame:
        """
        Returns a DataFrame with the following columns:
        order_id, number_of_sellers
        :return: a DataFrame with the specified columns
        :rtype: pd.core.frame.DataFrame
        """
        items = self.data['order_items'].copy()
        nb_sellers = items.groupby("order_id")['seller_id'].nunique().reset_index()
        return nb_sellers.rename(columns = {'seller_id': 'number_of_sellers'})


    def get_price_and_freight(self) -> pd.core.frame.DataFrame:
        """
        Returns a DataFrame with the following columns:
        order_id, price, freight_value
        :return: a DataFrame with the specified columns
        :rtype: pd.core.frame.DataFrame
        """
        order_items = self.data['order_items'].copy()
        return order_items.groupby('order_id')[['price', 'freight_value']].sum().reset_index()


    def get_distance_seller_customer(self) -> pd.core.frame.DataFrame:
        """
        Returns a DataFrame with the following columns:
        order_id, distance_seller_customer
        :return: a DataFrame with the specified columns
        :rtype: pd.core.frame.DataFrame
        """

        # import data
        data = self.data
        orders = data['orders']
        order_items = data['order_items']
        sellers = data['sellers']
        customers = data['customers']
        geo = data['geolocation']

        # Since one zip code can map to multiple (lat, lng), take the first one
        geo = data['geolocation']
        geo = geo.groupby('geolocation_zip_code_prefix',
                          as_index=False).first()

        # Merge geo_location for sellers
        columns = [
            'seller_id', 'seller_zip_code_prefix', 'geolocation_lat', 'geolocation_lng'
        ]
        sellers_geoloc = sellers.merge(
            geo,
            how='left',
            left_on='seller_zip_code_prefix',
            right_on='geolocation_zip_code_prefix')[columns]

        # Merge geo_location for customers
        columns = [
            'customer_id', 'customer_zip_code_prefix', 'geolocation_lat', 'geolocation_lng'
            ]
        customers_geoloc = customers.merge(
            geo,
            how='left',
            left_on='customer_zip_code_prefix',
            right_on='geolocation_zip_code_prefix')[columns]

        # Match customers with sellers in one table
        columns = [
            'order_id', 'customer_id','customer_zip_code_prefix', 'seller_id', 'seller_zip_code_prefix'
        ]
        customers_and_sellers = customers.merge(orders, on='customer_id')\
            .merge(order_items, on='order_id')\
            .merge(sellers, on='seller_id')[columns]

        # Add the geolocalisation from sellers_geoloc and customers_geoloc
        customers_and_sellers_geoloc = customers_and_sellers.merge(
            sellers_geoloc, on='seller_id'
            ).merge(customers_geoloc, on='customer_id', suffixes=('_seller', '_customer'))

        # remove na()
        customers_and_sellers_geoloc = customers_and_sellers_geoloc.dropna()

        # compute haversine distance in the distance_seller_customer column
        customers_and_sellers_geoloc.loc[:, "distance_seller_customer"] = \
            customers_and_sellers_geoloc.apply(
                lambda row: haversine((row['geolocation_lng_seller'],
                                       row['geolocation_lat_seller']),
                                        (row['geolocation_lng_customer'],
                                         row['geolocation_lat_customer'])),
                axis=1)

        # Since an order can have multiple sellers,
        # return the average of the distance per order
        return customers_and_sellers_geoloc.groupby('order_id', as_index=False)\
            .agg({'distance_seller_customer':'mean'})


    def get_training_data(self,
                          is_delivered=True,
                          with_distance_seller_customer=False):
        """
        Returns a clean DataFrame (without NaN), with the all following columns:
        order_id, wait_time, expected_wait_time, delay_vs_expected,
        order_status, dim_is_five_star, dim_is_one_star, review_score,
        number_of_products, number_of_sellers, price, freight_value,
        distance_seller_customer
        :param is_delivered: if True, filters out non-delivered orders
        :type is_delivered: bool
        :param with_distance_seller_customer: if True, include the distance seller-customer
        :type with_distance_seller_customer: bool
        :return: a DataFrame with the specified columns
        :rtype: pd.core.frame.DataFrame
        """
        training_set =\
            self.get_wait_time(is_delivered)\
                .merge(
                self.get_review_score(), on='order_id'
            ).merge(
                self.get_number_products(), on='order_id'
            ).merge(
                self.get_number_sellers(), on='order_id'
            ).merge(
                self.get_price_and_freight(), on='order_id'
            )

        # Include the distance seller-customer
        # only if with_distance_seller_customer is True
        if with_distance_seller_customer:
            training_set = training_set.merge(
                self.get_distance_seller_customer(), on='order_id')

        return training_set.dropna()


    def ping(self):
        """
        You call ping I return pong.
        """
        return "PONG"


def main():
    print("The library order.py has been ran directly.")


if __name__ == "__main__":
    main()
