
import logging

logger = logging.getLogger('test_logger')

def log_pass(message):
    logger.info(f"\033[92m✔ [PASS]\033[0m {message}")

def log_fail(message):
    logger.error(f"\033[91m✖ [FAIL]\033[0m {message}")

def log_warning(message):
    logger.warning(f"\033[93m⚠ [WARN]\033[0m {message}")