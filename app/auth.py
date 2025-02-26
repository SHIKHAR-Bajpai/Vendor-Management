from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token , jwt_required , get_jwt_identity
from werkzeug.security import generate_password_hash
from app import mongo

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    
    required_fields = [ "name", "email", "password"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    if mongo.db.vendors.find_one({"email": data["email"]}):
        return jsonify({"error": "Vendor already exists"}), 400

    hashed_password = generate_password_hash(data["password"])

    mongo.db.vendors.insert_one({
        "name": data["name"],    
        "email": data["email"],  
        "password": hashed_password
    })

    # print(data)
    return jsonify({"message": "Vendor registered successfully"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    vendor = mongo.db.vendors.find_one({"email": data["email"]})

    # print(vendor)

    if not vendor or not check_password_hash(vendor["password"], data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=vendor["email"])
    return jsonify({"access_token": access_token}), 200


@auth_bp.route("/update", methods=["PUT"])
@jwt_required() 
def update_vendor():
    vendor_email = get_jwt_identity() 

    data = request.get_json()

    if not any(field in data for field in ["name", "password"]):
        return jsonify({"error": "No fields to update"}), 400

    vendor = mongo.db.vendors.find_one({"email": vendor_email})

    if not vendor:
        return jsonify({"error": "Vendor not found"}), 404

    updated_data = {}

    if "name" in data:
        updated_data["name"] = data["name"]

    if "password" in data:
        updated_data["password"] = generate_password_hash(data["password"])

    mongo.db.vendors.update_one({"email": vendor_email}, {"$set": updated_data})

    return jsonify({"message": "Vendor updated successfully"}), 200


@auth_bp.route("/delete", methods=["DELETE"])
@jwt_required() 
def delete_vendor():
    vendor_email = get_jwt_identity()  

    vendor = mongo.db.vendors.find_one({"email": vendor_email})

    if not vendor:
        return jsonify({"error": "Vendor not found"}), 404

    mongo.db.vendors.delete_one({"email": vendor_email})

    return jsonify({"message": "Vendor deleted successfully"}), 200