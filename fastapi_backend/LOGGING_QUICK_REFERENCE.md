# Logging Quick Reference

## Quick Start

```python
import logging

logger = logging.getLogger(__name__)

# In your code:
logger.debug("Detailed info for developers")
logger.info("General informational messages")
logger.warning("Warning about potential issues")
logger.error("An error occurred")
logger.exception("Exception with full traceback")
```

## Log Levels Explained

| Level | Use When | Output |
|-------|----------|--------|
| DEBUG | You need detailed diagnostic info | File only |
| INFO | Recording significant events | Console + File |
| WARNING | Something unexpected (default) | Console + File |
| ERROR | A serious problem | Error file + Console |
| CRITICAL | System might fail | Error file + Console |

## Common Logging Patterns

### API Endpoint Logging
```python
@router.post("/endpoint")
async def my_endpoint(data: SomeModel):
    logger.info(f"Received request for {data.id}")
    try:
        result = process(data)
        logger.debug(f"Processing succeeded for {data.id}")
        return result
    except Exception as e:
        logger.exception(f"Failed to process {data.id}")
        raise
```

### Database Operations
```python
async def fetch_customer(customer_id):
    logger.debug(f"Fetching customer {customer_id}")
    customer = await db.get(Customer, customer_id)
    if not customer:
        logger.warning(f"Customer {customer_id} not found")
    else:
        logger.debug(f"Customer {customer_id} loaded")
    return customer
```

### External API Calls
```python
response = requests.post(API_URL, json=payload, timeout=30)
logger.debug(f"API response status: {response.status_code}")

if response.status_code == 201:
    logger.info(f"Order {order_id} successfully sent to external system")
else:
    logger.error(f"Failed to send order {order_id}: {response.text}")
```

### Data Processing with Metrics
```python
total_processed = 0
total_failed = 0

for item in items:
    try:
        process(item)
        total_processed += 1
    except Exception as e:
        logger.error(f"Failed to process {item.id}: {e}")
        total_failed += 1

logger.info(f"Processing complete: {total_processed} succeeded, {total_failed} failed")
```

## File Locations

```
fastapi_backend/
├── logs/
│   ├── app.log              # Main log (rotating)
│   ├── app_daily_*.log      # Daily rotation
│   └── error.log            # Errors only (rotating)
├── app/
│   ├── logging_config.py    # Logging setup
│   ├── logging_middleware.py # HTTP logging
│   └── main.py              # Initialization
```

## Check Log Files

### PowerShell Commands

```powershell
# View last 50 lines
Get-Content -Path "fastapi_backend/logs/app.log" -Tail 50

# Real-time follow (like 'tail -f')
Get-Content -Path "fastapi_backend/logs/app.log" -Tail 50 -Wait

# Search for errors
Select-String -Path "fastapi_backend/logs/error.log" -Pattern "ERROR"

# Count log entries
(Get-Content "fastapi_backend/logs/app.log" | Measure-Object -Line).Lines

# List recent log files
Get-ChildItem "fastapi_backend/logs/" | Sort-Object LastWriteTime -Descending | Select-Object Name, LastWriteTime
```

## Configuration

### To Change Log Level
Edit `app/logging_config.py`:
```python
root_logger.setLevel(logging.DEBUG)  # Change this
console_handler.setLevel(logging.INFO)  # or this
```

### To Change Rotation Settings
Edit `app/logging_config.py`:
```python
maxBytes=10 * 1024 * 1024  # Max file size
backupCount=7              # Number of backups to keep
```

### To Add Custom Handler
Add to `setup_logging()` in `app/logging_config.py`:
```python
custom_handler = logging.FileHandler('custom.log')
custom_handler.setLevel(logging.WARNING)
custom_handler.setFormatter(formatter)
root_logger.addHandler(custom_handler)
```

## Performance Tips

- ✅ Use `logger.debug()` freely—only writes to files
- ✅ Use `logger.info()` for important events
- ✅ Avoid logging in tight loops (use debug)
- ✅ Use `exc_info=True` for exceptions
- ❌ Don't use `print()` for logging
- ❌ Don't log sensitive data (passwords, tokens)

## Useful Links

- [Python Logging Docs](https://docs.python.org/3/library/logging.html)
- [Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html)
- [FastAPI Logging](https://fastapi.tiangolo.com/advanced/logging/)

---

**Last Updated:** March 5, 2026
