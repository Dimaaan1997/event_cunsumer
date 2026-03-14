from json import dumps

import structlog


def non_ascii_dumps(obj, **kwargs):
    return dumps(obj, ensure_ascii=False, **kwargs)


structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.format_exc_info,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(serializer=non_ascii_dumps),
    ],
    cache_logger_on_first_use=True,
)
log = structlog.get_logger()
