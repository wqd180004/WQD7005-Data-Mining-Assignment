
# coding: utf-8


import numpy as np
import pandas as pd
import re
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


# ### data loading


# load dataset into Pandas DataFrame

df = pd.read_csv('stock_data_2019-03-15.txt', delimiter=",", header=None,
                  names = ["name", "board", "stock_code", "52_week_high", "52_week_low", "open_price", 
                           "high_price", "low_price", "last_price", "chg", "chg_percent", "volume", 
                           "buy_volume", "sell_volume", "date", "time", "news", "final_report"])

# show dimension of data
print(df.shape)
print(df.head())


# ### data normalization



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
# add columns' name f
x = pd.DataFrame(x,columns = x_features)
# Separating out the target
y = df.loc[:, ['last_price']].replace(np.nan,0).values
print(x.shape, y.shape)


# ### co-variance


variable_features = ["last_price", "52_week_high", "52_week_low", "open_price", "high_price", 
                "chg", "chg_percent", "volume", "buy_volume", "sell_volume"]
co_variance_df = df.loc[:, variable_features]
co_variance = co_variance_df.cov()
print(co_variance)


# ### sorted co_variance list


sorted_co_variance = co_variance.loc[:,'last_price'].sort_values(ascending = False)
print(sorted_co_variance)


# ### pca


pca = PCA(n_components=2)
principal_components = pca.fit_transform(x)
principal_data = pd.DataFrame(data = principal_components, 
                              columns = ['principal component 1', 'principal component 2'])

print(principal_data)

final_data = pd.concat([principal_data, df[['last_price']]], axis = 1)

print(final_data)


# ### explained_variance

# The PCA class contains explained_variance_ratio_ which returns the variance caused by each of the principal components. 


explained_variance = pca.explained_variance_ratio_  
print(explained_variance)


# ### plot


fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1)
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('2 component PCA', fontsize = 20)
ax.scatter(final_data.loc[:,'principal component 1'],
           final_data.loc[:,'principal component 2'])
ax.grid()
plt.show()

