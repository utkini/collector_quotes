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

    LOG.propagate = False


LOG = logging.getLogger(_bot_logger)

if not len(LOG.handlers):
    init_logger()
