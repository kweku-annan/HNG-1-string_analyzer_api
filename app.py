from flask import Flask, jsonify
from app.models.string_analyzer import StringAnalyzer
from app.schemas.dbStorage import DBStorage
from app.routes.string_routes import string_bp


# Create Flask app
app = Flask(__name__)

# Initialize storage
storage = DBStorage()

# Register blueprints
app.register_blueprint(string_bp)


@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to String Analyzer API!"}), 200

if __name__ == "__main__":
    app.run(debug=True)

