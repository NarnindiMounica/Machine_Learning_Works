import os, sys
from networksecurity.exception_details.exception import CustomException
from networksecurity.logging_details.logger import logging

if __name__=="__main__":
    logging.info("testing custom exception")
    try:
        a = 1/0
        print("a will not be printed")
    except Exception as e:
        raise CustomException(e, sys)        