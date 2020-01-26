import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("movie_dataset.csv")


def get_movie_details(title):
    return df[df.title == title][["title", "release_date", "overview", "vote_average", "director"]].values[0]


def get_title_from_index(index):
    return df[df.index == index]["title"].values[0]


def get_index_from_title(title):
    return df[df.title == title]["index"].values[0]


def combine_features(row):
    return row['keywords'] + " " + row['cast'] + " " + row['genres'] + " " + row['director']


def search(title):
    search_list = df[df['title'].str.lower().str.contains(title.lower())]["title"].values

    if len(search_list) == 0:
        return []
    return search_list


def recommend(movie):
    # Select Features
    features = ['keywords', 'cast', 'genres', 'director']

    # Create a column in DF which combines all selected features
    for feature in features:
        df[feature].fillna('', inplace=True)

    df["combined_features"] = df.apply(combine_features, axis=1)

    # Create count matrix from this new combined column
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(df["combined_features"])

    # Compute the Cosine Similarity based on the count_matrix
    cosine_sim = cosine_similarity(count_matrix)

    # Get index of this movie from its title
    movie_index = get_index_from_title(movie)

    # Get a list of similar movies in descending order of similarity score
    similar_movies = list(enumerate(cosine_sim[movie_index]))
    sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)

    # Print titles of first 50 movies
    count = 0
    recommended_movies_list = []
    for movie in sorted_similar_movies:
        recommended_movies_list.append(get_title_from_index(movie[0]))
        count += 1
        if count > 50:
            break

    return recommended_movies_list[1:]
