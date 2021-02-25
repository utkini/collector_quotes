import logging
import sys
import warnings

log_level = logging.INFO
_bot_logger = 'FinTechLogger'
logging_format = '[%(levelname)s] %(asctime)s %(filename)s:%(funcName)s:%(lineno)s: %(message)s'


def init_logger() -> None:
    """ initialization default logger

    :return: logger
    """
    # if logger already initialized
    if len(LOG.handlers):
        warnings.warn('duplicated logger initialization')
        return
    formatter = logging.Formatter(logging_format)
    LOG.setLevel(log_level)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.set_name('console_handler')
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    LOG.addHandler(console_handler)
    #
    # time = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
    # file_name = f'log_{time}.log'
    # file_path = Path('/app/logs') / file_name
    # file_handler = logging.FileHandler(str(file_path))
    # file_handler.set_name('file_handler')
    # file_handler.setLevel(log_level)
    # file_handler.setFormatter(formatter)
    # LOG.addHandler(file_handler)

    LOG.propagate = False


LOG = logging.getLogger(_bot_logger)

if not len(LOG.handlers):
    init_logger()
