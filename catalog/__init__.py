from flask import Flask, session,  redirect, url_for, request, current_app, g
import catalog.config
import sqlite3
import os
from pathlib import Path


project_folder = Path(__file__).parent.parent.resolve()
instance_folder = project_folder / 'instance'


# this app factory function copied from flask documention
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = catalog.config.SECRET_KEY,
        DATABASE=os.path.join(instance_folder, 'catalog.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        # os.makedirs(app.instance_path)
        os.makedirs(instance_folder)
    except OSError:
        pass
    
    from . import db
    db.init_app(app)
    
    if not os.path.exists(app.config['DATABASE']):
        with app.app_context():
            db.init_db()
    
    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import dashboard
    app.register_blueprint(dashboard.bp)
    app.add_url_rule('/', endpoint='index')
    
    return app

    
# flask --app catalog run 
# flask --app catalog run --debug

# default user:
# username: admin
# password: password

# this file and dashboard.py require a secret key and an API key. 
# these keys must be provided in a file titled 'config.py' with 
# the names SECRET_KEY and API_key. The secret key can be created 
# with a hashing program, the API key can be downloaded from google.