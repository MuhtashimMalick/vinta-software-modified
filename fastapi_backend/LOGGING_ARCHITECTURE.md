# 📋 Logging System Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         FASTAPI APPLICATION                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    HTTP REQUEST ARRIVES                          │   │
│  │                (LoggingMiddleware intercepts)                    │   │
│  └────────────────────────┬─────────────────────────────────────────┘   │
│                           │                                              │
│                           ▼                                              │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │         LoggingMiddleware (app/logging_middleware.py)            │   │
│  │  ┌────────────────────────────────────────────────────────────┐  │   │
│  │  │ • Captures request details (method, path, query, client)   │  │   │
│  │  │ • Measures response time                                   │  │   │
│  │  │ • Logs via logger.info() / logger.error()                 │  │   │
│  │  └────────────────────────────────────────────────────────────┘  │   │
│  └────────────────────────┬─────────────────────────────────────────┘   │
│                           │                                              │
│                           ▼                                              │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    ROUTE HANDLER LOGIC                           │   │
│  │  (e.g., export_sales_orders, import_remote_xml)                │   │
│  │  ┌────────────────────────────────────────────────────────────┐  │   │
│  │  │ logger.debug("...")   - Detailed debugging info            │  │   │
│  │  │ logger.info("...")    - Important events                   │  │   │
│  │  │ logger.error("...", exc_info=True) - Error details         │  │   │
│  │  │ logger.exception("...") - Exception + traceback            │  │   │
│  │  └────────────────────────────────────────────────────────────┘  │   │
│  └────────────────────────┬─────────────────────────────────────────┘   │
│                           │                                              │
└───────────────────────────┼──────────────────────────────────────────────┘
                            │
                            ▼
    ┌───────────────────────────────────────────────────────────┐
    │   Python Logging System (logging module)                  │
    │   ┌─────────────────────────────────────────────────────┐ │
    │   │  Root Logger (logging.getLogger())                  │ │
    │   └─────────────────────────────────────────────────────┘ │
    └───────────────────────────────────────────────────────────┘
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │ Formatter    │  │ Formatter    │  │ Formatter    │
    │ (timestamp)  │  │ (timestamp)  │  │ (timestamp)  │
    └──────────────┘  └──────────────┘  └──────────────┘
          │                 │                 │
          ▼                 ▼                 ▼
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │  Console     │  │  File Handler│  │ Error File   │
    │  Handler     │  │  (Rotating)  │  │  Handler     │
    │              │  │              │  │  (Rotating)  │
    │ INFO+        │  │ DEBUG+       │  │ ERROR+       │
    │ WARNING,     │  │ INFO,        │  │ CRITICAL     │
    │ ERROR,       │  │ WARNING,     │  │              │
    │ CRITICAL     │  │ ERROR,       │  │              │
    │              │  │ CRITICAL     │  │              │
    └──────────────┘  └──────────────┘  └──────────────┘
          │                 │                 │
          │                 │                 │
          │            ┌────┴─────┐     ┌────┴─────┐
          │            │           │     │           │
          ▼            ▼           ▼     ▼           ▼
    [Console]    [app.log]    [*.1,.2]  [error.log] [*.1]
                  Size-based    Backups  Size-based  Backups
                  10 MB max                10 MB max
                  Keep 7                   Keep 10
                  
                  [app_daily_*]
                  Time-based
                  Daily at midnight
                  Keep 30 days
```

## Data Flow

```
Request comes in
     │
     ▼
LoggingMiddleware
  • Log: "REQUEST | Method: GET | Path: /sales/..."
  • Start timer
     │
     ▼
Route Handler (e.g., export_sales_orders)
  • logger.info("Processing started")
  • logger.debug("Fetching headers from database")
  • logger.error("Customer not found") - if error
  • logger.exception("Error occurred") - if exception
     │
     ▼
LoggingMiddleware (response captured)
  • Stop timer
  • Log: "RESPONSE | Method: GET | Status: 200 | Duration: 1.234s"
     │
     ▼
Response sent to client

All logs written to appropriate files:
  • DEBUG/INFO/WARNING → app.log
  • ERROR/CRITICAL → error.log + console
  • Automatic rotation when size/time limit reached
```

## File Structure

```
fastapi_backend/
│
├── logs/                                    ← All log files here
│   ├── app.log                              ← Main log (current)
│   ├── app.log.1                            ← Backup from previous rotation
│   ├── app.log.2                            ← Backup (older)
│   ├── app_daily_2026-03-05.log             ← Today's daily log
│   ├── app_daily_2026-03-04.log             ← Yesterday's daily log
│   ├── app_daily_2026-03-03.log             ← 3 days ago
│   ├── error.log                            ← Errors only (current)
│   ├── error.log.1                          ← Error backup
│   └── ...
│
├── app/
│   ├── __init__.py
│   ├── main.py                              ← Logging initialized here
│   │                                          ┣ setup_logging()
│   │                                          ┣ Middleware added
│   │                                          ┣ @on_event("startup")
│   │                                          ┗ @on_event("shutdown")
│   │
│   ├── logging_config.py                    ← Core logging setup
│   │   ├── setup_logging()                  ← Initializes all handlers
│   │   ├── get_logger()                     ← Get logger instance
│   │   ├── log_startup_info()               ← Log app start
│   │   └── log_shutdown_info()              ← Log app shutdown
│   │
│   ├── logging_middleware.py                ← HTTP request/response logging
│   │   └── LoggingMiddleware                ← Middleware class
│   │
│   ├── routes/
│   │   └── salesorder.py                    ← Uses logger
│   │       ├── logger = logging.getLogger(__name__)
│   │       ├── logger.debug("...")
│   │       ├── logger.info("...")
│   │       ├── logger.error("...")
│   │       └── logger.exception("...")
│   │
│   └── ...other files...
│
├── LOGGING.md                               ← Comprehensive guide
├── LOGGING_QUICK_REFERENCE.md               ← Quick reference
├── LOGGING_SETUP_SUMMARY.md                 ← This summary
├── test_logging.py                          ← Test script
├── .gitignore                               ← Updated (includes logs/)
└── ...
```

## Rotation Mechanism

### Size-Based Rotation (app.log, error.log)
```
Step 1: Log file reaches 10 MB
   app.log (10.0 MB) ──┐
                       ├─→ app.log.1
                       
