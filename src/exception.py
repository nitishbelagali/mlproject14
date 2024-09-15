import sys
import logging
import os
from datetime import datetime

# Setting up the log file path with a dynamic filename
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)
os.makedirs(logs_path, exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

# Configuring logging
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Logging a start message
logging.info("Logging has started")


def error_message_detail(error, error_detail: sys):
    """
    This function captures and returns a detailed error message.
    """
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occurred in python script name[{0}] line number[{1}] error message[{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )
    return error_message


class CustomException(Exception):
    """
    Custom Exception class that logs detailed error messages.
    """
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail=error_detail)
        logging.error(self.error_message)  # Log the error message when the exception is instantiated

    def __str__(self):
        return self.error_message


if __name__ == "__main__":

    try:
        # Intentionally cause an exception
        a = 1 / 0
    except Exception as e:
        logging.info("Divide by zero error caught")
        raise CustomException(e, sys)  # Raise the custom exception
