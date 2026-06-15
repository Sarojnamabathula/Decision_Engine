import logging
from pythonjsonlogger import jsonlogger
import sys

def setup_logger():
    logger = logging.getLogger("DecisionEngine")
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        logHandler = logging.StreamHandler(sys.stdout)
        formatter = jsonlogger.JsonFormatter('%(timestamp)s %(levelname)s %(name)s %(message)s', timestamp=True)
        logHandler.setFormatter(formatter)
        logger.addHandler(logHandler)
        
    return logger

logger = setup_logger()
