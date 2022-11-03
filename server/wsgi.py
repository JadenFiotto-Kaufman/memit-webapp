import logging
from .api import app

if __name__ == "__main__":

    app.config.from_object('config.ProdConfig')

    # gunicorn_logger = logging.getLogger('gunicorn.error')
    # app.logger.handlers = gunicorn_logger.handlers
    # app.logger.setLevel(gunicorn_logger.level)

    app.run()