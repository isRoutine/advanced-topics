import pandas as pd
import math

USER_A = 4

# import csv file and drop unuseful colunmns
ratings = pd.read_csv("dataset/ratings.csv").drop(['timestamp'], axis=1)
userA_ratings = ratings[ratings['userId'] == USER_A] # dataframe that contains ratings of USER A
ratings = ratings[ratings['userId'] != USER_A] # dataframe that contains ratings of all other users

similarity = dict() # dict for similarity { key='userid' : value = similarity}

# rows are ordered by userId, analyze the dataframe for all users
while ratings.shape[0] > 0:

    # read the userId of the first row and select all the rows(ratings) for this user
    userB_id = float(ratings.iloc[0]['userId'])
    userB_ratings = ratings[ratings['userId'] == userB_id]

    # create a dataframe that contains only the ratings on the common movies between the two users
    commonFilms = pd.merge(userA_ratings, userB_ratings, how ='inner', on =['movieId'])

    if commonFilms.empty != True: # correlation on ratings for common movies

        sim = commonFilms['rating_x'].corr(commonFilms['rating_y'])
        if not math.isnan(sim): #drop the user when similarity is nan
            similarity.update({userB_id : sim})
        #print('Similarity user '+ str(USER_A) + '& user', str(userB_id), ' --> ', similarity)

    # remove from the dataframe the rows(ratings of user B) analyzed in this iteration
    ratings = ratings[ratings['userId'] != userB_id]

# sort similarity and take top 10
similarity = dict(sorted(similarity.items(), key=lambda x:x[1], reverse=True)[:10])

print(similarity)
