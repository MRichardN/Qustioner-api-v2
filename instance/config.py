"""
    Configuration
"""
import os

class Config(object):
    """Parent configuration class."""
    DEBUG = False
    TESTING = False
    
    DATABASE_HOST = os.getenv('DATABASE_HOST')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
    DATABASE_USER = os.getenv('DATABASE_USER')
    DATABASE_PORT = os.getenv('DATABASE_PORT')
    
    SECRET = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']



class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True
    DATABASE_NAME = os.getenv('DATABASE_NAME')


class TestingConfig(Config):
    """Configurations for Testing; with a separate test database."""
    TESTING = True
    DATABASE_NAME = os.getenv('TEST_DB')


class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True
    DATABASE_NAME = os.getenv('TEST_DB')

class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False
    DATABASE_NAME = os.getenv('DATABASE_NAME')

app_config = {
    'development' : DevelopmentConfig,
    'testing' : TestingConfig,
    'staging' : StagingConfig,
    'production' : ProductionConfig
}
