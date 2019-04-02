# GooglePlay Game Parser

The application  (Selenium -> Flask) collects games name (in googleplay dot-separated format) by parsing them through GooglePlay website.

## How to run

To run the programm:

* create new  and activate venv
* install all required depencies: ```pip install -r requirements.txt ```
* run the application: ```flask run``` (_or_ ```DEBUG=1 flask run```)

Optionally (to create new sqlite db):
* delete old db
* run python3
* from app import db
* db.create_all()

## How it works

Script automatically open chrome window managed by selenium. The window not switched to hidden mode to see what pages the parser visits. Do not close it while using the parser.

Flask applications started by default at address: http://127.0.0.1:5000  
Initial application page located at http://127.0.0.1:5000/TEST  
All the data parsing executes in idle mode.

* __Parse all__  button. Click on it initaltes parsing all the categories not parsed yet. All collected data stored to db.
* __Delete collected data__ button. Click on it initaltes deleting all the data in db.
* __Search form__ Any text might be inputed to the form. Application will call the parser to collect all games found on GooglePlay search page with the same keywords.
* The page shows a table with a list of game categories and a status of each. Any category might be already parsed or not. If no categories found at db(sqlite), then parser collects them to show at the page. If db contains any of them already, then the data will be taken from the db. Each category name is a link to category-page. Last one contains The category name and list of games founded by the parser.

Page http://127.0.0.1:5000//CATALOG contains a list of categories. Each one realised as drop-down menu with a games belonged to the category.

It's possible to use 'search' in 'manual' mode. Just go to link
http://127.0.0.1:5000/?search={keywords}, where {keywords} is a keyword you're interested in.

## Files

### parser.py

Contains a class ```Parser```. When application starts, one insanse of the class initiated. All parsing is executed by it. 


### app.py 
Flask application file.


### templates/
Several html files, nothing special.

### requirements.txt
Contains a list prerequisites.

### test.db
SQLite database. Contains only one minimal table with class "Category".

### Other comments
The application execution is well-logged. It might be helpful for debug or modification.