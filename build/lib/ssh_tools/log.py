#! /usr/bin/python3

import logging


def get_logger(name, verbose=False):
    log_formatter = logging.Formatter('\n\t[%(levelname)s] %(message)s\n')
    log = logging.getLogger(name)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    log.addHandler(console_handler)

    set_verbose(log, verbose)

    return log

def set_verbose(log: logging.Logger, verbose:bool):
    if verbose:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.WARNING)
