import pandas as pd

r_cols = ['user_id', 'movie_id', 'rating']
ratings = pd.read_csv('e:/datascience/u.data', sep='\t', names=r_cols, usecols=range(3), encoding="ISO-8859-1")

m_cols = ['movie_id', 'title']
movies = pd.read_csv('e:/datascience/u.item', sep='|', names=m_cols, usecols=range(2), encoding="ISO-8859-1")

ratings = pd.merge(movies, ratings)

ratings.head()
userRatings = ratings.pivot_table(index=['user_id'],columns=['title'],values='rating')
userRatings.head()

corrMatrix = userRatings.corr()
corrMatrix.head()

corrMatrix = userRatings.corr(method='pearson', min_periods=100)
print "corrMatrix["101 Dalmatians (1996)"]"

myRatings = userRatings.loc[0].dropna()
print "myRatings"


#item based reccomendation by going to a list of all movies that asingle user rated

simCandidates = pd.Series()
for i in range(0, len(myRatings.index)):
    print ("Adding sims for " + myRatings.index[i] + "...")
    # Retrieve similar movies to this one that I rated
    sims = corrMatrix[myRatings.index[i]].dropna()
    # Now scale its similarity by how well I rated this movie
    sims = sims.map(lambda x: x * myRatings[i])
    # Add the score to the list of similarity candidates
    simCandidates = simCandidates.append(sims)
    
#Glance at our results so far:
print ("sorting")
simCandidates.sort_values(inplace = True, ascending = False)
print (simCandidates.head(10))

#if same movies come twice or more sum up there correlation score
simCandidates = simCandidates.groupby(simCandidates.index).sum()


#sort and print top ten movies
simCandidates.sort_values(inplace = True, ascending = False)
print "simCandidates.head(10)"

#filterout the movies that the user have already rated.
filteredSims = simCandidates.drop(myRatings.index)
print "filteredSims.head(10)"