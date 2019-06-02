
# coding: utf-8

import os
import re
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
#import matplotlib.lines as mlines
#from scipy.stats import norm
#from pyts.quantization import SAX
from tslearn.piecewise import PiecewiseAggregateApproximation
from tslearn.piecewise import SymbolicAggregateApproximation, OneD_SymbolicAggregateApproximation

# features for stock data
# stock_code + stock_name + stock_ref + stock_open + stock_last + stock_change + stock_change_perc + stock_volume


# read data from file list

path = "./dataset_5d"
files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.txt' in file:
            files.append(os.path.join(r, file))
print("all files: ")
for f in files:
    print(f)

# make time series table based on different features

features = ["stock_code", "stock_name", "stock_ref", "stock_open", 
            "stock_last", "stock_change", "stock_change_percent", "stock_volume"]
df_feature= []
for fea in features:
    df_day = []
    for f in files:
        df = pd.read_csv(f, delimiter="|", header=None, names = features)
        df_fea = df.loc[:,fea]
        
        df_day.append(df_fea)
    df_feature.append(np.array(df_day).T)
df_feature = np.array(df_feature)
print(df_feature.shape)

df_time_series = []
day_features = ['day1', 'day2', 'day3', 'day4', 'day5']
for df_fea in df_feature:
    day_feature = pd.DataFrame(df_fea,columns = day_features)
    df_time_series.append(day_feature)


# pick price feture and normalization

df_price = df_time_series[4]
for nf in day_features:
    rows = []
    for element in df_price[nf]:
        try:
            if type(element) == str:
                element = re.sub(r'[^\w\s]',"", element)
            element = float(element)
        except ValueError:
            #print("error",e," happens!")
            element = 0
        rows.append(element)
    df_price[nf] = rows
        
df_price = df_price.loc[:, day_features].replace(np.nan,0).values
# Standardizing the features
df_price = StandardScaler().fit_transform(df_price)
# add columns' name 
df_price = pd.DataFrame(df_price, columns = day_features)

dataset = df_price.values
print("price feature sample: ")
print(df_price.head())


# PAA transformation
# PAA transform (and inverse transform) of the data
n_paa_segments = 3
paa = PiecewiseAggregateApproximation(n_segments=n_paa_segments)
paa_list = []
for item in df_price.values:
    item = item.reshape((1,5,1))
    paa_price_inv = paa.inverse_transform(paa.fit_transform(item))
    paa_list.append(paa_price_inv)
paa_array = np.array(paa_list)

paa_data = paa_array.reshape(1904, 5)
paa_df = pd.DataFrame(paa_data, columns = day_features)
print("save time series data after PAA")
paa_df.to_csv("./paa_stock_data_time_series.csv", sep=',', encoding='utf-8')
print("PAA sample: ")
print(paa_df.head())


n_sax_symbols = 3
sax = SymbolicAggregateApproximation(n_segments=n_paa_segments, alphabet_size_avg=n_sax_symbols)
sax_dataset_inv = sax.inverse_transform(sax.fit_transform(dataset))


# save the processed data with sax transformation
sax_data = sax_dataset_inv.reshape(1904, 5)
sax_df = pd.DataFrame(sax_data,columns = day_features)
print("save time series data after SAX")
sax_df.to_csv("./sax_stock_data_time_series.csv", sep=',', encoding='utf-8')
print("SAX sample: ")
sax_df.head()


# 1d-SAX tranformation

n_sax_symbols_slope = 4
n_sax_symbols_avg = 4

one_d_sax = OneD_SymbolicAggregateApproximation(
    n_segments=n_paa_segments, 
    alphabet_size_avg=n_sax_symbols_avg,
    alphabet_size_slope=n_sax_symbols_slope)
one_d_list = []
for item in dataset:
    item = item.reshape((1,5,1))
    one_d_sax_dataset_inv = one_d_sax.inverse_transform(one_d_sax.fit_transform(item))
    one_d_list.append(one_d_sax_dataset_inv)
one_d_sax_array = np.array(one_d_list)

one_d_data = one_d_sax_array.reshape(1904, 5)
one_d_df = pd.DataFrame(one_d_data, columns = day_features)
print("save time series data after 1D SAX")
one_d_df.to_csv("./one_d_sax_stock_data_time_series.csv", sep=',', encoding='utf-8')
print("1D SAX sample: ")
one_d_df.head()


# plot the results for the first row

plt.figure(figsize=(12,8))
# First, raw time series
plt.subplot(2, 2, 1)  
plt.plot(dataset[0].ravel(), "b-")
plt.title("Raw time series")

plt.subplot(2, 2, 2)  
# Second, PAA
plt.plot(dataset[0].ravel(), "b-", alpha=0.4)
plt.plot(paa_array[0,0,:].ravel(), "b-")
plt.title("PAA")

plt.subplot(2, 2, 3)  # Then SAX
plt.plot(dataset[0].ravel(), "b-", alpha=0.4)
plt.plot(sax_dataset_inv[0].ravel(), "b-")
plt.title("SAX, %d symbols" % n_sax_symbols)

plt.subplot(2, 2, 4)  # Finally, 1d-SAX
plt.plot(dataset[0].ravel(), "b-", alpha=0.4)
plt.plot(one_d_sax_dataset_inv[0].ravel(), "b-")
plt.title("1d-SAX, %d symbols (%dx%d)" % (n_sax_symbols_avg * n_sax_symbols_slope,
                                          n_sax_symbols_avg,
                                          n_sax_symbols_slope))
plt.tight_layout()
plt.show()

