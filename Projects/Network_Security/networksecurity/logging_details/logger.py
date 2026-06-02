import logging, os, sys
from datetime import datetime

LOG_FILE=f"{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.log"

log_filepath = os.path.join(os.getcwd(),'logs', LOG_FILE)
os.makedirs(log_filepath, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_filepath, LOG_FILE),
    format="[%(asctime)s]  %(lineno)d  %(name)s  %(levelname)s : %(message)s",
    level = logging.INFO
)


logging.info("working fine")