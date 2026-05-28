import logging
import os
from datetime import datetime


LOG_FILE = f"{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.log"
log_path = os.path.join(os.getcwd(), "logs")
os.makedirs(log_path, exist_ok=True)

logs_path = os.path.join(log_path, LOG_FILE)
logging.basicConfig(
    filename=logs_path,
    level=logging.INFO,
    format="[%(asctime)s] - %(lineno)d  %(name)s - %(levelname)s - %(message)s"
)

