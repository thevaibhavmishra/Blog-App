from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

db = SQLAlchemy()       # instanciating SQLAlchemy() imported from flask_sqlalchemy
DB_NAME = 'blogapp.db'  #  name you want to give your database 

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "mY sUPER sECTREKEY"     # Secret key encrypt your app
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # setting SQLAlchemy url 
    db.init_app(app)        # this will configure the database with our app


    from .views import views
    app.register_blueprint(views, url_prefix = '/')

    from .models import User, Blog
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'views.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('instance/' + DB_NAME ):
        with app.app_context():
            print("Droppin g table")
            db.drop_all()
            db.create_all()
        print("Database Created")
 