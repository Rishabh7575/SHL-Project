import logging

def setup_logger():
    """
    Sets up a simple, readable logger for debugging.
    This avoids print() statements and gives us timestamps and severity levels.
    """
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    return logging.getLogger("backend")

# Global logger instance
logger = setup_logger()
