from flask import Blueprint, jsonify
from db.connection import executeQuery

insightsBP = Blueprint("insights", __name__, url_prefix="/api/insights")

# GET /insights/restaurants/summary - gives the Restaurant summary view | cuisine, review count, avg rating, fav count per rest.
@insightsBP.route("/restaurants/summary", methods=["GET"])
def getRestaurantSum():
    rows = executeQuery("SELECT * FROM RestaurantSummary ORDER BY AvgRating DESC, ReviewCount DESC",
    fetch=True,
    )
    return jsonify(rows), 200

# GET /insights/top-restaurants gets the top 5 restaurants by the average rating; has to have min of 2 reviews to qualify
@insightsBP.route("/top-restaurants", methods=["GET"])
def getTopRestaurants():
    rows = executeQuery(
    """SELECT r.RestaurantID, r.Name, r.City, r.PriceRange,
            ROUND(AVG(rv.Rating), 2) AS AvgRating,
            COUNT(rv.ReviewID) AS ReviewCount
        FROM Restaurant r JOIN Review rv ON r.RestaurantID = rv.restaurantID
        GROUP BY  r.RestaurantID, r.Name, r.City, r.PriceRange
        HAVING COUNT(rv.ReviewID) >= 2 
        ORDER BY AvgRating DESC, ReviewCount DESC
        LIMIT 5""",
    fetch=True,
    )
    return jsonify(rows), 200

# GET /insights/schema/tables - metadata, lists all the tables in Curated Bites DB with row count
@insightsBP.route("/schema/tables", methods=["GET"])
def getSchemaTables():
    rows = executeQuery("""
        SELECT TABLE_NAME AS TableName, TABLE_ROWS AS EstimatedRows
        FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'CuratedBites'
        ORDER BY TABLE_NAME""",
    fetch=True,
    )
    return jsonify(rows), 200

# GET /insights/schema/indexes - metadata, lists all the indexes that are defined in the Curated Bites DB
@insightsBP.route("/schema/indexes", methods=["GET"])
def getSchemaIndexes():
    rows = executeQuery("""
        SELECT TABLE_NAME AS TableName, INDEX_NAME AS IndexName,
        COLUMN_NAME AS ColumnName, NON_UNIQUE AS NonUnique
        FROM INFORMATION_SCHEMA.STATISTICS WHERE TABLE_SCHEMA = 'CuratedBites'
        ORDER BY TABLE_NAME, INDEX_NAME, SEQ_IN_INDEX""",
    fetch=True,
    )
    return jsonify(rows), 200