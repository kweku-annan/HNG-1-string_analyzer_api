from flask import Flask, jsonify
from api.schemas.dbStorage import DBStorage
from api.routes.string_routes import string_bp


# Create Flask api
app = Flask(__name__)

# Initialize storage
storage = DBStorage()

# Register blueprints
app.register_blueprint(string_bp)


@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to String Analyzer API!"}), 200

# if __name__ == "__main__":
#     api.run(debug=True)

