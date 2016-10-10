import os
basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = 'thisissecretkey'

SQLALCHEMY_DATABASE_URI = 'mysql://root:Motylek80@localhost/Harmony_Data_Test'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

