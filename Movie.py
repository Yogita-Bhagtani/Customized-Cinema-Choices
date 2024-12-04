# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 14:32:32 2024

@author: DeLL
"""
import os
import streamlit as st
import pickle
import requests

working_dir = os.path.dirname(os.path.abspath(__file__))

similarity=pickle.load(open(f'saved_model2\similarity.pkl','rb'))


def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=c070108e424ca89a712e0b65409e780b&language=en-US'.format(movie_id))
    data=response.json()
    poster_path=data["poster_path"]
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path
    

def recommend(movie):
    recommended_movies=[]
    recommended_movies_posters=[]
    movie_index=movies_list[movies_list['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_lists=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    
    for i in movies_lists[0:5]:
        movie_id=movies_list.iloc[i[0]].movie_id
        # fetch poster from API
        
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies_list.iloc[i[0]].title)
    return recommended_movies,recommended_movies_posters

# i will be like this
#i=(35, 0.7505683356701914)

#i=(495, 0.7279315776474005)

#i=(2997, 0.7113159996271998)

#i=(31, 0.7088062931178188)

#i=(483, 0.7055562611121694)
    
st.set_page_config(page_title="Movie Recommender",
                       layout="wide",
                       page_icon="🧑‍⚕️")

    
    
movies_list=pickle.load(open(f'{working_dir}\saved_models\movies.pkl','rb'))

st.header("Movie Recommendation")
selected_movie_name=st.selectbox(
    "Movies",(movies_list['title'].values))
    # Movies",(movies_list.iloc[:, 1]))
   
    
if st.button('Recommend'):
    recommended_movies, recommended_movies_posters = recommend(selected_movie_name)
    num_movies = len(recommended_movies)

    # Create columns based on the number of recommendations
    cols = st.columns(num_movies)

    # Display recommendations in sequence using a loop
    for i in range(num_movies):
        with cols[i]:
            st.text(recommended_movies[i])
            st.image(recommended_movies_posters[i])
            
    #recommended_movies,recommended_movies_posters=recommend(selected_movie_name)
  ##with col2:
  #      st.text(recommended_movies[1])
   #    3 st.image(recommended_movies_posters[1])
    #with col3:
     #   st.text(recommended_movies[2])
      ##h col4:
        ####tps://api.themoviedb.org/3/movie/movie_id}?api_key=<<api_key>>&language=en-US

#c070108e424ca89a712e0b65409e780b
