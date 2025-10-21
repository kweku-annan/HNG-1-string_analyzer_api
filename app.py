from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    profile = {
        "First name": "Emmanuel",
        "Last name": "Saah",
        "Role": "Backend Engineer"
    }
    return jsonify(profile)


if __name__ == "__main__":
    app.run(debug=True)

