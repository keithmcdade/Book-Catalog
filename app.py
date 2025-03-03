from catalog.__init__ import create_app
from catalog.db import init_db
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""This is a web app built with flask,
                                     for searching and cataloging books using the Google Books API.
                                     \nCurrently only supports searches with ISBN-13, formatted with no dashes.""")
    parser.add_argument("--debug", help="run app with debugger", 
                        action="store_true")
    args = parser.parse_args()
    if args.debug:
        create_app().run(debug=True)
    else:
        create_app().run()