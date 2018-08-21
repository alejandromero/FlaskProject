import os

class BasicConfig(object):
    DEBUG = False
    SECRET_KEY = "prueba"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DebugConfig(BasicConfig):
    DEBUG = True

class PDBConfig(BasicConfig): #PDB = Permanent Data Base
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.abspath("") + "/database.db"

class DebugDBConfig(DebugConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.abspath("") + "/database.db"