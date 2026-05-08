import logging

def setup_logger():
    # Simple, readable logging format
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    return logging.getLogger("app")

# Global logger instance
logger = setup_logger()
