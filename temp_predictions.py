import pandas as pd
import pickle
import os
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.stattools import adfuller
import itertools
import warnings
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error


def main():

    # Reading from a pickle file may or may not be faster? idk take out if reading from pandas every time is better
    if not os.path.exists("gltbycountry.p"):
        df = pd.read_csv("archive/GlobalLandTemperaturesByCountry.csv")
        pickle.dump(df, open( "gltbycountry.p", "wb" ))
    else:
        df = pickle.load(open( "gltbycountry.p", "rb" ))
    
    # Drop all na
    df.dropna(inplace=True)
    # Set datetime
    df.index = pd.to_datetime(df['dt'], format='%Y-%m-%d')
    del df['dt']
    del df['AverageTemperatureUncertainty']
    # df.sort_values(by='dt')
    # print(df.iloc[[0, -1]])


    countries = df['Country'].unique()
    # print(countries)
    for c in countries:
        df_c = df[df['Country'] == c]
        del df_c['Country']
        # f = open("demofile2.txt", "a")
        # f.write("Now the file has more content!")
        # f.close()

        # if c == "Afghanistan":
        # ts = df_c["AverageTemperature"]
        # adf_result = adfuller(ts, autolag='AIC')
        # print(f'ADF Statistic:{adf_result[0]}')
        # print(f'p-value:{adf_result[1]}')

        # for percentage,value in adf_result[4].items():
        #     print("Critical Value:")
        #     print(f'{percentage}{value}')

        train_df, test_df = train_test_split(df_c, shuffle=False)

        # plt.ylabel('Average Temperature')
        # plt.xlabel('Date')
        # plt.xticks(rotation=45)

        # plt.plot(train_df, color = "black")
        # plt.plot(test_df, color = "red")
        # plt.legend()
        # plt.show()

        ts = train_df['AverageTemperature']

        # warnings.filterwarnings('ignore')

        # # parameter ranges
        # p = range(0, 4)
        # d = 0 #ARMA model
        # q = range(0, 4)

        # # all possible combinations of p and q
        # pq = itertools.product(p, q)

        # best_aic = float('inf') 
        # best_order = None
        # best_model_res = None

        # for order in pq:
        #     try:
        #         model = SARIMAX(ts, order=(*order, d), seasonal_order=(2,2,2,12))
        #         results = model.fit()
        #         aic = results.aic
        #         if aic < best_aic:
        #             best_aic = aic
        #             best_order = order
        #             best_model_res = results
        #         print(f'ARMA{order} - AIC: {aic:.2f}')
        #     except:
        #         continue

        # print(f'Best ARMA model: ARMA{best_order} - AIC: {best_aic:.2f}')
        model = SARIMAX(ts, order=(3,0,0), seasonal_order=(2,2,2,12))
        best_model_res = model.fit()
        y_pred = best_model_res.get_forecast(len(test_df.index))
        y_pred_df = y_pred.conf_int(alpha = 0.05) 
        y_pred_df["Predictions"] = best_model_res.predict(start = y_pred_df.index[0], end = y_pred_df.index[-1])
        y_pred_df.index = test_df.index
        y_pred_out = y_pred_df["Predictions"] 

        # sns.set()
        # plt.ylabel('Average Temperature')
        # plt.xlabel('Date')
        # plt.xticks(rotation=45)

        # plt.plot(train_df, color = "black")
        # plt.plot(test_df, color = "red")
        # plt.plot(y_pred_out, color='green', label = 'Predictions')
        # plt.legend()
        # plt.show()

        arma_rmse = np.sqrt(mean_squared_error(test_df["AverageTemperature"].values, y_pred_df["Predictions"]))
        print("RMSE: ",arma_rmse)

main()