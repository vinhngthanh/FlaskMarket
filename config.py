import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    
    @staticmethod
    def init_app(app):
        app.config["SESSION_PERMANENT"] = False
        app.config["SECRET_KEY"] = "secret_key"
        
class DevelopmentConfig(Config):
    DEBUG = True
    # Testing use different database than production
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"

class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    # Testing use different database than production
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    
class ProductionConfig(Config):
    DEBUG = False
    # Use app.db database
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": ProductionConfig
}