from flask import Blueprint, request, jsonify
from db.connection import executeQuery

restaurantsBP = Blueprint("restaurants", __name__, url_prefix="/api/restaurants")

# GET /api/restaurants/ | return all restaurants, optionally filtered by city and or the price range
@restaurantsBP.route("/", methods=["GET"])
def getRestaurants():
    city = request.args.get("city")
    priceRange = request.args.get("priceRange")
    query  = "SELECT * FROM Restaurant WHERE 1=1"
    params = []
    if city:
        query += " AND City = %s"
        params.append(city)
    if priceRange:
        if not str(priceRange).isdigit() or int(priceRange) not in range(1, 5):
            return jsonify({"error": "priceRange must be an integer between 1 and 4"}), 400
        query += " AND PriceRange = %s"
        params.append(int(priceRange))
    query += " ORDER BY Name"
    results = executeQuery(query, tuple(params), fetch=True)
    return jsonify(results), 200

# GET /api/restaurants/<restaurant_id> | return restaurant by ID #
@restaurantsBP.route("/<int:restaurant_id>", methods=["GET"])
def getRestaurant(restaurant_id):
    row = executeQuery(
        "SELECT * FROM Restaurant WHERE RestaurantID = %s",
        (restaurant_id,),
        fetch_one=True,
    )
    if not row:
        return jsonify({"error": "Restaurant not found"}), 404
    return jsonify(row), 200

# POST /api/restaurants/ | create a new restaurant & requires Name, Address, City, Phone, and PriceRange (1–4)
@restaurantsBP.route("/", methods=["POST"])
def createRestaurant():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON body required"}), 400

    required = ["Name", "Address", "City", "Phone", "PriceRange"]
    missing  = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400
    try:
        price = int(data["PriceRange"])
        if price not in range(1, 5):
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "PriceRange must be an integer between 1 and 4"}), 400

    new_id = executeQuery(
        """INSERT INTO Restaurant (Name, Address, City, Phone, Website, Description, Hours, PriceRange)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
        (
            data["Name"], data["Address"], data["City"], data["Phone"], data.get("Website"), data.get("Description"), data.get("Hours"), price,
        ),
    )
    return jsonify({"message": "Restaurant created", "RestaurantID": new_id}), 201

# PUT /api/restaurants/<restaurant_id> | update one or more fields of existing restaurant
@restaurantsBP.route("/<int:restaurant_id>", methods=["PUT"])
def updateRestaurant(restaurant_id):
    existing = executeQuery(
        "SELECT RestaurantID FROM Restaurant WHERE RestaurantID = %s",
        (restaurant_id,),
        fetch_one=True,
    )
    if not existing:
        return jsonify({"error": "Restaurant not found"}), 404
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON body required"}), 400
    updatable = ["Name", "Address", "City", "Phone", "Website", "Description", "Hours", "PriceRange"]
    fields, values = [], []

    for field in updatable:
        if field in data:
            if field == "PriceRange":
                try:
                    val = int(data[field])
                    if val not in range(1, 5):
                        raise ValueError
                except (ValueError, TypeError):
                    return jsonify({"error": "PriceRange must be 1–4"}), 400
                values.append(val)
            else:
                values.append(data[field])
            fields.append(f"{field} = %s")
    if not fields:
        return jsonify({"error": "No valid fields to update"}), 400

    values.append(restaurant_id)
    executeQuery(
        f"UPDATE Restaurant SET {', '.join(fields)} WHERE RestaurantID = %s",
        tuple(values),
    )
    return jsonify({"message": "Restaurant information updated"}), 200

# DELETE /api/restaurants/<restaurant_id> | delete a restaurant by ID #
@restaurantsBP.route("/<int:restaurant_id>", methods=["DELETE"])
def deleteRestaurant(restaurant_id):
    existing = executeQuery(
        "SELECT RestaurantID FROM Restaurant WHERE RestaurantID = %s",
        (restaurant_id,),
        fetch_one=True,
    )
    if not existing:
        return jsonify({"error": "Restaurant not found"}), 404
    executeQuery(
        "DELETE FROM Restaurant WHERE RestaurantID = %s",
        (restaurant_id,),
    )
    return jsonify({"message": "Restaurant deleted"}), 200