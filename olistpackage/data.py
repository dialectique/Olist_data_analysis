import os
import pandas as pd
import opendatasets
import shutil

class Olist:
    """
    A class to access the Olist dataset version 2 from www.kaggle.com
    """

    def root_absolute_path(self) -> str:
        """
        return the absolute path of the root directory
        """
        # absolute path of the current directory
        dir = os.path.dirname(os.path.abspath(__file__))
        # absolute path of the root directory
        return os.path.dirname(os.path.abspath(dir))


    def csv_path(self) -> str:
        """
        return the absolute path of the olist csv files directory
        which is root/data/csv
        :return: the absolute path of the directory
        :rtype: str
        """
        # absolute path of the root directory
        root_dir = self.root_absolute_path()
        # absolute path of the olist csv files directory
        return os.path.join(root_dir, "data", "csv")


    def csv_files_exist(self) -> bool:
        """
        Check if the root/data/csv directory contains all the csv files
        :return: True if all the files exists else False
        :rtype: bool
        """
        # get the absolute path of the csv files directory
        csv_path = self.csv_path()
        # list of the csv files
        csv_files_names = [
            "olist_customers_dataset.csv",
            "olist_geolocation_dataset.csv",
            "olist_order_items_dataset.csv",
            "olist_order_payments_dataset.csv",
            "olist_order_reviews_dataset.csv",
            "olist_orders_dataset.csv",
            "olist_products_dataset.csv",
            "olist_sellers_dataset.csv",
            "product_category_name_translation.csv"
        ]
        # list of the path for each csv files
        csv_files_paths = [os.path.join(csv_path, f) for f in csv_files_names]
        # True if all the files exists else False
        return all(map(os.path.exists, csv_files_paths))


    def download_data(self) -> None:
        """
        Return True if the Olist csv files already exist in root/data/csv directory.
        Else: download the csv files from the Kaggle Official API.
        Uses the Kaggle Official API for donwloading dataset from Kaggle.
        Kaggle Official API credentials are asked by opendatasets.download()
        Sign in to https://kaggle.com/, then click on your profile picture
        on the top right and select "My Account" from the menu.
        Scroll down to the "API" section and click "Create New API Token".
        This will download a file kaggle.json with the following contents:
        {"username":"YOUR_KAGGLE_USERNAME","key":"YOUR_KAGGLE_KEY"}

        :return: None

        """
        # Check if the csv files already exist
        if self.csv_files_exist():
            # return True if yes
            print("The Olist csv files are already downloaded.")

        # If the files don't exist already,
        # download the csv files from the Kaggle Official API
        # in a new directory named brazilian-ecommerce
        dataset_url = "https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/download?datasetVersionNumber=2"
        opendatasets.download(dataset_url)

        # Depending of where this function is called,
        # the path of brazilian-ecommerce can be located in different places

        # scan the folders and find the brazilian-ecommerce directory path
        for root, dirs, files in os.walk(self.root_absolute_path()):
            for dir in dirs:
                if os.path.split(dir)[-1] == "brazilian-ecommerce":
                    brazilian_ecommerce_path = dir

        # move the csv files from root/brazilian-ecommerce to root/data/csv
        source = brazilian_ecommerce_path
        destination = self.csv_path()
        for f in os.listdir(source):
            shutil.move(os.path.join(source, f), os.path.join(destination, f))

        # delete the root/brazilian-ecommerce directory
        shutil. rmtree(source)

        print("The Olist csv files are downloaded.")


    def get_data(self) -> dict:
        """
        Transfert the csv files from brazilian-ecommerce directory
        into a dictionary of dataframes
        :return: a Python dict of pandas dataframes from the Olist csv files
        :rtype: dict
        """
        # get the absolute path of the csv files directory
        csv_path = self.csv_path()

        # get the csv files names and store them in a dictionary
        file_names = [file for file in os.listdir(csv_path) if file.endswith(".csv")]
        key_names = [
            key_name.replace("olist_", "").replace("_dataset", "").replace(".csv", "")
            for key_name in file_names
        ]

        # Read the csv files into pandas dataframes and store them in a dictionary
        data = {
            k: pd.read_csv(os.path.join(csv_path, f))
            for k, f in zip(key_names, file_names)
        }
        return data


    def ping(self):
        """
        You call ping I return pong.
        """
        return "PONG"


def main():
    print("The library data.py has been ran directly.")


if __name__ == "__main__":
    main()
