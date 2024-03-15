import pandas as pd


df = pd.read_csv("ratings.csv")
print(df)
user = 1

userD = df[df['userId'] == user]
otherD = df[df['userId'] == 2]

mergeD = pd.merge(userD, otherD, how ='inner', on =['movieId'])
print(mergeD)
mergeD = mergeD.drop(['movieId','timestamp_x','timestamp_y','userId_x','userId_y'], axis=1)
print(mergeD)


data = pd.DataFrame({
    "column1": [5.0, 3.0, 4.0, 4.0],
    "column2": [3.0, 1.0, 2.0, 3.0],
    "column3": [4.0, 3.0, 4.0, 3.0],
    "column4": [3.0, 3.0, 1.0, 5.0],
    "column5": [1.0, 5.0, 5.0, 2.0]})

# get correlation between element wise
print(data)
print(data['column1'].corr(data['column2']))
print(data['column1'].corr(data['column3']))
print(data['column1'].corr(data['column4']))
print(data['column1'].corr(data['column5']))
