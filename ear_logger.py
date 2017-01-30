'''
Created on Jan 28, 2017

@author: jolin
'''

import logging
from logging import config as logging_config
import config

_logger = None

def get_logger():
    global _logger, _config_called
    verbosity = config.verbosity
    log_path = config.log_filename
    noisy = config.noisy
    if (_logger is not None):
        return _logger
    name = 'default'
    logLevels = ['ERROR','WARNING','INFO','DEBUG']
    level = logLevels[verbosity]
    cLevel = logLevels[verbosity] if noisy else 'ERROR'
    handlers = ['file','console']
    logging_config.dictConfig({
        'version': 1,
        'formatters': {
            'default': {'format': '%(asctime)s - %(levelname)s - %(message)s', 'datefmt': '%Y-%m-%d %H:%M:%S'}
        },
        'handlers': {
            'console': {
                'level': cLevel,
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'level': level,
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'default',
                'filename': log_path,
                'maxBytes': (10*1024*1024),
                'backupCount': 3,
                'mode': 'a'
            }
        },
        'loggers': {
            'default': {
                'level': level,
                'handlers': handlers
            }
        },
        'disable_existing_loggers': False
    })
    _logger = logging.getLogger(name)
    return _logger
        
def main():
    pass

if __name__ == '__main__':
    main()
