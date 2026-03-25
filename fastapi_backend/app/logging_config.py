"""
Logging configuration with file rotation for FastAPI application.
"""

import logging
import logging.handlers
import json
import uuid


from datetime import datetime, timezone
from pathlib import Path

# Create logs directory if it doesn't exist
LOGS_DIR = Path(__file__).parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)
JSONL_LOGS_DIR = Path(__file__).parent.parent / "logs" / "jsonl"
JSONL_LOGS_DIR.mkdir(exist_ok=True)

TIMEZONE = timezone.utc

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


class JsonlRotatingHandler(logging.handlers.TimedRotatingFileHandler):
    """
    Writes a new JSONL log file each day.
    Files are named DD-MM-YYYY.log and stored in JSONL_LOGS_DIR.
    """

    def __init__(self):
        # Compute today's file path on init
        filename = self._get_filepath()
        super().__init__(
            filename=filename,
            when="midnight",
            interval=1,
            backupCount=0,      # we manage filenames ourselves
            encoding="utf-8",
            delay=False,
        )
        self.suffix = "%d-%m-%Y.log"  # not really used but kept for clarity

    def _get_filepath(self) -> str:
        today = datetime.now(tz=TIMEZONE).strftime("%d-%m-%Y")
        return str(JSONL_LOGS_DIR / f"{today}.log")

    def rotation_filename(self, default_name: str) -> str:
        """Override so rotated file gets today's date name, not yesterday's."""
        return self._get_filepath()

    def emit(self, record: logging.LogRecord):
        """Write the record's msg (already a JSON string) as a JSONL line."""
        try:
            with open(self.baseFilename, "a", encoding="utf-8") as f:
                f.write(record.getMessage() + "\n")
        except Exception:
            self.handleError(record)

    def doRollover(self):
        """On midnight rollover, just update baseFilename to the new date."""
        self.baseFilename = self._get_filepath()
        self.rolloverAt = self.computeRollover(self.rolloverAt)


def get_jsonl_logger() -> logging.Logger:
    """
    Returns a dedicated logger that writes structured JSONL entries
    to a daily rotating file (DD-MM-YYYY.log) in the jsonl logs directory.

    Usage:
        from logging_config import get_jsonl_logger, build_jsonl_entry

        jsonl_logger = get_jsonl_logger()
        jsonl_logger.info(build_jsonl_entry(
            action_type="Export Unleashed",
            action_variant="export-unleashed",
            status="Success",
            message="Exported 212 purchase orders to Unleashed ERP.",
        ))
    """
    logger_name = "jsonl"
    logger = logging.getLogger(logger_name)

    # Avoid adding duplicate handlers if called multiple times
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)
    logger.propagate = False  # don't bubble up to root logger

    handler = JsonlRotatingHandler()
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    return logger


def build_jsonl_entry(
    action_type: str,
    action_variant: str,
    status: str,
    message: str,
) -> str:
    """
    Builds a JSON string representing one log entry.

    Args:
        action_type:    Human-readable action label e.g. "Export Unleashed"
        action_variant: Machine-readable slug e.g. "export-unleashed"
        status:         "Success", "Failed", "Pending", etc.
        message:        Descriptive message for this log entry

    Returns:
        A JSON string ready to be passed to the jsonl logger.
    """
    entry = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now(tz=TIMEZONE).isoformat(),
        "actionType": action_type,
        "actionVariant": action_variant,
        "status": status,
        "message": message,
    }
    return json.dumps(entry)