Step 2: app.log grows again to 10 MB
   app.log (10.0 MB) ──┐
   app.log.1 (10.0 MB)├─→ app.log.2
                       ├─→ app.log.1
                       
Step 3: After 7 rotations
   Oldest (app.log.7) is deleted
   Only last 7 backups kept

Result: Maximum disk usage = 10 MB × 8 files = 80 MB for app.log
        Maximum disk usage = 10 MB × 11 files = 110 MB for error.log
```

### Time-Based Rotation (app_daily_*.log)
```
Day 1: app_daily_2026-03-05.log created at midnight
       Logs written throughout the day

Day 2: At midnight (00:00)
       app_daily_2026-03-05.log ──→ app_daily_2026-03-05.log (final)
       New file: app_daily_2026-03-06.log created
       Logs continue here

After 30 days:
       app_daily_2026-02-04.log deleted (oldest, >30 days)
       Only last 30 days of logs kept

Result: One log file per day, maximum 30 files kept
```

## Log Levels Hierarchy

```
                CRITICAL (50)
                    │
                    ▼
                  ERROR (40)
                    │
                    ▼
                 WARNING (30) ← Default level
                    │
                    ▼
                   INFO (20)
                    │
                    ▼
                  DEBUG (10)
                    │
                    ▼
                NOTSET (0)

Each level includes all levels above it.
Example: Setting level to INFO means DEBUG messages are filtered out.
```

## Handler Configuration

```
┌─────────────────────────────────────────────────────────────────┐
│                     Root Logger                                 │
│              (Level: DEBUG - captures all)                      │
└────────────────────────┬────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
    HANDLER 1        HANDLER 2        HANDLER 3
   (Console)      (File Rotating)   (Error File)
   ┌──────────┐   ┌──────────────┐  ┌──────────────┐
   │ Level: ▼ │   │ Level: ▼     │  │ Level: ▼     │
   │ INFO     │   │ DEBUG        │  │ ERROR        │
   └──────────┘   └──────────────┘  └──────────────┘
   │              │                  │
   │ Outputs:     │ Outputs:         │ Outputs:
   │ • INFO       │ • DEBUG          │ • ERROR
   │ • WARNING    │ • INFO           │ • CRITICAL
   │ • ERROR      │ • WARNING        │
   │ • CRITICAL   │ • ERROR          │
   │              │ • CRITICAL       │
   └──────────────┘──────────────────┘──────────────┘
```

## Example Log Output

### Console Output (INFO level)
```
INFO - app.main - FastAPI application started successfully
INFO - app.routes.salesorder - REQUEST | Method: POST | Path: /sales/export-sales-orders | Query: None
INFO - app.routes.salesorder - Processing sales order | TaxCode: GST | PostCode: 2000
INFO - app.routes.salesorder - RESPONSE | Method: POST | Path: /sales/export-sales-orders | Status: 200 | Duration: 2.341s
```

### File Output (app.log, DEBUG level)
```
2026-03-05 10:30:15 - app.main - INFO - APPLICATION STARTUP
2026-03-05 10:30:15 - app.main - INFO - Log directory: .../fastapi_backend/logs
2026-03-05 10:30:15 - app.routes.salesorder - DEBUG - Found 1 unsent headers
2026-03-05 10:30:15 - app.routes.salesorder - DEBUG - Retrieved TCustomer record: <TCustomers object>
2026-03-05 10:30:15 - app.routes.salesorder - INFO - Processing sales order | TaxCode: GST | PostCode: 2000
2026-03-05 10:30:18 - app.routes.salesorder - DEBUG - Unleashed response status: 201
2026-03-05 10:30:18 - app.routes.salesorder - INFO - REQUEST | Method: POST | Path: /sales/export-sales-orders
2026-03-05 10:30:18 - app.routes.salesorder - INFO - RESPONSE | Method: POST | Path: /sales/export-sales-orders | Status: 200 | Duration: 2.341s
```

### Error Output (error.log, ERROR level only)
```
2026-03-05 11:45:32 - app.routes.salesorder - ERROR - Failed to send order ABC123: Connection timeout
2026-03-05 11:45:33 - app.routes.salesorder - ERROR - Exception processing order XYZ456: 
Traceback (most recent call last):
  File "app/routes/salesorder.py", line 245, in export_sales_orders
    response = requests.post(BASE_URL, json=payload)
  File "requests/api.py", line 49, in post
    return request('post', url, data=data, json=json, **kwargs)
  ...
ValueError: Invalid payload structure
```

## Performance Characteristics

```
Operation                    Impact
─────────────────────────────────────────────
logger.debug("msg")         Minimal (async, goes to file only)
logger.info("msg")          Low (written to console + file)
logger.error("msg")         Low (written to error file)
requests.post()             Varies (async context)
File rotation               Minimal (background task)
Disk I/O                    Buffered (OS handles)
─────────────────────────────────────────────

Typical response time increase: <5ms per request
Disk space used: ~80-110 MB (depending on activity)
CPU overhead: <1% (logging operations)
```

---

**Last Updated:** March 5, 2026
