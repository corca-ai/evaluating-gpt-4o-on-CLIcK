import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create file handlers
fh = logging.FileHandler("debug.log")
fh.setLevel(logging.DEBUG)

# Add the handlers to the logger
logger.addHandler(fh)
