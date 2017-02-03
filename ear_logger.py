"""Creates and manages a singleton logger instance.
                    
@author:     jolin

@copyright:  2017 xMatters, Inc. All rights reserved.

@license:    Apache License 2.0
             http://www.apache.org/licenses/LICENSE-2.0

@contact:    jolin@xmatters.com
@deffield    updated: 2017-01-28

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import logging
from logging import config as logging_config
import config

_logger = None

def get_logger():
    """Returns the existing logger or creates a new one if the first time
    
    Used the values specified in the config module to determine the log
    filename, log level (based on verbosity), and whether a console handler
    should be included based on the noisy flag.
    The method will only create a singleton logger that is requested by and
    shared across modules.

    Returns:
        An instance of a logger
    """
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
