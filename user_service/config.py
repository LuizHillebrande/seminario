import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-change-in-production")

    SQLALCHEMY_DATABASE_URI = os.getenv("USER_DATABASE_URL", f"sqlite:///{os.path.join(basedir, 'user.db')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False