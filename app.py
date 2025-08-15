from flask import Flask, request, jsonify
from data_manager import DataManager
from models import db, Movie


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'

db.init_app(app)

data_manager = DataManager()


@app.route('/')
def home():
    return "Welcome to MoviWeb App!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)