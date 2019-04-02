from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import logging
from parser import Parser

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

p = Parser()

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(80), unique=True)
    _games = db.Column(db.Text, unique=True)


@app.route('/TEST')
def get_categories():
    categories = [row._name for row in Category.query.with_entities(Category._name).all()]
    logging.info(f'Check DB. Found categories: {len(categories)}')
    if not categories:
        # parse page
        categories = [c.split('GAME_')[1] for c in list(filter(lambda link: 'GAME_' in link, p.parse_html(p.root_address)))]
        # add collected categories to db
        for c in categories:
            obj = Category()
            obj._name = c
            db.session.add(obj)
            db.session.commit()
            logging.info(f'Created an obj with category: {c}')
        logging.info(f'DB Updated. Found categories: {len(categories)}')
    # get list of bools if each cat has games:
    has_games = [(bool(Category.query.filter_by(_name = c).first()._games)) for c in categories]
    return render_template('categories.html', categories=zip(categories, has_games))


@app.route('/TEST/<category>', methods=['GET','POST'])
def get_category_games(category):
    row = Category.query.filter_by(_name = category).first()
    if row._games is None:
    # parse the page and save the data to db (update the category row)
        logging.info('PARSE NEW GAMES')
        games_list = p.get_games_by_category(category)
        add_games_to_db_row(row, games_list)
    return render_template('category.html', games = row._games.split(","), cat_link = category)

@app.route('/CATALOG')
def show_catalog():
    # create two lists: categories and list of games belong to each category. (data for html)
    all_categories = list()
    all_games = list()
    # iterate through all categories in DB
    for row in db.session.query(Category):
        # populate list of categories (data for html)
        all_categories.append(row._name)
        if row._games is None:
            print(f'GAMES NOT FOUND! for {row._name}')
            # parse the category page
            games_list = p.get_games_by_category(row._name)
            # write the dict to DB
            add_games_to_db_row(row, games_list)
            # populate list of games (data for html)
            all_games.append(games_list)
        else:
            all_games.append(row._games.split(","))
    return render_template('catalog.html', catalog = zip(all_categories, all_games))

@app.route('/ALL_DATA_IN_DB_IS_REMOVED')
def empty_db():
    num_rows_deleted = db.session.query(Category).delete()
    db.session.commit()
    return render_template('clear_db_message.html')


def add_games_to_db_row(row: object, games: list)-> None:
    ''' Update object(game category) with games in DB'''
    row._games = ",".join([str(x) for x in games])
    db.session.commit()


@app.route('/')
def search_games():
    search = request.args.get('search')
    if search:
        search_results = p.get_games_by_keyword(search)
        return render_template('search_result.html', categories={search: search_results})
    else:
        return render_template('index.html')
