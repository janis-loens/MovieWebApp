from flask import Flask, request, jsonify, render_template, redirect, url_for
from data_manager import DataManager
from models import db, Movie, User
from api_communication import get_movie_data


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
db.init_app(app)
data_manager = DataManager()


@app.route('/')
def home():
    users = data_manager.get_all_users()
    return render_template('index.html', users=users)

@app.route('/users', methods=['POST'])
def add_user():
    username = request.form.get('username')
    if username:
        user = data_manager.add_user(username)
        return redirect(url_for('home'))
    return jsonify({'error': 'Username is required'}), 400

@app.route('/select_user', methods=['POST'])
def select_user():
    user_id = request.form.get('user_id')
    if user_id:
        return redirect(url_for('get_user_movies', user_id=user_id))
    return redirect(url_for('home'))

@app.route('/users/<int:user_id>/movies', methods=['GET', 'POST'])
def get_user_movies(user_id):
    user = User.query.filter_by(id=user_id).one()
    username = user.username if user else 'Unknown User'
    if request.method == 'POST':
        title = request.form.get('title')
        movie_data = get_movie_data(title)
        if movie_data:
            data_manager.add_movie(
                title=movie_data["Title"],
                year=movie_data["Year"],
                director=movie_data["Director"],
                poster_url=movie_data["Poster"],
                user_id=user_id
            )
            return redirect(url_for('get_user_movies', user_id=user_id, username=username))
        return jsonify({'error': 'Title is required'}), 400

    movies = data_manager.get_user_movies(user_id)
    return render_template('movies.html', movies=movies, user_id=user_id, username=username)


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    new_title = request.form.get('new_title')

    if new_title:
        updated_movie = data_manager.update_movie(movie_id, new_title)
        if updated_movie:
            return redirect(url_for('get_user_movies', user_id=user_id))
        return jsonify({'error': 'Movie not found'}), 404
    return jsonify({'error': 'New title is required'}), 400


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(movie_id)
    return redirect(url_for('get_user_movies', user_id=user_id))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)