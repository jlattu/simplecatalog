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
    limit = request.args.get('sorting_limit')
    offset = request.args.get('sorting_offset')
    return jsonify(get_shirts(sorting_key, sorting_order, limit, offset)), 200


@app.route("/add_new_shirt", methods=["POST"])
def add_new_shirt():
    json_data = request.get_json()
    try:
        name = json_data['name']
        color = json_data['color']
        amount = json_data['amount']
        price = json_data['price']
        size = json_data['size']
    except KeyError as e:
        print("Missing data: " + e.args[0])
        if str(e.args[0]) != "size":
            return abort(400, "Missing data other than size")
        print("Size will be M")
        size = 'M'
    add_shirt(name, color, size, amount, price)
    return "Shirt added"


@app.route("/delete_shirt", methods=["POST"])
def shirt_deletion():
    json_data = request.get_json()
    print(json_data)
    tel = {'jack': 4098, 'sape': 4139}
    print(tel)
    print(type(json_data))
    print(json_data['id'])
    try:
        shirt_id = int(json_data['id'])
    except KeyError as e:
        print("Missing data: " + e.args[0])
        return abort(400, "Missing id")
    delete_shirt(shirt_id)
    return "Shirt deleted!"


if __name__ == "__main__":
    app.run(host='0.0.0.0')
