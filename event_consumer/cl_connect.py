from event_consumer.utils.clickhouse import Session

cl_connect: Session | None = None


def set_cl_connect(session: Session | None):
    global cl_connect
    cl_connect = session


def get_cl_connect() -> Session:
    return cl_connect
