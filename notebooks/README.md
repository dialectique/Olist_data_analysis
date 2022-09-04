## Olist_data_analysis - notebooks

Analyze a dataset provided by Brazilian e-commerce marketplace [Olist](https://www.olist.com).

"Olist dataset version 2" is available on Kaggle:
https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/download?datasetVersionNumber=2

This folder contains notebooks that analyse the cleaned data provided by the olistpackage.

### 1_exploratory_analysis.ipynb
Exploratory analysis of the Olist cleaned data:
- Original dataset descritption
- Original dataset download and data cleansing
- Automated exploratory analysis with SweetViz
- Cardinalities
- Metric Design

### 2_orders_analysis.ipynb
Get an understanding of the `orders properties` and their associated `review_scores`
- Import the dataset from the olistpackage, description of the dataset
- Inspect features
- Simple regression of `review_score` against `delivery duration`
- Multivariate regression of `review_score`
- Exploration of low score `order_reviews`
- Net Promoter Score (NPS) exploration

### 3_seller_analysis.ipynb
Get an understanding of the `sellers properties` and their associated `review_scores`
Find sellers who have repeatedly been underperforming vs. others, and understand why.
- Import the dataset from the olistpackage, description of the dataset
- Impact of various features on `review_score` using a `multivariate-OLS` in `statsmodels`
- `seller_state` analysis

### 4_products_analysis.ipynb
Get an understanding of the `products properties` and their associated `review_scores`
Find `product categories` that repeatedly `underperform` vs. others, and understand the reasons behind.
- Import the dataset from the olistpackage, description of the dataset
- Exploratory analysis
- Predicting the average `review_score` per `product_id` using a `multivariate-OLS` from `statsmodels`
- Analysis per `product category`

### 5_products_analysis.ipynb
Sentiment analysis of the reviews to understand what could be the causes of the bad ones

### 6_final_analysis.ipynb
- P&L
- Seller cut-off analysis
- Underperforming products cut-off analysis
