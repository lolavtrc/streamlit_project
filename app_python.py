import streamlit as st
import pandas as pd
import numpy as np
import ast
import seaborn as sns
import matplotlib.pyplot as plt

st.title('Streamlit project')

# Chargement du fichier CSV en DataFrame
def load_data():
    data = pd.read_csv('data/tmdb_5000_movies.csv')
    data['genres'] = data['genres'].apply(lambda x: [genre['name'] for genre in ast.literal_eval(x)])
    data['keywords'] = data['keywords'].apply(lambda x: [keyword['name'] for keyword in ast.literal_eval(x)])
    data['production_companies'] = data['production_companies'].apply(lambda x: [keyword['name'] for keyword in ast.literal_eval(x)])
    data['production_countries'] = data['production_countries'].apply(lambda x: [keyword['iso_3166_1'] for keyword in ast.literal_eval(x)])
    
    data.drop(columns=['homepage', 'id', 'spoken_languages', 'status', 'tagline'], inplace=True)
    
    # Réordonner les colonnes dans l'ordre spécifié
    column_order = ['title', 'vote_average', 'genres', 'overview', 'runtime', 'release_date', 'original_language', 'budget', 'revenue', 'production_companies', 'production_countries', 'original_title', 'vote_count']
    
    data = data[column_order]

    return data

movies_data = load_data()

# Affichage des informations sur les films
st.subheader("01 - Information available in the Movie dataframe :")
st.write(movies_data)

# Affichage de quelques informations 
st.subheader("02 - A few Insights about the data")

st.text('Number of movies in the dataset : ')
st.write(movies_data.shape[0])

st.text('Average rate value of the movies (out of 10): ')
st.write(np.round(movies_data['vote_average'].mean(), 2))

# Histogramme des notes attribuées
fig = plt.figure()
st.text('Histogram of Vote values distribution : ')
sns.histplot(movies_data['vote_average'], bins=20, kde=True)
st.pyplot(fig)

# Histogramme des revenus (pour les données non nulles)
revenue_data = movies_data[movies_data['revenue'] > 0]
fig = plt.figure()
st.text('Histogram of Revenue distribution :')
sns.histplot(revenue_data['revenue'], bins=20, kde=True)
st.pyplot(fig)

# Histogramme des budgets (pour les données non nulles)
budget_data = movies_data[movies_data['budget'] > 0]
fig = plt.figure()
st.text('Histogram of Budget distribution :')
sns.histplot(budget_data['budget'], bins=20, kde=True)
st.pyplot(fig)

# Graphique de dispersion entre le revenu et le budget (pour les données non nulles)
fig = plt.figure(figsize=(10, 6))
st.text('Revenue vs Budget, scatter plot :')
sns.scatterplot(x='budget', y='revenue', data=budget_data)
st.pyplot(fig)

# Affichage de quelques informations 
st.subheader("03 - Look out for movie recommendation by genre")

# Sélection du genre à partir du menu déroulant
selected_genre = st.selectbox("Select a genre:", movies_data['genres'].explode().unique())

# Filtrer les films comportant ce genre
filtered_movies = movies_data[movies_data['genres'].apply(lambda x: selected_genre in x)]

# Afficher les 5 films les mieux notés
if not filtered_movies.empty:
    top_rated_movies = filtered_movies.sort_values(by='vote_average', ascending=False).head(5)
    st.text(f"Top 5 Highest Rated Movies in the '{selected_genre}' Genre:")
    st.write(top_rated_movies[['title', 'vote_average']])
else:
    st.text(f"No movies found in the '{selected_genre}' Genre.")
    
# Affichage de quelques informations 
st.subheader("04 - Look out for movie recommendation by Production company")

# Sélection du genre à partir du menu déroulant
selected_company = st.selectbox("Select a Production company:", movies_data['production_companies'].explode().unique())

# Filtrer les films comportant ce genre
filtered_movies_by_company = movies_data[movies_data['production_companies'].apply(lambda x: selected_company in x)]

# Afficher les 5 films les mieux notés
if not filtered_movies_by_company.empty:
    top_rated_movies = filtered_movies_by_company.sort_values(by='vote_average', ascending=False).head(5)
    st.text(f"Top 5 Highest Rated Movies producted by '{selected_company} :")
    st.write(top_rated_movies[['title', 'vote_average']])
else:
    st.text(f"No movies found.")

# Ajout de la section de recherche par titre de film
st.subheader("Search for a Movie by Title")

# Filtrer les films par titre en fonction de la recherche

# Barre de recherche pour le titre du film
search_term = ''

# Filtrer les films par titre en fonction de la recherche
matching_movies = movies_data[movies_data['title'].str.contains(search_term, case=False, na=False)]

# Affichage des informations sur le film sélectionné dans un tableau à deux colonnes
if not matching_movies.empty:
    selected_movie = st.selectbox("Select a movie:", matching_movies['title'].tolist())
    movie_info = matching_movies[matching_movies['title'] == selected_movie]
    st.subheader(f"Information for the Movie '{selected_movie}':")
    
    # Créer un tableau de deux colonnes pour afficher les informations
    info_table = pd.DataFrame({
        'Attribute': movie_info.columns,
        'Value': movie_info.values[0]
    })
    st.write(info_table)
else:
    st.subheader("No matching movies found.")
