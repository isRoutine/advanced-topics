from operator import ne
import pandas as pd
import math


# function: sim -> get the Pearson correlation between two users
# parameter
#   userA_ratings: DataFrame
#   userB_ratings: DataFrame
#   commonColumns: [string]
#
# return
#   similarity: float | nan
def getSimilarity(userA_id, userB_id, ratings, commonColumns=['movieId']):

    userA_ratings = ratings[ratings['userId'] == userA_id]
    userB_ratings = ratings[ratings['userId'] == userB_id]
    common = pd.merge(userA_ratings, userB_ratings, how ='inner', on = commonColumns)
    if common.empty == True:
        return math.nan
    else:
        s = common['rating_x'].corr(common['rating_y'])
        return s.item()

# function: sim -> get average rating for user
# parameter
#   ratings: DataFrame
# return
#   average: float
def avg(ratings):
   return ratings['rating'].sum()/len(ratings)



# function: get moviesIds of all movies not rated by user
# parameter
#   ratings: DataFrame
#   movies:  DataFrame
# return
#   m: numpy array
def getMoviesNotRated(userId, movies, ratings):
    userRatings = ratings[ratings['userId'] == userId]
    m = movies.merge(userRatings, how='left', indicator=True, on=['movieId'])
    m = m[m['_merge'] == 'left_only']
    return m['movieId'].values


# function: get users that rated movieId
# parameter
#   movieId:  float
#   ratings: DataFrame
# return
#   users: set
def getUsersForFilm(movieId, ratings):
    users = set()
    ratings = ratings[ratings['movieId'] == movieId]
    user = None
    for index, row in ratings.iterrows():
        if(row['userId'] != user):
            user = row['userId'].item()
            users.add(user)
    return users



# function: get rating of a user for a movie
# parameter
#   userId: float
#   movieId:  float
#   ratings: DataFrame
# return
#   rating: float
def getRating(userId, movieId, ratings):
    row = ratings[(ratings['userId'] == userId) & (ratings['movieId'] == movieId)]
    return float(row.iloc[0]['rating'])


# function: predict the rating of a movie for a user
# parameter
#   userId: float
#   movieId:  float
#   ratings: DataFrame
# return
#   prediction: float
def getPrediction(userId, movieId, ratings):
    avgA = avg(ratings[ratings['userId'] == 1])
    num = 0
    den = 0

    for user in getUsersForFilm(movieId,ratings):
        s = getSimilarity(userId,user,ratings)
        if( not math.isnan(s)):
            num += s * (getRating(user,movieId,ratings) - avg(ratings[ratings['userId']==user]))
            den += s

    try:
        x = num/den
        prediction = avgA + x
    except:
        prediction = math.nan

    return prediction



USER_A = 1

# import csv file and drop unuseful colunmns
ratings = pd.read_csv("dataset/ratings.csv").drop(['timestamp'], axis=1)
movies = pd.read_csv("dataset/movies.csv")

similarity = dict() # dict for similarity { key='userid' : value = similarity}
predictions =  dict()


# get top 10 users most similar to USER_A
# rows are ordered by userId, analyze the dataframe for all users
rates = ratings[ratings['userId'] != USER_A]
userA_ratings = ratings[ratings['userId'] == USER_A]
while rates.shape[0] > 0:

    #read the userId of the first row and select all the rows(ratings) for this user
    userB_id = rates.iloc[0]['userId']
    userB_ratings = rates[rates['userId'] == userB_id]

    # create a dataframe that contains only the ratings on the common movies between the two users
    commonFilms = pd.merge(userA_ratings, userB_ratings, how ='inner', on =['movieId'])

    if commonFilms.empty != True: # correlation on ratings for common movies
        sim = commonFilms['rating_x'].corr(commonFilms['rating_y'])
        if not math.isnan(sim): #drop the user when similarity is nan
            similarity.update({userB_id : sim})

    # remove from the dataframe the rows(ratings of user B) analyzed in this iteration
    rates = rates[rates['userId'] != userB_id]

# sort similarity and take top 10
similarity = dict(sorted(similarity.items(), key=lambda x:x[1], reverse=True)[:10])
print(f'top 10 most similar users to user_{USER_A} are: {similarity}')


# predict movies rating for USER_A
mvs = getMoviesNotRated(USER_A, movies, ratings)
for mv in mvs:
    prediction = getPrediction(USER_A, mv, ratings)
    if(not math.isnan(prediction)):
      predictions.update({mv : prediction})
predictions = dict(sorted(predictions.items(), key=lambda x:x[1], reverse=True)[:10])
print(f'top 10 most recommended movies to user_{USER_A} are: {predictions}')
