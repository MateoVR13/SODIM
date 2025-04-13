import os

class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:840862@localhost/sodim_dm"
