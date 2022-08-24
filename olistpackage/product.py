import pandas as pd
import numpy as np

from olistpackage.data import Olist
from olistpackage.order import Order


class Product:
    """
    DataFrames containing all products
    and various properties of these products as columns
    :return: a DataFrame with the specified columns
    :rtype: pd.core.frame.DataFrame

    """
    def __init__(self):
        # Import data only once
        olist = Olist()
        self.data = olist.get_data()
        self.order = Order()


    def get_product_features(self) -> pd.core.frame.DataFrame:
        """
        Returns a DataFrame with the following columns:
        product_id, category, product_name_length,
        product_description_length, product_photos_qty, product_weight_g,
        product_length_cm, product_height_cm, product_width_cm
        :return: a DataFrame with the specified columns
        :rtype: pd.core.frame.DataFrame
        """
        products = self.data['products']

        # convert name to English
        en_category = self.data['product_category_name_translation']
        df = products.merge(en_category, on='product_category_name')
        df.drop(['product_category_name'], axis=1, inplace=True)
        # rename columns, fix typo: lenght -> length
        # and return the wanted dataframe
        df.rename(columns={
            'product_category_name_english': 'category',
            'product_name_lenght': 'product_name_length',
            'product_description_lenght': 'product_description_length'
        },
                  inplace=True)

        return df


    def get_price(self) -> pd.core.frame.DataFrame:
        """
        Return a DataFrame with the following columns:
        product_id, price
        :return: a DataFrame with the specified columns
        :rtype: pd.core.frame.DataFrame
        """
        # get the order_items dataframe
        order_items = self.data['order_items']
        # compute the mean price for each product
        # and return the wanted dataframe
        df =  order_items[['product_id', 'price']].groupby('product_id').mean()

        return df.reset_index()


    def get_wait_time(self) -> pd.core.frame.DataFrame:
        """
        Returns a DataFrame with the following columns:
        product_id, wait_time
        :return: a DataFrame with the specified columns
        :rtype: pd.core.frame.DataFrame
        """
        # get dataframe from get_wait_time() (order.py librairy)
        orders_wait_time = self.order.get_wait_time()
        # get a subset of order_items dataset and drop duplicates
        orders_products = self.data['order_items'][['order_id', 'product_id']]
        orders_products.drop_duplicates()
        # merge the two previous dataset
        orders_products_with_time = orders_products.merge(orders_wait_time, on='order_id')
        # compute the mean wait time for each product
        # and return the wanted dataframe
        df = orders_products_with_time.groupby('product_id', as_index=False) \
            .agg({'wait_time': 'mean'})

        return df


    def get_quantity(self) -> pd.core.frame.DataFrame:
        """
        Returns a DataFrame with the following columns:
        product_id, n_orders, quantity
        :return: a DataFrame with the specified columns
        :rtype: pd.core.frame.DataFrame
        """
        # get the order_items dataframe
        order_items = self.data['order_items']
        # compute the number of orders for each product in n_orders dataframe
        n_orders = order_items.groupby('product_id')['order_id'] \
            .nunique().reset_index()
        # rename columns
        n_orders.columns = ['product_id', 'n_orders']
        # compute the total quantity for each product in quantity dataframe
        quantity = order_items.groupby('product_id', as_index=False) \
            .agg({'order_id': 'count'})
        # rename columns
        quantity.columns = ['product_id', 'quantity']
        # merge the two previous dataframes
        # and return the wanted dataframe
        df = n_orders.merge(quantity, on='product_id')

        return df


    def get_sales(self) -> pd.core.frame.DataFrame:
        """
        Returns a DataFrame with the following columns:
        product_id, sales
        :return: a DataFrame with the specified columns
        :rtype: pd.core.frame.DataFrame
        """
        # compute the total sales for each product
        # and return the wanted dataframe
        df = self.data['order_items'][['product_id', 'price']]\
            .groupby('product_id')\
            .sum()\
            .rename(columns={'price': 'sales'})

        return df.reset_index()


    def get_review_score(self) -> pd.core.frame.DataFrame:
        """
        Returns a DataFrame with the following columns:
        product_id, share_of_five_stars, share_of_one_stars,
        review_score, cost_of_reviews
        :return: a DataFrame with the specified columns
        :rtype: pd.core.frame.DataFrame
        """
        # get dataframe from get_review_score() (order.py librairy)
        orders_reviews = self.order.get_review_score()
        # compute the product_id s for all the order_id
        # in order_products dataframe
        orders_products = self.data['order_items'] \
            [['order_id', 'product_id']].drop_duplicates()
        # merge the two previous dataframes
        df = orders_products.merge(orders_reviews, on='order_id')

        # compute the cost_of_review column
        # according to the following:
        # score |  1  |  2  |  3  |  4  |  5
        # ------+-----+-----+-----+-----+-----
        # cost  | 100 |  50 |  40 |  0  |  0
        df['cost_of_reviews'] = df.review_score.map({
            1: 100, 2: 50, 3: 40, 4: 0, 5: 0
        })
        # compute for each product the following means and sum
        df = df.groupby('product_id', as_index=False).agg({
            'dim_is_one_star': 'mean',
            'dim_is_five_star': 'mean',
            'review_score': 'mean',
            'cost_of_reviews': 'sum'
        })
        # set columns label and return the wanted dataframe
        df.columns = [
            'product_id', 'share_of_one_stars', 'share_of_five_stars',
            'review_score', 'cost_of_reviews'
        ]

        return df


    def get_training_data(self) -> pd.core.frame.DataFrame:
        """
        Returns a DataFrame with the following columns:
        product_id, product_name_length, product_description_length,
        product_photos_qty, product_weight_g, product_length_cm,
        product_height_cm, product_width_cm, category, wait_time,
        price, share_of_one_stars, share_of_five_stars, review_score,
        cost_of_reviews, n_orders, quantity, sales, revenues, profits
        :return: a DataFrame with the specified columns
        :rtype: pd.core.frame.DataFrame
        """
        # merge the dataframes from the previous methods of this class
        training_set =\
            self.get_product_features()\
                .merge(
                self.get_wait_time(), on='product_id'
               ).merge(
                self.get_price(), on='product_id'
               ).merge(
                self.get_review_score(), on='product_id'
               ).merge(
                self.get_quantity(), on='product_id'
               ).merge(
                self.get_sales(), on='product_id'
               )

        # compute the economics (revenues, profits)
        olist_sales_cut = 0.1
        training_set['revenues'] = olist_sales_cut * training_set['sales']
        training_set['profits'] = training_set['revenues'] - training_set[
            'cost_of_reviews']

        return training_set


    def get_product_cat(self, agg: str ="mean") -> pd.core.frame.DataFrame:
        '''
        Returns a DataFrame with category as index,
        and aggregating various properties for each category in columns such as:
        - quantity: total number of products sold for this category.
        - product_weight_g: mean or median weight per category, depending
        of the agg parameter
        - ...
        :param agg: function name
        :type agg: str
        :return: a DataFrame with the specified columns
        :rtype: pd.core.frame.DataFrame
        '''
        # get the training_data from the previous class method
        products = self.get_training_data()
        # list of columns for which dtype is not object
        columns = list(products.select_dtypes(exclude=['object']).columns)
        # set the aggregiate parameters
        agg_params = dict(zip(columns, [agg] * len(columns)))
        agg_params['quantity'] = 'sum'
        # compute and return the wanted dataframe
        df = products.groupby("category").agg(agg_params)

        return df


    def ping(self):
        """
        You call ping I return pong.
        """
        return "PONG"


def main():
    print("The library product.py has been ran directly.")


if __name__ == "__main__":
    main()
