from scipy.sparse import csr_matrix
final_ratings_sparse = csr_matrix(final_ratings_matrix.values)

# Calculate the minimum dimension of final_ratings_sparse
min_dimension = min(final_ratings_sparse.shape)

# Adjust the value of k if necessary
k = min(50, min_dimension - 1)  # Ensuring k is less than the minimum dimension

# Singular Value Decomposition
U, s, Vt = svds(final_ratings_sparse, k=k)

# Construct diagonal array in SVD
sigma = np.diag(s)

U.shape
sigma.shape
Vt.shape
all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt)

# Predicted ratings
preds_df = pd.DataFrame(abs(all_user_predicted_ratings), columns = final_ratings_matrix.columns)
preds_df.head()
preds_matrix = csr_matrix(preds_df.values)
import numpy as np

def recommend_items(user_index, interactions_matrix, preds_matrix, num_recommendations):

    # Get the user's ratings from the actual and predicted interaction matrices
    user_ratings = interactions_matrix[user_index,:].toarray().reshape(-1)
    user_predictions = preds_matrix[user_index,:].toarray().reshape(-1)

    #Creating a dataframe with actual and predicted ratings columns
    temp = pd.DataFrame({'user_ratings': user_ratings, 'user_predictions': user_predictions})
    temp['Recommended Products'] = np.arange(len(user_ratings))
    temp = temp.set_index('Recommended Products')

    #Filtering the dataframe where actual ratings are 0 which implies that the user has not interacted with that product
    temp = temp.loc[temp.user_ratings == 0]

    #Recommending products with top predicted ratings
    temp = temp.sort_values('user_predictions',ascending=False)#Sort the dataframe by user_predictions in descending order
    print('\nBelow are the recommended products for user(user_id = {}):\n'.format(user_index))
    print(temp['user_predictions'].head(num_recommendations))

#Enter 'user index' and 'num_recommendations' for the user
recommend_items(1,final_ratings_sparse,preds_matrix,5)
recommend_items(10,final_ratings_sparse,preds_matrix,10)
final_ratings_matrix['user_index'] = np.arange(0, final_ratings_matrix.shape[0])
final_ratings_matrix.set_index(['user_index'], inplace=True)

# Actual ratings given by users
final_ratings_matrix.head()
average_rating = final_ratings_matrix.mean()
average_rating.head()
preds_df.head()
avg_preds=preds_df.mean()
avg_preds.head()
rmse_df = pd.concat([average_rating, avg_preds], axis=1)

rmse_df.columns = ['Avg_actual_ratings', 'Avg_predicted_ratings']

rmse_df.head()
from matplotlib import pyplot as plt
_df_10['Avg_actual_ratings'].plot(kind='hist', bins=20, title='Avg_actual_ratings')
plt.gca().spines[['top', 'right',]].set_visible(False)
from matplotlib import pyplot as plt
_df_11['Avg_predicted_ratings'].plot(kind='hist', bins=20, title='Avg_predicted_ratings')
plt.gca().spines[['top', 'right',]].set_visible(False)
RMSE=mean_squared_error(rmse_df['Avg_actual_ratings'], rmse_df['Avg_predicted_ratings'], squared=False)
print(f'RMSE SVD Model = {RMSE} \n')

