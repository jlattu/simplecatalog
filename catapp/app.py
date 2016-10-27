from flask import Flask
import catapp.catalog as catalog
from catapp.catalog import *


app = Flask(__name__)

open_database_connection(catalog)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/add_test_data")
def test_data():
    populate_test_data()
    return "Test data added!"


if __name__ == "__main__":
    app.run()
