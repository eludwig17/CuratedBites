from flask import Flask, jsonify
from routes.restaurants import restaurantsBP
from routes.reviews import reviewsBP
from routes.users import usersBP
import os
os.environ.setdefault("FLASK_APP", "app.py")
FLASK_APP="app.py"
FLASK_DEBUG=1
app = Flask(__name__)
app.register_blueprint(restaurantsBP)
app.register_blueprint(reviewsBP)
app.register_blueprint(usersBP)

@app.route('/')
def index():
    return jsonify({
        "app": "Curated Bites API",
        "status": "running",
        "routes": {
            "restaurants": "/api/restaurants",
            "reviews": "/api/reviews",
            "users": "/api/users",
        }
    }), 200

if __name__ == '__main__':
    app.run(debug=True)