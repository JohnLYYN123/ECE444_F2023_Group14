import logging
from logging.handlers import RotatingFileHandler
import os
app_root = os.path.dirname(__file__)
project_root = os.path.dirname(app_root)

def setup_logger(logger_name, log_file=os.path.join(project_root, 'logs', 'operation.log'), level=logging.INFO):
    log = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    
    fileHandler = RotatingFileHandler(log_file, maxBytes=100 * 1024 * 1024,
                                       backupCount=100, encoding='utf-8')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    log.setLevel(level)
    log.addHandler(fileHandler)
    log.addHandler(streamHandler)
    return log
