from flask import *
import catapp.catalog as catalog
from catapp.catalog import *


app = Flask(__name__)

open_database_connection(catalog)


@app.route("/")
def hello():
    return send_file("templates/index.html")


@app.route("/add_test_data")
def test_data():
    added_shirts = populate_test_data()
    return str(added_shirts) + " new shirts added as a test data!"


@app.route("/get_shirts")
def fetch_shirts():
    """Gets shirts from database using parameters to narrow results down.

    :return: Information about shirts gathered with parameter
    """
    name = request.args.get('name')
    sorting_key = request.args.get('sorting_key')
    sorting_order = request.args.get('sorting_order')
    limit = request.args.get('sorting_limit')
    offset = request.args.get('sorting_offset')
    result = get_shirts(name, sorting_key, sorting_order, limit, offset)
    total_count = get_shirt_count(name)
    shirts = {'total_count': total_count, 'shirts': result}
    return jsonify(shirts), 200


@app.route("/add_new_shirt", methods=["POST"])
def add_new_shirt():
    """Adds new base to database.

    :return: Confirmation of new shirt getting added to databe
    """
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
    return "Shirt added to database"


@app.route("/update_shirt", methods=["POST"])
def edit_shirt():
    """Route for updating shirt with new information by using its id as identifier

    :return: Confirmation of updating
    """
    json_data = request.get_json()
    print(json_data)
    try:
        shirt_id = json_data['id']
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
    update_shirt(shirt_id, name, color, size, amount, price)
    return "Shirt information updated"


@app.route("/delete_shirt", methods=["POST"])
def shirt_deletion():
    """Route for deleting a shirt by using its id as identifier

    :return: Confirmation of deletion
    """
    json_data = request.get_json()
    try:
        shirt_id = int(json_data['id'])
    except KeyError as e:
        print("Missing data: " + e.args[0])
        return abort(400, "Missing id")
    delete_shirt(shirt_id)
    return "Shirt deleted from database"


@app.route("/delete_all_shirts", methods=["POST"])
def nuke_it_down():
    """Route for deleting a shirt by using its id as identifier

    :return: Confirmation of deletion
    """
    delete_all_shirts()
    return "I love the smell of napalm in the morning"


if __name__ == "__main__":
    app.run()
