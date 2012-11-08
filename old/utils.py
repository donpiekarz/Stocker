
# global
import logging
import os

# project

import config 


def getLogger(app, level=config.logLevel):
	filename = app + '.log'
        path = os.path.join(config.logDir, filename)

	logging.basicConfig(filename=path, level=level, format=config.logFormat)
        logger = logging.getLogger(app)

        return logger

