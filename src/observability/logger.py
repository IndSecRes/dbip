"""
Structured Logging
Provides structured logging with levels and context
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum
from dataclasses import dataclass, field


class LogLevel(str, Enum):
    """Log levels"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class LogEntry:
    """Structured log entry"""
    level: LogLevel
    message: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    component: Optional[str] = None
    request_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    stack_trace: Optional[str] = None


class Logger:
    """
    Structured logger with context
    """
    
    def __init__(self, name: str, level: LogLevel = LogLevel.INFO):
        self.name = name
        self.level = level
        self.logs: list[LogEntry] = []
        self._logger = logging.getLogger(name)
        self._logger.setLevel(level.value)
        
        # Configure handler if not already configured
        if not self._logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)
    
    def debug(self, message: str, **metadata) -> None:
        """Log DEBUG level"""
        self._log(LogLevel.DEBUG, message, metadata)
    
    def info(self, message: str, **metadata) -> None:
        """Log INFO level"""
        self._log(LogLevel.INFO, message, metadata)
    
    def warning(self, message: str, **metadata) -> None:
        """Log WARNING level"""
        self._log(LogLevel.WARNING, message, metadata)
    
    def error(self, message: str, exception: Optional[Exception] = None, **metadata) -> None:
        """Log ERROR level"""
        stack_trace = None
        if exception:
            import traceback
            stack_trace = traceback.format_exc()
            metadata["exception_type"] = type(exception).__name__
            metadata["exception_message"] = str(exception)
        
        self._log(LogLevel.ERROR, message, metadata, stack_trace)
    
    def critical(self, message: str, exception: Optional[Exception] = None, **metadata) -> None:
        """Log CRITICAL level"""
        stack_trace = None
        if exception:
            import traceback
            stack_trace = traceback.format_exc()
            metadata["exception_type"] = type(exception).__name__
            metadata["exception_message"] = str(exception)
        
        self._log(LogLevel.CRITICAL, message, metadata, stack_trace)
    
    def _log(self, level: LogLevel, message: str, metadata: Dict[str, Any], stack_trace: Optional[str] = None) -> None:
        """Internal log method"""
        if level.value < self.level.value:
            return
        
        entry = LogEntry(
            level=level,
            message=message,
            component=self.name,
            metadata=metadata,
            stack_trace=stack_trace
        )
        
        # Store in memory
        self.logs.append(entry)
        
        # Log to Python logger
        log_method = getattr(self._logger, level.value.lower(), self._logger.info)
        log_text = f"{message} | {json.dumps(metadata) if metadata else ''}"
        if stack_trace:
            log_text += f"\n{stack_trace}"
        log_method(log_text)
    
    def get_logs(self, level: Optional[LogLevel] = None, limit: int = 100) -> list[LogEntry]:
        """Get stored logs"""
        logs = self.logs
        if level:
            logs = [l for l in logs if l.level == level]
        return logs[-limit:]
    
    def clear(self) -> None:
        """Clear stored logs"""
        self.logs.clear()


# Global logger instances
_global_logger: Optional[Logger] = None


def get_logger(name: str = "DBIP", level: LogLevel = LogLevel.INFO) -> Logger:
    """Get or create a logger"""
    global _global_logger
    if _global_logger is None:
        _global_logger = Logger(name, level)
    return _global_logger