import logging


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s.%(msecs)03d %(module)s %(levelname)s %(message)s",
)
log = logging.getLogger("UAVlogger")
