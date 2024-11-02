
import pickle
import streamlit as st
from surprise import SVD

# Load data and model
with open('66130701704recommendation_movie_svd.pkl', 'rb') as file:
    svd_model, movie_ratings, movies = pickle.load(file)

# Sidebar for user selection
st.sidebar.header("Movie Recommendation System")
user_id = st.sidebar.number_input("Enter User ID:", min_value=1, step=1)

# Filter movies for the selected user
rated_user_movies = movie_ratings[movie_ratings['userId'] == user_id]['movieId'].values
unrated_movies = movies[~movies['movieId'].isin(rated_user_movies)]['movieId']

# Generate predictions for unrated movies
pred_ratings = [svd_model.predict(user_id, movie_id) for movie_id in unrated_movies]
sorted_predictions = sorted(pred_ratings, key=lambda x: x.est, reverse=True)

# Get top 10 movie recommendations
top_recommendations = sorted_predictions[:10]

# Display recommendations
st.write(f"### Top 10 Movie Recommendations for User {user_id}")
for recommendation in top_recommendations:
    movie_title = movies[movies['movieId'] == recommendation.iid]['title'].values[0]
    st.write(f"{movie_title} (Estimated Rating: {recommendation.est:.2f})")


