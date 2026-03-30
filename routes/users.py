from flask import Blueprint, request, jsonify
from db.connection import executeQuery

usersBP = Blueprint("users", __name__, url_prefix="/api/users")

# GET /api/users/ | return all users sorted by username, excluding passwords
@usersBP.route("/", methods=["GET"])
def getUsers():
    rows = executeQuery(
        "SELECT UserID, Username, Email, CreationDate FROM Users ORDER BY Username",
        fetch=True,
    )
    return jsonify(rows), 200

# GET /api/users/<user_id> | return a single user by their ID, excluding password
@usersBP.route("/<int:user_id>", methods=["GET"])
def getUser(user_id):
    row = executeQuery(
        "SELECT UserID, Username, Email, CreationDate FROM Users WHERE UserID = %s",
        (user_id,),
        fetch_one=True,
    )
    if not row:
        return jsonify({"error": "User not found"}), 404
    return jsonify(row), 200

# POST /api/users/ | register a new user & requires Username, Email, and Password (min 6 characters) and the password stored as SHA-256 hash
@usersBP.route("/", methods=["POST"])
def createUser():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON body required"}), 400

    required = ["Username", "Email", "Password"]
    missing  = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400
    if "@" not in data["Email"]:
        return jsonify({"error": "Invalid email address"}), 400
    if len(data["Password"]) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400
    # Checks for duplicate username or email
    dup = executeQuery(
        "SELECT UserID FROM Users WHERE Username = %s OR Email = %s",
        (data["Username"], data["Email"]),
        fetch_one=True,
    )
    if dup:
        return jsonify({"error": "Username or email is already in use"}), 409
    new_id = executeQuery(
        """INSERT INTO Users (Username, Email, Password, CreationDate)
           VALUES (%s, %s, SHA2(%s, 256), CURDATE())""",
        (data["Username"], data["Email"], data["Password"]),
    )
    return jsonify({"message": "User created", "UserID": new_id}), 201

# GET /api/users/<user_id>/favorites | returns all favorite restaurants for a user
@usersBP.route("/<int:user_id>/favorites", methods=["GET"])
def getUserFavorites(user_id):
    user = executeQuery(
        "SELECT UserID FROM Users WHERE UserID = %s", (user_id,), fetch_one=True
    )
    if not user:
        return jsonify({"error": "User not found"}), 404

    rows = executeQuery(
        """SELECT f.FavoriteID, r.RestaurantID, r.Name, r.City, r.PriceRange
           FROM Favorite f JOIN Restaurant r ON f.RestaurantID = r.RestaurantID
           WHERE f.UserID = %s ORDER BY r.Name""",
        (user_id,),
        fetch=True,
    )
    return jsonify(rows), 200

# POST /api/users/<user_id>/favorites | add a restaurant to a user's favorites & requires RestaurantID
@usersBP.route("/<int:user_id>/favorites", methods=["POST"])
def addFavorite(user_id):
    data = request.get_json(silent=True)
    if not data or not data.get("RestaurantID"):
        return jsonify({"error": "RestaurantID is required"}), 400

    user = executeQuery(
        "SELECT UserID FROM Users WHERE UserID = %s", (user_id,), fetch_one=True
    )
    if not user:
        return jsonify({"error": "User not found"}), 404
    restaurant = executeQuery(
        "SELECT RestaurantID FROM Restaurant WHERE RestaurantID = %s",
        (data["RestaurantID"],),
        fetch_one=True,
    )
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404
    dup = executeQuery(
        "SELECT FavoriteID FROM Favorite WHERE UserID = %s AND RestaurantID = %s",
        (user_id, data["RestaurantID"]),
        fetch_one=True,
    )
    if dup:
        return jsonify({"error": "Already in favorites"}), 409
    new_id = executeQuery(
        "INSERT INTO Favorite (UserID, RestaurantID) VALUES (%s, %s)",
        (user_id, data["RestaurantID"]),
    )
    return jsonify({"message": "Favorite added", "FavoriteID": new_id}), 201