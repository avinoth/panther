import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
CSRF_ENABLED = True
SECRET_KEY = 'rc#41he@q$o&w^019_h1%)-41-6^omcb5x3c14cd22dcz8r*tl'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')