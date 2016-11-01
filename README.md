# simplecatalog
Simple product catalog with UI and backend

Current functionality:
* Adding / removing / editing products
* Searching product by matching the beginning of product name
* Option to query 25, 50, 100, 250 or all products at once with pagination
* Possibility to sort results by any sorting key (by pressing table headers)
  * Clicking the same sorting key toggles between ascending and descending
* Deleting all data at once so catalog can once again be filled with glorious lorem ipsum shirts (test data has 500 of them)
  
Made with:
* Python
* Flask
* SQLite
* AngularJS

Currently lacking:
* Tests for AngularJS (catalog.py is unit tested)

Needs Python and Flask installed to be able to run