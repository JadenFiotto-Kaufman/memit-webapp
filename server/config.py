import logging

class Config:
    """Base config."""
    SECRET_KEY = 'secret_key'



class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False



class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True

    def __init__(self):
        super().__init__()

        logging.basicConfig(filename='debug.log')
