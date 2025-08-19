from models import db, User, Movie

class DataManager():
    def __init__(self):
        self.db = db

    def add_user(self, username):
        new_user = User(username=username)
        self.db.session.add(new_user)
        self.db.session.commit()
        return new_user

    def add_movie(self, title, director, year, poster_url, user_id):
        new_movie = Movie(title=title, director=director, year=year, poster_url=poster_url, user_id=user_id)
        self.db.session.add(new_movie)
        self.db.session.commit()
        return new_movie
    
    def get_user_movies(self, user_id):
        return Movie.query.filter_by(user_id=user_id).all()

    def get_all_users(self):
        return User.query.all()
    
    def update_movie(self, movie_id, new_title):
        movie = Movie.query.filter_by(id=movie_id).one()
        if movie:
            movie.title = new_title
            self.db.session.commit()
            return movie
        return None

    def delete_movie(self, movie_id):
        movie = Movie.query.filter_by(id=movie_id).one()
        if movie:
            self.db.session.delete(movie)
            self.db.session.commit()
            return True
        return False
        
            