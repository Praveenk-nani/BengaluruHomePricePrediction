import pandas as pd
from joblib import dump
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np
import json


df = pd.read_csv("cleaned_data.csv")
y = df['price']
x = df.drop("price",axis=1)


xtrain,xtest,ytrain,ytest = train_test_split(x,y,test_size=0.2,random_state=1)

linear_model = LinearRegression(fit_intercept=False)
linear_model.fit(xtrain,ytrain)

def prediction(location:str,sqft:int,bath:int,bhk:int):
    loc_index = np.where(x.columns == location)[0][0]
    x_pre=np.zeros(len(x.columns))

    x_pre[0]=sqft
    x_pre[1]=bath
    x_pre[2]=bhk
    if loc_index >= 0:
        x_pre[loc_index]=1
    
    return linear_model.predict(np.array([x_pre]))[0]


# print(prediction("Whitefield",1500,4,4).round().astype(int)," lakhs only")

columns = {
    "data_columns":[col.lower() for col in x.columns]
}

with open("benguluru_city_list.json",'w') as f:
    f.write(json.dumps(columns))

# dump(linear_model,"Benguluru_House_Price_Model.joblib")