import os

from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://user:123456@188.243.57.73:29650/tree_base"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
