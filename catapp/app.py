from flask import Flask, render_template
import json
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


@app.route("/get_shirts")
def asd_shirts():
    return render_template('shirts.html', result=get_shirts())


if __name__ == "__main__":
    app.run()
