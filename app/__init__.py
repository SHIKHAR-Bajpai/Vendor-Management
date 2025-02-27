from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
    
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    with app.app_context():
        from app.models import Vendor, Shop
        db.create_all()
    
    from app.routes import main
    from app.auth import auth_bp
    from app.shop import shop_bp
    
    app.register_blueprint(main)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(shop_bp, url_prefix="/shops")
    
    return app
