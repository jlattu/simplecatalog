from flask import *
import json
import catapp.catalog as catalog
from catapp.catalog import *


app = Flask(__name__)

open_database_connection(catalog)


@app.route("/")
def hello():
    return send_file("templates/index.html")


@app.route("/add_test_data")
def test_data():
    populate_test_data()
    return "Test data added!"


@app.route("/get_shirts")
def fetch_shirts():
    sorting_key = request.args.get('sorting_key')
    sorting_order = request.args.get('sorting_order')
    limit = 250
    offset = 0
    return jsonify(get_shirts(sorting_key, sorting_order, limit, offset)), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0')
