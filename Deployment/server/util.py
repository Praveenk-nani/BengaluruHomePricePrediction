# from joblib import load
import joblib
import json
import numpy as np

__locations=[]
__data_columns=[]
__model=None

def get_location_name():
    load_saved_artifacts()
    return __locations




def load_saved_artifacts():
    global __locations
    global __data_columns
    global __model
    

    with open("D:/MachineLearning/Projects/Benguluru_House_Price_Prediction/Deployment/server/artifacts/benguluru_city_list.json","r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]

    
    with open("D:/MachineLearning/Projects/Benguluru_House_Price_Prediction/Deployment/server/artifacts/Benguluru_House_Price_Model.joblib","rb") as f:
        __model = joblib.load(f)



def get_estimated_price(location :str,bhk:int,bath:int,sqft:int):
    load_saved_artifacts()
    try:
        index_of_location = __data_columns.index(location.lower())
    except:
        index_of_location=-1

    x=np.zeros(len(__data_columns))
    x[0]=sqft
    x[1]=bath
    x[2]=bhk

    if index_of_location >=0:
        x[index_of_location]=1
    return round(__model.predict([x])[0],2)

if __name__ == "__main__":
    load_saved_artifacts()