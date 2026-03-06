"""
Logging configuration with file rotation for FastAPI application.
"""

import logging
import logging.handlers
import os
from pathlib import Path
from datetime import datetime

# Create logs directory if it doesn't exist
LOGS_DIR = Path(__file__).parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Log file paths
MAIN_LOG_FILE = LOGS_DIR / "app.log"
ERROR_LOG_FILE = LOGS_DIR / "error.log"
ACCESS_LOG_FILE = LOGS_DIR / "access.log"

# Logging configuration
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging():
    """
    Configure application logging with file rotation.
    
    Features:
    - Main application log file with daily rotation
    - Separate error log file
    - Access log file for HTTP requests
    - Console output for debugging
    """
    
    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    
    # Clear existing handlers to avoid duplicates
    root_logger.handlers.clear()
    
    # Formatter
    formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
    
    # =====================================================================
    # 1. FILE HANDLER - Main Application Log (Rotating Daily)
    # =====================================================================
    file_handler = logging.handlers.RotatingFileHandler(
        filename=str(MAIN_LOG_FILE),
        maxBytes=10 * 1024 * 1024,  # 10 MB per file
        backupCount=7,  # Keep 7 backup files
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # =====================================================================
    # 2. TIMED ROTATING FILE HANDLER - Daily Rotation
    # =====================================================================
    timed_file_handler = logging.handlers.TimedRotatingFileHandler(
        filename=str(MAIN_LOG_FILE.with_stem(MAIN_LOG_FILE.stem + "_daily")),
        when="midnight",  # Rotate at midnight
        interval=1,  # Every 1 day
        backupCount=30,  # Keep 30 days of logs
        encoding='utf-8'
    )
    timed_file_handler.setLevel(logging.DEBUG)
    timed_file_handler.setFormatter(formatter)
    # Add suffix to rotated files
    timed_file_handler.suffix = "%Y-%m-%d.log"
    root_logger.addHandler(timed_file_handler)
    
    # =====================================================================
    # 3. ERROR FILE HANDLER - Errors Only
    # =====================================================================
    error_handler = logging.handlers.RotatingFileHandler(
        filename=str(ERROR_LOG_FILE),
        maxBytes=10 * 1024 * 1024,  # 10 MB per file
        backupCount=10,  # Keep 10 backup files
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    root_logger.addHandler(error_handler)
    
    # =====================================================================
    # 4. CONSOLE HANDLER - Console Output (INFO level and above)
    # =====================================================================
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        "%(levelname)s - %(name)s - %(message)s"
    )
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    return root_logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the given name.
    
    Args:
        name: Module name (typically __name__)
    
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


def log_startup_info():
    """Log application startup information."""
    logger = get_logger(__name__)
    logger.info("=" * 80)
    logger.info("APPLICATION STARTUP")
    logger.info("=" * 80)
    logger.info(f"Log directory: {LOGS_DIR}")
    logger.info(f"Main log: {MAIN_LOG_FILE}")
    logger.info(f"Error log: {ERROR_LOG_FILE}")
    logger.info(f"Access log: {ACCESS_LOG_FILE}")
    logger.info(f"Timestamp: {datetime.now().isoformat()}")
    logger.info("=" * 80)


def log_shutdown_info():
    """Log application shutdown information."""
    logger = get_logger(__name__)
    logger.info("=" * 80)
    logger.info("APPLICATION SHUTDOWN")
    logger.info(f"Timestamp: {datetime.now().isoformat()}")
    logger.info("=" * 80)
