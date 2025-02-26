from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from geopy.distance import geodesic
from app import mongo

shop_bp = Blueprint("shop", __name__)

@shop_bp.route("/create", methods=["POST"])
@jwt_required()  
def create_shop():
    vendor_email = get_jwt_identity()  

    if not vendor_email:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.get_json()

    last_shop = mongo.db.shops.find_one({}, sort=[("shop_id", -1)]) 
    shop_id = (last_shop["shop_id"] + 1) if last_shop else 1  #

    if not all(k in data for k in ("shop_name", "owner_name", "type", "latitude", "longitude")):
        return jsonify({"error": "Missing required fields"}), 400

    new_shop = {
        "shop_id": shop_id,
        "shop_name": data["shop_name"],
        "owner_name": data["owner_name"],
        "email" : vendor_email,
        "type": data["type"],
        "location": {  
            "type": "Point",
            "coordinates": [float(data["longitude"]), float(data["latitude"])]  
        }
    }

    mongo.db.shops.insert_one(new_shop)
    # print("Shop inserted:", new_shop) 
    return jsonify({"message": "Shop added successfully"}), 201
    

@shop_bp.route("/", methods=["GET"])
@jwt_required()
def get_shops():
    vendor_email = get_jwt_identity()
    shops = list(mongo.db.shops.find({"email": vendor_email}, {"_id": 0}))
    # print(shops)
    return jsonify(shops), 200

@shop_bp.route("/update/<int:shop_id>", methods=["PUT"])
@jwt_required()
def update_shop(shop_id):
    data = request.get_json()
    vendor_email = get_jwt_identity()

    updated_shop = mongo.db.shops.find_one_and_update(
        {"shop_id": shop_id, "email": vendor_email},  
        {"$set": data},
        return_document=True
    )

    if not updated_shop:
        return jsonify({"error": "Shop not found"}), 404

    return jsonify({"message": "Shop updated successfully"}), 200

@shop_bp.route("/delete/<int:shop_id>", methods=["DELETE"])
@jwt_required()
def delete_shop(shop_id):
    vendor_email = get_jwt_identity()

    result = mongo.db.shops.delete_one({"shop_id": shop_id, "email": vendor_email})  

    if result.deleted_count == 0:
        return jsonify({"error": "Shop not found"}), 404

    return jsonify({"message": "Shop deleted successfully"}), 200


@shop_bp.route("/nearby", methods=["GET"])
def find_nearby_shops():
    try:
        latitude = float(request.args.get("latitude"))
        longitude = float(request.args.get("longitude"))
        radius_km = float(request.args.get("radius", 50 )) 

        mongo.db.shops.create_index([("location", "2dsphere")])

        nearby_shops = mongo.db.shops.find({
            "location": {
                "$near": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": [longitude, latitude]
                    },
                    "$maxDistance": radius_km * 1000  
                }
            }
        })

        shop_list = []
        for shop in nearby_shops:
            shop["_id"] = str(shop["_id"])
            shop_list.append(shop)

        return jsonify({"shops": shop_list}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500