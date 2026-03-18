# FastAPI Logging System

## Overview

This FastAPI application includes a comprehensive file-based logging system with automatic rotation mechanisms. Logs are organized, rotated daily, and managed to prevent excessive disk usage.

## Features

✅ **Multiple Log Files**
- `app.log` - Main application logs
- `app_daily_*.log` - Daily rotated logs
- `error.log` - Error-level logs only

✅ **Automatic Rotation**
- Size-based rotation (10 MB per file)
- Time-based rotation (daily at midnight)
- Maintains 7-30 days of historical logs

✅ **HTTP Request/Response Logging**
- All requests logged with method, path, query, client IP
- Response status codes and processing duration
- Request-specific timing information

✅ **Structured Output**
- Console output for development (INFO level)
- File output for production (DEBUG level)
- Consistent timestamp and formatting

## Log Locations

Logs are stored in: `fastapi_backend/logs/`

```
logs/
├── app.log                  # Main application log (rotating, max 10 MB)
├── app.log.1                # Rotated backup
├── app.log.2                # Rotated backup
├── app_daily_2026-03-05.log # Daily rotation
├── app_daily_2026-03-04.log # Previous day
├── error.log                # Errors only
└── error.log.1              # Rotated backup
```

## Configuration

### Rotation Settings

Located in `app/logging_config.py`:

```python
# File rotation
maxBytes=10 * 1024 * 1024  # 10 MB per file
backupCount=7              # Keep 7 backup files

# Time-based rotation
when="midnight"            # Rotate at midnight
interval=1                 # Every 1 day
backupCount=30             # Keep 30 days
```

### Log Levels

- **DEBUG** - Detailed diagnostic information (file output)
- **INFO** - General informational messages (console + file)
- **WARNING** - Warning messages
- **ERROR** - Error messages (separate error.log file)
- **CRITICAL** - Critical issues requiring immediate attention

## Usage

### Getting a Logger in Your Module

```python
import logging

logger = logging.getLogger(__name__)

# Use in your code
logger.debug("Debug message")
logger.info("Information message")
logger.warning("Warning message")
logger.error("Error message", exc_info=True)
logger.exception("Exception occurred")  # Automatically includes traceback
```

### In FastAPI Routes

```python
import logging
from fastapi import APIRouter

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/some-endpoint")
async def some_endpoint():
    logger.info("Endpoint called")
    try:
        # Your logic
        logger.debug("Processing step 1")
    except Exception as e:
        logger.exception(f"Error processing: {e}")
        raise
```

### HTTP Request Logging (Automatic)

The `LoggingMiddleware` automatically logs:

```
INFO - REQUEST | Method: POST | Path: /sales/export-sales-orders | Query: None | Client: ('127.0.0.1', 54321)
INFO - RESPONSE | Method: POST | Path: /sales/export-sales-orders | Status: 200 | Duration: 1.234s
```

## Startup/Shutdown Logging

Application startup and shutdown are automatically logged:

```
2026-03-05 10:30:15 - app.main - INFO - ================================================================================
2026-03-05 10:30:15 - app.main - INFO - APPLICATION STARTUP
2026-03-05 10:30:15 - app.main - INFO - ================================================================================
2026-03-05 10:30:15 - app.main - INFO - Log directory: .../fastapi_backend/logs
2026-03-05 10:30:15 - app.main - INFO - Main log: .../fastapi_backend/logs/app.log
```

## Monitoring Logs

### View Real-Time Logs (Windows PowerShell)

```powershell
Get-Content -Path "fastapi_backend/logs/app.log" -Tail 50 -Wait
```

### Search Logs for Errors

```powershell
Select-String -Path "fastapi_backend/logs/error.log" -Pattern "Exception"
```

### View Recent Activity

```powershell
Get-Item fastapi_backend/logs/ | Sort-Object LastWriteTime -Descending
```

### Check Log File Sizes

```powershell
Get-ChildItem fastapi_backend/logs/ | Select-Object Name, @{Name="Size(MB)"; Expression={[math]::Round($_.Length/1MB, 2)}}
```

## Best Practices

### 1. Use Appropriate Log Levels

```python
# DON'T: Use print() for logging
print("User login successful")  # ❌ No timestamp, no level

# DO: Use logger with appropriate level
logger.info("User login successful")  # ✅ Has timestamp, level
logger.debug("User ID: 123")           # ✅ Debug details
logger.error("Login failed", exc_info=True)  # ✅ With traceback
```

### 2. Include Context in Messages

```python
# DON'T: Vague messages
logger.info("Processing started")

# DO: Include identifying information
logger.info(f"Processing order {order_id} for customer {customer_id}")
logger.debug(f"Processing step: {step_name} | Status: {status}")
```

### 3. Use Exception Logging Properly

```python
# DON'T: Log without context
except Exception as e:
    logger.error(str(e))

# DO: Use exc_info=True for full traceback
except Exception as e:
    logger.exception(f"Failed to process order {order_id}")  # Automatically includes traceback
    # or
    logger.error(f"Failed to process order {order_id}", exc_info=True)
```

### 4. Avoid Logging Sensitive Data

```python
# DON'T: Log passwords or tokens
logger.info(f"User password: {password}")

# DO: Log safe identifying information
logger.info(f"User {user_id} authenticated")
logger.debug(f"Request headers (excluding auth): {safe_headers}")
```

## Troubleshooting

### Logs Not Being Created

1. Check that `logs/` directory exists or can be created
2. Verify file permissions in the fastapi_backend directory
3. Check that logging is initialized in `main.py`

### Log File Growing Too Large

- Current configuration limits files to 10 MB
- Files rotate automatically when limit is reached
- Historical logs are kept for 7-30 days depending on rotation type

### Missing Recent Entries

- Logs may be buffered; restart the application to flush
- Check permissions on log files
- Verify that the logging level isn't filtering out messages

## Integration with Monitoring Tools

To integrate with external monitoring (e.g., ELK, Datadog, etc.):

```python
# In logging_config.py, add custom handler:
import logging.handlers

syslog_handler = logging.handlers.SysLogHandler(
    address=('logserver.example.com', 514)
)
root_logger.addHandler(syslog_handler)
```

## Performance Considerations

- File I/O is asynchronous in the middleware
- Rotating handlers add minimal overhead
- Daily rotation helps manage disk usage
- Old logs are automatically cleaned up per backupCount settings

## See Also

- [Python Logging Documentation](https://docs.python.org/3/library/logging.html)
- [FastAPI Logging Documentation](https://fastapi.tiangolo.com/advanced/logging/)
