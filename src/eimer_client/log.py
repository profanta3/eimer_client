import structlog
from rich_structlog import setup_logging

setup_logging(
    log_level="INFO",
    pkg2loglevel={
        # "streamlit": "INFO",
        # "sqlalchemy": "WARN",
        # "urllib3": "WARN",
    },
)

log: structlog.stdlib.BoundLogger = structlog.get_logger()
