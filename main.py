import streamlit as st
import pickle
import pandas as pd
import requests
import gdown
import os

# Google Drive file ID for similarity.pkl
file_id = "1m0QcQQgpUJxgSLEnOu1H6PNN09_x2QO-"
download_url = f"https://drive.google.com/uc?id={file_id}"

def fetch_similarity_matrix():
    if not os.path.exists("similarity.pkl"):
        # Download similarity.pkl from Google Drive if not already present
        gdown.download(download_url, "similarity.pkl", quiet=False)
    with open("similarity.pkl", "rb") as f:
        similarity_matrix = pickle.load(f)
    return similarity_matrix

# Fetch the movie poster
def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(
            movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movie_posters

# Load movie data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Load the similarity matrix from Google Drive
similarity = fetch_similarity_matrix()

st.title('Movie Recommender System')

# Dropdown menu for movie selection
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# Show recommendations on button click
if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie)
    # Display recommendations in columns
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
