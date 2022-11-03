from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager #helps us manage the logins

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__) # name of the file that was ran, this is how you initialize flask
    app.config['SECRET_KEY'] = 'randomstring here as secret key of our app'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' #my database is stored at sqlite:///{DB_NAME}
    
    db.init_app(app)

    # tell it about the blueprints we have
    from .views import views
    from .auth import auth

    # register the blueprints with our flask app
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Note #import the classes we made in models.py so we are sure they have ran before we initialize the database

    login_manager = LoginManager() # initialize login manager
    login_manager.login_view = 'auth.login' #where do we need to go if we are not logged in
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):  #tell flask how we load a user
        return User.query.get(int(id))

    create_database(app)

    return app

def create_database(app):
    #check if the database exists and if not create it
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all() #create the database, we pass app because we need to tell which app we create a db for
        print('Created Database!')
