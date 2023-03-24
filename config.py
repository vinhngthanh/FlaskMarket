import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    
    @staticmethod
    def init_app(app):
        app.config["SESSION_PERMANENT"] = False
        app.config["SECRET_KEY"] = "secret_key"
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

        
class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    
class ProductionConfig(Config):
    DEBUG = False
    
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": ProductionConfig
}