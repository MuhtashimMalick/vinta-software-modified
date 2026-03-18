"""
Middleware for logging HTTP requests and responses.
"""

import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log incoming requests and outgoing responses.
    Logs include request method, path, status code, and response time.
    """
    
    async def dispatch(self, request: Request, call_next):
        """
        Process request and log details.
        """
        # Start timer
        start_time = time.time()
        
        # Log request
        logger.info(
            f"REQUEST | Method: {request.method} | Path: {request.url.path} | "
            f"Query: {request.url.query or 'None'} | Client: {request.client}"
        )
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate response time
            response_time = time.time() - start_time
            
            # Log response
            logger.info(
                f"RESPONSE | Method: {request.method} | Path: {request.url.path} | "
                f"Status: {response.status_code} | Duration: {response_time:.3f}s"
            )
            
            # Add custom headers (optional)
            response.headers["X-Process-Time"] = str(response_time)
            
            return response
            
        except Exception as e:
            # Log errors
            response_time = time.time() - start_time
            logger.error(
                f"ERROR | Method: {request.method} | Path: {request.url.path} | "
                f"Duration: {response_time:.3f}s | Error: {str(e)}",
                exc_info=True
            )
            raise
