from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models import Vendor

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    required_fields = ["name", "email", "password"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    existing_vendor = Vendor.query.filter_by(email=data["email"]).first()
    if existing_vendor:
        return jsonify({"error": "Vendor already exists"}), 400

    hashed_password = generate_password_hash(data["password"])
    new_vendor = Vendor(name=data["name"], email=data["email"], password=hashed_password)
    db.session.add(new_vendor)
    db.session.commit()

    return jsonify({"message": "Vendor registered successfully"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    vendor = Vendor.query.filter_by(email=data["email"]).first()

    if not vendor or not check_password_hash(vendor.password, data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=vendor.email)
    return jsonify({"access_token": access_token}), 200

@auth_bp.route("/update", methods=["PUT"])
@jwt_required()
def update_vendor():
    vendor_email = get_jwt_identity()
    data = request.get_json()

    vendor = Vendor.query.filter_by(email=vendor_email).first()
    if not vendor:
        return jsonify({"error": "Vendor not found"}), 404

    if "name" in data:
        vendor.name = data["name"]
    if "password" in data:
        vendor.password = generate_password_hash(data["password"])
    
    db.session.commit()
    return jsonify({"message": "Vendor updated successfully"}), 200

@auth_bp.route("/delete", methods=["DELETE"])
@jwt_required()
def delete_vendor():
    vendor_email = get_jwt_identity()

    vendor = Vendor.query.filter_by(email=vendor_email).first()
    if not vendor:
        return jsonify({"error": "Vendor not found"}), 404

    db.session.delete(vendor)
    db.session.commit()

    return jsonify({"message": "Vendor deleted successfully"}), 200
