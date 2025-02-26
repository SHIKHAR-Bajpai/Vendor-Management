from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv()

mongo = PyMongo()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config['MONGO_URI'] = os.getenv("MONGO_URI")  
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
    mongo.init_app(app)
    jwt.init_app(app)
    CORS(app)


    from app.routes import main
    app.register_blueprint(main)
    from app.auth import auth_bp
    from app.shop import shop_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(shop_bp, url_prefix="/shops")

    return app
