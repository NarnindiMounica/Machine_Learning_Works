import os, sys

from networksecurity.logging_details.logger import logging

def get_error_details(error_msg, error_details:sys)->str:
    _, _, exc_tb = error_details.exc_info()
    lineno = exc_tb.tb_lineno
    filename = exc_tb.tb_frame.f_code.co_filename

    return f"Error occurred in {filename} at line number {lineno} : {error_msg}"

class CustomException(Exception):
    def __init__(self, error_msg, error_details):
        self.error_msg = get_error_details(error_msg=error_msg, error_details=sys)

    def __str__(self):
        return self.error_msg
    

