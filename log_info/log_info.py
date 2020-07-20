#!/usr/bin/env python3
"""
Create a logger object and associate it with files for each level of logging.
"""
import logging

# create a debug logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# format it's output
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

# declare file for each level of output
# debug
file_handler = logging.FileHandler('debug.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
# assign debug file and stream handler to logger
logger.addHandler(file_handler)

# info
file_handler = logging.FileHandler('info.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
# assign info file and stream handler to logger
logger.addHandler(file_handler)

# warning
file_handler = logging.FileHandler('warning.log')
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)
# assign warning file and stream handler to logger
logger.addHandler(file_handler)

# error
file_handler = logging.FileHandler('error.log')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)
# assign error file and stream handler to logger
logger.addHandler(file_handler)

# critical
file_handler = logging.FileHandler('critical.log')
file_handler.setLevel(logging.CRITICAL)
file_handler.setFormatter(formatter)
# assign critical file and stream handler to logger
logger.addHandler(file_handler)




