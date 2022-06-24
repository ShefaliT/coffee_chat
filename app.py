from flask import Flask, session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, logout_user



# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    ENV = 'prod'
    if ENV == 'dev':
        app.debug = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:shef@localhost/chatbot'
    else:
        app.debug = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://iocnuuuvfwlbrl:ec6b3e2d306ff777cb260b65e770435347be819bb5d2f081b1452fdfb121bc1a@ec2-3-229-252-6.compute-1.amazonaws.com:5432/d375sbm9t43v9i'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = '********'
   

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @app.before_request
    def before_request():

        session.permanent = False
        app.permanent_session_lifetime = timedelta(minutes=2)
        session.modified = True
        print("session runs")



    from models import User

    @login_manager.user_loader
    def load_user(user_id):
         # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
