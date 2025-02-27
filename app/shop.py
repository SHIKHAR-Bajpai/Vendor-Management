from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import text
from app import db
from app.models import Shop

shop_bp = Blueprint("shop", __name__)

@shop_bp.route("/create", methods=["POST"])
@jwt_required()
def create_shop():
    vendor_email = get_jwt_identity()
    data = request.get_json()

    if not all(k in data for k in ("shop_name", "owner_name", "type", "latitude", "longitude")):
        return jsonify({"error": "Missing required fields"}), 400

    new_shop = Shop(
        shop_name=data["shop_name"],
        owner_name=data["owner_name"],
        email=vendor_email,
        type=data["type"],
        latitude=data["latitude"],
        longitude=data["longitude"]
    )

    db.session.add(new_shop)
    db.session.commit()

    return jsonify({"message": "Shop added successfully"}), 201

@shop_bp.route("/", methods=["GET"])
@jwt_required()
def get_shops():
    vendor_email = get_jwt_identity()
    shops = Shop.query.filter_by(email=vendor_email).all()
    shop_list = [{"shop_id": shop.id, "shop_name": shop.shop_name, "owner_name": shop.owner_name, "type": shop.type, "latitude": shop.latitude, "longitude": shop.longitude} for shop in shops]
    return jsonify(shop_list), 200

@shop_bp.route("/update/<int:shop_id>", methods=["PUT"])
@jwt_required()
def update_shop(shop_id):
    vendor_email = get_jwt_identity()
    data = request.get_json()
    
    shop = Shop.query.filter_by(id=shop_id, email=vendor_email).first()
    if not shop:
        return jsonify({"error": "Shop not found"}), 404

    for key, value in data.items():
        setattr(shop, key, value)
    
    db.session.commit()
    return jsonify({"message": "Shop updated successfully"}), 200

@shop_bp.route("/delete/<int:shop_id>", methods=["DELETE"])
@jwt_required()
def delete_shop(shop_id):
    vendor_email = get_jwt_identity()
    shop = Shop.query.filter_by(id=shop_id, email=vendor_email).first()
    if not shop:
        return jsonify({"error": "Shop not found"}), 404

    db.session.delete(shop)
    db.session.commit()
    return jsonify({"message": "Shop deleted successfully"}), 200



@shop_bp.route("/nearby", methods=["GET"])
def get_nearby_shops():
    try:
        latitude = request.args.get('latitude')
        longitude = request.args.get('longitude')
        radius = request.args.get("radius", default=5000, type=float)

        if latitude is None or longitude is None:
            return jsonify({"error": "Latitude and Longitude are required"}), 400
        
        latitude = float(latitude)
        longitude = float(longitude)
        radius = float(radius)


        query = text("""
            SELECT id, shop_name, owner_name, type, latitude, longitude,
                (6371 * acos(cos(radians(:lat)) * cos(radians(latitude))
                * cos(radians(longitude) - radians(:lng))
                + sin(radians(:lat)) * sin(radians(latitude))))
                AS distance
            FROM shop
            WHERE (6371 * acos(cos(radians(:lat)) * cos(radians(latitude))
                * cos(radians(longitude) - radians(:lng))
                + sin(radians(:lat)) * sin(radians(latitude)))) < :radius
            ORDER BY distance;
        """)

        result = db.session.execute(query, {"lat": latitude, "lng": longitude, "radius": radius})
        shops = [dict(row._asdict()) for row in result]  
        return jsonify(shops)

    except ValueError:
        return jsonify({'error': 'Invalid latitude, longitude, or radius'}), 400
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500