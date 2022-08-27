## Olist_data_analysis - notebooks

Analyze a dataset provided by Brazilian e-commerce marketplace [Olist](https://www.olist.com).

"Olist dataset version 2" is available on Kaggle:
https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/download?datasetVersionNumber=2

This folder contains notebooks that analyse the cleaned data provided by the olistpackage.

### exploratory_analysis.ipynb
Exploratory analysis of the Olist cleaned data:
- original dataset descritption
- original dataset download and data cleansing
- automated exploratory analysis with SweetViz
- cardinalities

### orders_analysis
Get an understanding of the `orders properties` and their associated `review_scores`
- import the dataset from the olistpackage, description of the dataset
- inspect features
- Simple regression of `review_score` against `delivery duration`
- Multivariate regression

### seller_analysis
Get an understanding of the `sellers properties` and their associated `review_scores`
Find sellers who have repeatedly been underperforming vs. others, and understand why.
- import the dataset from the olistpackage, description of the dataset
- Impact of various features on `review_score` using a `multivariate-OLS` in `statsmodels`
- `seller_state` analysis


### products_analysis
Get an understanding of the `products properties` and their associated `review_scores`
Find `product categories` that repeatedly `underperform` vs. others, and understand the reasons behind.
- import the dataset from the olistpackage, description of the dataset
- Impact of various features on `review_score` using a `multivariate-OLS` in `statsmodels`
work in progress
