import pandas as pd
from sklearn.model_selection import GridSearchCV,train_test_split,ShuffleSplit
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression,Lasso



df = pd.read_csv("cleaned_data.csv")


y = df.price
df.drop(["price","others"],axis=1,inplace=True)
x=df
xtrain,xtest,ytrain,ytest = train_test_split(x,y,test_size=0.2,random_state=1)



def finding_best_model_using_grid_search_cv(x,y):
    algorithms={

        "linear_regression":{
            "model":LinearRegression(),
            "params":{
                'fit_intercept':[True,False]
            }

        },

        "lasso":{
            "model":Lasso(),
            "params":{
                'alpha':[1,2],
                'selection':["random","cyclic"]
            }
        }

    }

    scores=[]
    cv = ShuffleSplit(n_splits=5,test_size=0.2,random_state=0)
    for model_name,mp in algorithms.items():
        clf = GridSearchCV(mp["model"],mp['params'],cv=cv,return_train_score=False)
        clf.fit(x,y)

        scores.append({
            'Model':model_name,
            'Parameters':clf.best_params_,
            'BestScore':clf.best_score_
        })

    dataframe = pd.DataFrame(scores,columns=["Model","Parameters","BestScore"])
    print(dataframe)



linear_model = LinearRegression(fit_intercept=False)

linear_model.fit(xtrain,ytrain)

print(linear_model.score(xtest,ytest))

