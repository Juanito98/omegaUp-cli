import logging


def init_logger() -> None:
    logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO)
    logging.getLogger("urllib3").setLevel(logging.CRITICAL)
