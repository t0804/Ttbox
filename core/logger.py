import logging
import sys
def setup_logger():
    logger = logging.getLogger('Ttbox')
    logger.setLevel(logging.DEBUG)
    # logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    logger.addHandler(handler)

    logger.debug('logger setup done')
#
def get_logger(name: str):
    if not name.startswith('Ttbox.'):
        name = f'Ttbox.{name}'
    return logging.getLogger(name)
