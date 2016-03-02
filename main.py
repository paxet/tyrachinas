#!/usr/bin/env python3
import argparse
import webapp
from webapp import app, db
from webapp.models import Resource
import config

__author__ = 'paxet'

db_tables = [Resource]


def get_app():
    """Return the application object."""
    # Don't loose sesions between restarts while coding
    app.config['SECRET_KEY'] = 'development_secret'
    app.config['WTF_CSRF_KEY'] = 'development_csrf_key'
    app.config['WTF_CSRF_SECRET_KEY'] = 'development_csrf_secret'
    return app


def class_for_name(module_name, class_name):
    """Credit goes to m.kocikowski --> http://stackoverflow.com/a/13808375"""
    # load the module, will raise ImportError if module cannot be loaded
    m = importlib.import_module(module_name)
    # get the class, will raise AttributeError if class cannot be found
    c = getattr(m, class_name)
    return c


def create_tables():
    if db.get_db().is_closed():
        db.get_db().connect()
    db.get_db().create_tables(db_tables)
    print('Tables created')


def create_one(table):
    if db.get_db().is_closed():
        db.get_db().connect()
    try:
        c = class_for_name("webapp", table)
    except (ImportError, AttributeError) as err:
        print('No such table: {}'.format(table))
    else:
        db.get_db().create_tables([c])
        print('Table {} created'.format(table))


def drop_tables():
    if db.get_db().is_closed():
        db.get_db().connect()
    db.get_db().drop_tables(db_tables)
    print('Tables dropped')


def interpret_args(args):
    commands = []
    if args.create:
        commands.append(create_tables)
    if args.create_one:
        raise  NotImplementedError
        # commands.append(lambda: create_one(Table))
    if args.drop:
        commands.append(drop_tables)
    if args.webserver:
        # toolbar = DebugToolbarExtension(app)
        commands.append(lambda: get_app().run(debug=True))
    if len(commands) > 0:
        for command in commands:
            command()
    else:
        parser.print_help()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='{appname} web project: simple share and host web app'.format(appname=config.APP_NAME))
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-c', '--create',
                       help='Create tables in Database',
                       action='store_true')
    group.add_argument('-o', '--create_one',
                       help='Create only one Database table')
    group.add_argument('-d', '--drop',
                       help='Drop all Database tables',
                       action='store_true',)
    group.add_argument('-w', '--webserver',
                       help='Launch web app with the Flask integrated server',
                       action='store_true',)
    parser.add_argument('--version',
                        action='version', version='%(prog)s for {appname} {version}'.format(appname=config.APP_NAME, version=webapp.__version__))

    interpret_args(parser.parse_args())
