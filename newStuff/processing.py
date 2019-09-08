from sklearn.linear_model import LinearRegression
import datetime as dt
import pandas as pd
import numpy as np

def functionName(testdata):

    unfilteredx = []
    y = []



    for i in testdata:
        unfilteredx.append(i[5])
        y.append(i[4])



    #raw from Colin
    X = []

    for item in unfilteredx:
        count = 0
        corrected = ""
        for char in item:
            if char.isalpha():
                break
            else:
                corrected += char
        X.append(corrected)
        
    d = {'date':X, 'value':y}

    finalX = data_df['date'].tolist()
    finalY = data_df['value'].tolist()
    
    return finalX, finalY

