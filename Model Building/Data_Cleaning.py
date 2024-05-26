import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("bengaluru_house_prices.csv")

df.drop(["availability","society","area_type","balcony"],axis=1,inplace=True)

# print(df.isna().sum())
# print(df.groupby("size")["size"].agg("count"))

# print(df[df['size']== "43 Bedroom"])

df.fillna({"bath":df["bath"].median()},inplace=True)
df.dropna(inplace=True)


df['bhk']=df["size"].apply(lambda x: int(x.split(' ')[0]))
df.drop("size",axis=1,inplace=True)

# print(df.isna().sum())



def isfloat(x):
    try:
        float(x)
    except:
        return False
    return True

def handle_messydata(x):
    token = x.split('-')
    if(len(token)==2):
        return (float(token[0]) + float(token[1]))/2
    try:
        return float(x)
    except:
        return None


# df[~df["total_sqft"].apply(lambda x: isfloat(x))].apply(lambda x: handle_messydata(x))
df["total_sqft"] = df["total_sqft"].apply(lambda x:handle_messydata(x))



# print(df[~df["total_sqft"].apply(lambda x: isfloat(x))])
df.dropna(inplace=True)
# print(df.isna().sum())



# print(df.loc[30])
# print(df.shape)






#doing feature engineering means adding new feature to

df["price_per_sqft"]=(((df['price']*100000)/df['total_sqft']).round().astype(int))


# print(df.groupby("location")["location"].agg("count").sort_values(ascending=False))
# print(df["location"].nunique())

df["location"] = df["location"].apply(lambda x:x.strip())


values_count = df.groupby("location")["location"].agg("count").sort_values(ascending=False)



location_less_than_10 = values_count[values_count<=10]

# print(df.groupby("location")["location"].agg("count").sort_values(ascending=False))


df["location"] = df["location"].apply(lambda x: 'others' if x in location_less_than_10 else x)


errored_data_element = df[df["total_sqft"]/df["bhk"] < 300]

df = df[~(df["total_sqft"]/df["bhk"] < 300)]


def removing_outliner(df):
    # outliner removal using "NORMAL DISRTIBUTION"
    # any data item beyond or above the 68 percentage
    # we are removing all the data element which are extream in cases such as very low price or very high price
    new_df = pd.DataFrame()
    for key,sub_df in df.groupby("location"):
        mean = np.mean(sub_df["price_per_sqft"])
        standard_deviation = np.std(sub_df["price_per_sqft"])
        reduced_df = sub_df[(sub_df["price_per_sqft"] > (mean-standard_deviation)) & (sub_df["price_per_sqft"] < (mean+standard_deviation))]
        new_df = pd.concat([new_df,reduced_df],ignore_index=True)
    
    return new_df


# print(df.shape)

new_df = removing_outliner(df)

# print(new_df.shape)


#now removing some more outlines

def plotting(df,location):
    bh2 = df[(df["location"]==location) & (df["bhk"]==2)]
    bh3 = df[(df["location"]==location) & (df["bhk"]==3)]
    plt.figure(figsize=(15,10))

    plt.scatter(bh3["total_sqft"],bh3["price_per_sqft"],marker="*",edgecolors="blue")
    plt.scatter(bh2["total_sqft"],bh2["price_per_sqft"],marker="+",edgecolors="black")
    plt.xlabel("total_sqft area")
    plt.ylabel("price")
    plt.show()


# plotting(df,"Rajaji Nagar")


def removing_bhk_outliners(df):
    exclude_indices = np.array([])
     
    for location,location_df in df.groupby("location"):
        bhk_stats={}
        for bhk,bhk_df in location_df.groupby("bhk"):
            bhk_stats[bhk]={
                "mean":np.mean(bhk_df["price_per_sqft"]),
                "std":np.std(bhk_df["price_per_sqft"]),
                "count":bhk_df.shape[0]
            }

        for bhk,bhk_df in location_df.groupby("bhk"):
            stats = bhk_stats.get(bhk-1)
            if stats and stats["count"]>5:
                exclude_indices = np.append(exclude_indices,bhk_df[(bhk_df["price_per_sqft"]) < (stats["mean"])].index.values)
            
    return df.drop(exclude_indices,axis="index")

# print(new_df.shape)
new_df = removing_bhk_outliners(new_df)

df = new_df.copy()

# plotting(df,"Rajaji Nagar")



def plotting_histogram(df):
    plt.figure(figsize=(10,8))
    plt.hist(df["price_per_sqft"],rwidth=0.5)
    plt.xlabel("price per sqft")
    plt.ylabel("count")
    plt.show()

# plotting_histogram(df)

def plotting_bathrooms(df):
    plt.figure(figsize=(10,8))
    plt.hist(df["bath"],rwidth=0.5)
    plt.xlabel("Number of bathrooms")
    plt.ylabel("count")
    plt.show()


# plotting_bathrooms(df)

def removing_bathroom_outliners(df):

    return df[(df['bath']) <= (df["bhk"]+2)]


df = removing_bathroom_outliners(df)

df.drop("price_per_sqft",axis=1,inplace=True)

one_hot_encoded = pd.get_dummies(df['location'])

new_encoded_df = pd.concat([df,one_hot_encoded],axis=1)


# print(new_encoded_df)


# print(df.shape)


# print(df.shape)
# print(df[(df['total_sqft']/df["bhk"]) < 300])

new_encoded_df.drop("location",axis=1,inplace=True)
# print(new_encoded_df)
# new_encoded_df.to_csv("cleaned_data.csv",index=False)


