from flask import Flask, render_template, request, url_for
from movie_recommender import recommend, search, get_movie_details

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def search_movies():
    movie = request.form.get("movie_name")
    if movie:
        return render_template('index.html', movies=search(movie))
    else:
        return render_template('index.html')


@app.route('/details', methods=['GET', 'POST'])
def details():
    movie = request.form.get('movie_details')
    if movie:
        return render_template('details.html', movie_details=get_movie_details(movie),
                               recommend_movies=recommend(movie))
    else:
        return render_template('details.html')


if __name__ == '__main__':
    app.debug = True
    app.run()
