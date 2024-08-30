# app.py
'''
Sets up the Flask application (app) and the SQLAlchemy instance (db).
imports the database models to ensure they are registered with SQLAlchemy.
Creates the database tables within an application context using db.create_all()

'''
from flask_migrate import Migrate
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db
from flask import Flask, render_template
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer

mail = Mail()
serializer = URLSafeTimedSerializer(Config.SECRET_KEY) 
def create_app():
    # intialize the flask application
    app = Flask(__name__)
    app.config.from_object(Config)

    #initialize database and migration
    db.init_app(app)
    migrate = Migrate(app, db)
    mail.init_app(app)


    # import blue prints
    from routes.auth_routes import  auth_bp
    from routes.page_routes import page_bp 



    # Register blueprinti
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(page_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    # Run the Flask application in debug mode
    app.run(debug=True)
