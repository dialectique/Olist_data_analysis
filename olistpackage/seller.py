import pandas as pd
import numpy as np

from olistpackage.data import Olist
from olistpackage.order import Order


class Seller:
    """
    DataFrames containing all sellers
    and various properties of these sellers as columns
    """

    def __init__(self):
        # Import data only once
        olist = Olist()
        self.data = olist.get_data()
        self.order = Order()

    def get_seller_features(self) -> pd.core.frame.DataFrame:
        """
        Returns a DataFrame with the following columns:
        seller_id, seller_city, seller_state
        :return: a DataFrame with the specified columns
        :rtype: pd.core.frame.DataFrame
        """
        # copy of sellers dataframe
        sellers = self.data['sellers'].copy()
        # remove the unwanted column and remove multiple rows per seller
        return sellers.drop('seller_zip_code_prefix', axis=1).drop_duplicates()


    def get_seller_delay_wait_time(self)-> pd.core.frame.DataFrame:
        """
        Returns a DataFrame with the following columns:
        seller_id, delay_to_carrier, wait_time
        :return: a DataFrame with the specified columns
        :rtype: pd.core.frame.DataFrame
        """
        # copy of order_items and orders dataframes
        order_items = self.data['order_items'].copy()
        orders = self.data['orders'].query("order_status=='delivered'").copy()

        # merge order_item and orders dataframes
        ship = order_items.merge(orders, on='order_id')

        # convert dates to datetime type
        for col in ['shipping_limit_date',
                    'order_delivered_carrier_date',
                    'order_delivered_customer_date',
                    'order_purchase_timestamp']:
            ship.loc[:, col] = pd.to_datetime(ship[col])

        # compute delay_to_carrier
        def delay_to_logistic_partner(df):
            days = np.mean(
                (df.order_delivered_carrier_date - df.shipping_limit_date) /
                np.timedelta64(24, 'h'))
            return days if days > 0 else 0

        delay = ship.groupby('seller_id')\
                    .apply(delay_to_logistic_partner)\
                    .reset_index()
        delay.columns = ['seller_id', 'delay_to_carrier']

        # compute wait_time
        def order_wait_time(df):
            return np.mean(
                (df.order_delivered_customer_date - df.order_purchase_timestamp)
                / np.timedelta64(24, 'h'))

        wait = ship.groupby('seller_id')\
                   .apply(order_wait_time)\
                   .reset_index()
        wait.columns = ['seller_id', 'wait_time']

        # return delay dataframe merged with wait dataframe
        return delay.merge(wait, on='seller_id')


    def get_active_dates(self) -> pd.core.frame.DataFrame:
        """
        Returns a DataFrame with the following columns:
        seller_id, date_first_sale, date_last_sale, months_on_olist
        :return: a DataFrame with the specified columns
        :rtype: pd.core.frame.DataFrame
        """
        # get a df with order_id, order_approved_at
        # from orders dataframe, only for orders that are approved
        orders_approved = self.data['orders'][['order_id', 'order_approved_at']]
        orders_approved.dropna()

        # create a orders - sellers join table
        # because a seller can appear multiple times in the same order
        orders_sellers = orders_approved \
            .merge(self.data['order_items'], on='order_id')[[
                'order_id', 'seller_id','order_approved_at']]
        orders_sellers.drop_duplicates()
        orders_sellers["order_approved_at"] = pd.to_datetime(
            orders_sellers["order_approved_at"])

        # Compute dates and return the wanted dataframe
        orders_sellers["date_first_sale"] = orders_sellers["order_approved_at"]
        orders_sellers["date_last_sale"] = orders_sellers["order_approved_at"]
        df = orders_sellers.groupby('seller_id').agg({
            "date_first_sale": min,
            "date_last_sale": max
        })
        df['months_on_olist'] = round(
            (df['date_last_sale'] - df['date_first_sale']) /
            np.timedelta64(1, 'M'))
        return df.reset_index()


    def get_quantity(self) -> pd.core.frame.DataFrame:
        """
        Returns a DataFrame with the following columns:
        seller_id, n_orders, quantity, quantity_per_order
        :return: a DataFrame with the specified columns
        :rtype: pd.core.frame.DataFrame
        """
        # get order_items dataframe
        order_items = self.data['order_items']

        # compute the number of orders per seller
        n_orders = order_items.groupby('seller_id')['order_id']\
            .nunique()\
            .reset_index()
        n_orders.columns = ['seller_id', 'n_orders']

        # compute the number of products per seller
        quantity = order_items.groupby('seller_id', as_index=False).agg(
            {'order_id': 'count'})
        quantity.columns = ['seller_id', 'quantity']

        # compute and return the wanted dataframe
        df = n_orders.merge(quantity, on='seller_id')
        df['quantity_per_order'] = df['quantity'] / df['n_orders']
        return df


    def get_sales(self) -> pd.core.frame.DataFrame:
        """
        Returns a DataFrame with the following columns:
        seller_id, sales
        :return: a DataFrame with the specified columns
        :rtype: pd.core.frame.DataFrame
        """
        # compute and return the total sales per seller
        return self.data['order_items'][['seller_id', 'price']]\
            .groupby('seller_id')\
            .sum()\
            .rename(columns={'price': 'sales'}).reset_index()


    def get_review_score(self) -> pd.core.frame.DataFrame:
        """
        Returns a DataFrame with the following columns:
        seller_id, share_of_five_stars, share_of_one_stars,
        review_score, cost_of_reviews
        :return: a DataFrame with the specified columns
        :rtype: pd.core.frame.DataFrame
        """
        # get the order_reviews dataframe from order librairy
        orders_reviews = self.order.get_review_score()
        # get all the sellers for each order
        orders_sellers = self.data['order_items'][['order_id', 'seller_id'
                                                   ]].drop_duplicates()
        # merge the orders_seller and order_reviews dataframes
        df = orders_sellers.merge(orders_reviews, on='order_id')

        # compute the estimated cost_of_review column
        # according to the following:
        # score |  1  |  2  |  3  |  4  |  5
        # ------+-----+-----+-----+-----+-----
        # cost  | 100 |  50 |  40 |  0  |  0
        df['cost_of_review'] = df.review_score.map({
            1: 100, 2: 50, 3: 40, 4: 0, 5: 0
        })
        # compute for each seller the following means and sum
        df_grouped_by_sellers = df.groupby('seller_id', as_index=False).agg({
            'dim_is_one_star': 'mean',
            'dim_is_five_star': 'mean',
            'review_score': 'mean',
            'cost_of_review': 'sum'
        })
        # set column labels and return the wanted dataframe
        df_grouped_by_sellers.columns = [
            'seller_id', 'share_of_one_stars', 'share_of_five_stars',
            'review_score', 'cost_of_reviews'
        ]

        return df_grouped_by_sellers


    def get_training_data(self) -> pd.core.frame.DataFrame:
        """
        Returns a DataFrame with with the following columns:
        seller_id, seller_city, seller_state, delay_to_carrier,
        wait_time, date_first_sale, date_last_sale, months_on_olist,
        share_of_one_stars, share_of_five_stars, review_score,
        cost_of_reviews, n_orders, quantity, quantity_per_order,
        sales, revenues, profits
        :return: a DataFrame with the specified columns
        :rtype: pd.core.frame.DataFrame
        """
        # merge the dataframes from the previous methods of this class
        training_df =\
            self.get_seller_features()\
                .merge(
                    self.get_seller_delay_wait_time(), on='seller_id'
                ).merge(
                    self.get_active_dates(), on='seller_id'
                ).merge(
                    self.get_review_score(), on='seller_id'
                ).merge(
                    self.get_quantity(), on='seller_id'
                ).merge(
                self.get_sales(), on='seller_id'
                )

        # add seller economics (revenues, profits)
        olist_monthly_fee = 80
        olist_sales_cut = 0.1

        training_df['revenues'] = training_df['months_on_olist'] * olist_monthly_fee\
            + olist_sales_cut * training_df['sales']

        training_df['profits'] = training_df['revenues'] - training_df[
            'cost_of_reviews']

        return training_df


    def ping(self):
        """
        You call ping I return pong.
        """
        return "PONG"


def main():
    print("The library seller.py has been ran directly.")


if __name__ == "__main__":
    main()
