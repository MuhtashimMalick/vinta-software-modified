"""
Test script to verify logging setup is working correctly.
Run this to ensure logging is properly configured.

Usage:
    python -m fastapi_backend.test_logging
    
    or from fastapi_backend directory:
    python -m app.test_logging
"""

import logging
import sys
import os
from pathlib import Path

# Add parent directory to path to import app
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.logging_config import setup_logging, get_logger, log_startup_info, log_shutdown_info, LOGS_DIR


def test_logging():
    """Test logging functionality."""
    
    print("\n" + "="*80)
    print("FASTAPI LOGGING TEST")
    print("="*80 + "\n")
    
    # Initialize logging
    print("1. Initializing logging...")
    setup_logging()
    print(f"   ✓ Logging initialized")
    
    # Get logger
    print("\n2. Getting logger...")
    logger = get_logger(__name__)
    print(f"   ✓ Logger instance created: {logger.name}")
    
    # Test log directory
    print(f"\n3. Checking log directory...")
    print(f"   Log directory: {LOGS_DIR}")
    if LOGS_DIR.exists():
        print(f"   ✓ Directory exists")
    else:
        print(f"   ✗ Directory does not exist!")
        return False
    
    # Log startup info
    print(f"\n4. Logging startup information...")
    log_startup_info()
    print(f"   ✓ Startup info logged")
    
    # Test different log levels
    print(f"\n5. Testing log levels...")
    
    logger.debug("This is a DEBUG message (file only)")
    print(f"   ✓ DEBUG logged")
    
    logger.info("This is an INFO message (console + file)")
    print(f"   ✓ INFO logged")
    
    logger.warning("This is a WARNING message")
    print(f"   ✓ WARNING logged")
    
    logger.error("This is an ERROR message (error.log)")
    print(f"   ✓ ERROR logged")
    
    # Test exception logging
    print(f"\n6. Testing exception logging...")
    try:
        raise ValueError("Test exception for logging")
    except Exception:
        logger.exception("Caught a test exception")
    print(f"   ✓ Exception logged with traceback")
    
    # Check log files created
    print(f"\n7. Checking log files...")
    if os.path.exists(os.path.join(LOGS_DIR, "app.log")):
        print(f"   ✓ app.log exists")
    else:
        print(f"   ✗ app.log not found!")
        
    if os.path.exists(os.path.join(LOGS_DIR, "error.log")):
        print(f"   ✓ error.log exists")
    else:
        print(f"   ✗ error.log not found!")
    
    # List log files
    print(f"\n8. Log files created:")
    log_files = list(LOGS_DIR.glob("*"))
    if log_files:
        for log_file in sorted(log_files):
            size_kb = log_file.stat().st_size / 1024
            print(f"   - {log_file.name:<40} ({size_kb:.2f} KB)")
    else:
        print(f"   No log files found!")
        return False
    
    # Read and display sample from app.log
    print(f"\n9. Sample from app.log (last 10 lines):")
    print(f"   " + "-"*76)
    with open(os.path.join(LOGS_DIR, "app.log"), "r") as f:
        lines = f.readlines()
        for line in lines[-10:]:
            print(f"   {line.rstrip()}")
    print(f"   " + "-"*76)
    
    # Log shutdown
    print(f"\n10. Logging shutdown information...")
    log_shutdown_info()
    print(f"    ✓ Shutdown info logged")
    
    print("\n" + "="*80)
    print("✓ ALL TESTS PASSED!")
    print("="*80)
    print(f"\nLog files location: {LOGS_DIR}")
    print(f"\nTo view logs:")
    print(f"  Get-Content -Path '{LOGS_DIR}/app.log' -Tail 50")
    print(f"\nTo follow logs in real-time:")
    print(f"  Get-Content -Path '{LOGS_DIR}/app.log' -Tail 50 -Wait")
    print()
    
    return True


if __name__ == "__main__":
    success = test_logging()
    sys.exit(0 if success else 1)
