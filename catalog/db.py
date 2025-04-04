import sqlite3
import click
from flask import current_app, g
from werkzeug.security import generate_password_hash

def get_db():
    
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
        
        # included a default account. username = admin | password = password
        username = "admin"
        password = "password"
        sql = "INSERT INTO users (username, user_password) VALUES (?, ?)"
        db.execute(sql, (username, generate_password_hash(password)),)
        db.commit()

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    
# command to initialize db:
# flask --app catalog init-db 
