
# coding: utf-8

import load_data


if __name__ == "__main__":
	# load data
	path = './dataset/stock_data_2019-03-15.txt'
	df,x,y = load_data.stock_data(path)

	# co-variance
	variable_features = ["last_price", "52_week_high", "52_week_low", "open_price", "high_price", 
                "chg", "chg_percent", "volume", "buy_volume", "sell_volume"]
	co_variance_df = df.loc[:, variable_features]
	co_variance = co_variance_df.cov()

	print("co-variance sample: ")
	print(co_variance.head())

	# sorted co-variance list
	sorted_co_variance = co_variance.loc[:,'last_price'].sort_values(ascending = False)
	print("sorted co-variance list: ")
	print(sorted_co_variance)
	
