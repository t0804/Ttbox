from core import app
from core import logger



if __name__ == "__main__":
    logger.setup_logger()
    logger = logger.get_logger(__name__)
    logger.debug('main.py run')
    app.run()
