import numpy as np
import pandas as pd
import re
from sklearn.preprocessing import StandardScaler


def stock_data(path):
	# load dataset into Pandas DataFrame

	df = pd.read_csv(path, delimiter=",", header=None,
	                  names = ["name", "board", "stock_code", "52_week_high", "52_week_low", "open_price", 
	                           "high_price", "low_price", "last_price", "chg", "chg_percent", "volume", 
	                           "buy_volume", "sell_volume", "date", "time", "news", "final_report"])
	
	# data normalization
	num_features = ["52_week_high", "52_week_low", "open_price", "high_price", 
                "chg", "chg_percent", "volume", "buy_volume", "sell_volume", "last_price"]
	
	# Converting strting to numeric
	for nf in num_features:
	    rows = []
	    for element in df[nf]:
	        try:
	            if type(element) == str:
	                element = re.sub(r'[^\w\s]',"", element)
	            element = float(element)
	        except ValueError:
	            #print("error",e," happens!")
	            element = 0
	        rows.append(element)
	    df[nf] = rows
	
	# Separating out the features
	x_features = ["52_week_high", "52_week_low", "open_price", "high_price", 
	                "chg", "chg_percent", "volume", "buy_volume", "sell_volume"]

	#x = pd.DataFrame(x).fillna(0)
	x = df.loc[:, x_features].replace(np.nan,0).values
	
	# Standardizing the features
	x = StandardScaler().fit_transform(x)
	
	# add columns' name 
	x = pd.DataFrame(x,columns = x_features)
	
	# Separating out the target
	y = df.loc[:, ['last_price']].replace(np.nan,0).values
	y = pd.DataFrame(y,columns = ['price'])

	return (df,x,y)

if __name__ == "__main__":
	path = './dataset/stock_data_2019-03-15.txt'
	df,x,y = stock_data(path)
	print("Dimension of features and labels: ",x.shape, y.shape)

