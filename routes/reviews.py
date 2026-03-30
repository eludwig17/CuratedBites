from flask import Blueprint, request, jsonify
from db.connection import executeQuery

reviewsBP = Blueprint("reviews", __name__, url_prefix="/api/reviews")

# GET /api/reviews/restaurant/<restaurant_id> | return all reviews for a restaurant, newest first
@reviewsBP.route("/restaurant/<int:restaurant_id>", methods=["GET"])
def getReviewsForRestaurant(restaurant_id):
    rows = executeQuery(
        """SELECT r.ReviewID, r.Rating, r.Description, r.ReviewDate, u.Username
           FROM Review r JOIN Users u ON r.UserID = u.UserID
           WHERE r.RestaurantID = %s ORDER BY r.ReviewDate DESC""",
        (restaurant_id,),
        fetch=True,
    )
    return jsonify(rows), 200

# GET /api/reviews/<review_id> | returns a single review with author & restaurant
@reviewsBP.route("/<int:review_id>", methods=["GET"])
def getReview(review_id):
    row = executeQuery(
        """SELECT r.*, u.Username, res.Name AS RestaurantName
           FROM Review r JOIN Users u ON r.UserID = u.UserID
           JOIN Restaurant res ON r.RestaurantID = res.RestaurantID
           WHERE r.ReviewID = %s""",
        (review_id,),
        fetch_one=True,
    )
    if not row:
        return jsonify({"error": "Review doesn't exist"}), 404
    return jsonify(row), 200

# POST /api/reviews/ | creates a new review & requires UserID, RestaurantID, and Rating (1–5)
@reviewsBP.route("/", methods=["POST"])
def createReview():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON body required"}), 400
    required = ["UserID", "RestaurantID", "Rating"]
    missing  = [f for f in required if data.get(f) is None]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400
    try:
        rating = int(data["Rating"])
        if rating not in range(1, 6):
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "Rating must be an integer between 1 and 5"}), 400
    user = executeQuery(
        "SELECT UserID FROM Users WHERE UserID = %s",
        (data["UserID"],),
        fetch_one=True,
    )
    if not user:
        return jsonify({"error": "UserID does not exist"}), 400

    restaurant = executeQuery(
        "SELECT RestaurantID FROM Restaurant WHERE RestaurantID = %s",
        (data["RestaurantID"],),
        fetch_one=True,
    )
    if not restaurant:
        return jsonify({"error": "RestaurantID does not exist"}), 400

    new_id = executeQuery(
        """INSERT INTO Review (UserID, RestaurantID, Rating, Description, ReviewDate)
           VALUES (%s, %s, %s, %s, CURDATE())""",
        (
            data["UserID"], data["RestaurantID"], rating, data.get("Description"),
        ),
    )
    return jsonify({"message": "Review created", "ReviewID": new_id}), 201


# DELETE /api/reviews/<review_id> | delete a review by ID #
@reviewsBP.route("/<int:review_id>", methods=["DELETE"])
def deleteReview(review_id):
    existing = executeQuery(
        "SELECT ReviewID FROM Review WHERE ReviewID = %s",
        (review_id,),
        fetch_one=True,
    )
    if not existing:
        return jsonify({"error": "Review not found"}), 404
    executeQuery("DELETE FROM Review WHERE ReviewID = %s", (review_id,))
    return jsonify({"message": "Review deleted"}), 200