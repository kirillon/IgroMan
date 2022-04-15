class Config(object):
    DATABASE_ENGINE = "postgresql"
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:0000@127.0.0.1:5432/test"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
