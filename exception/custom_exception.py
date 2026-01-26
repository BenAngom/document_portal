import sys
import traceback

from logger.custom_logger import CustomLogger
logger=CustomLogger().get_logger("__file__")

class DocumentPortalException(Exception):
    """Custom exception for document portal"""
    def __init__(self, error_message:str, error_details:sys):
        _,_,exc_tb=error_details.exc_info()
        self.file_name = exc_tb.tb_frame.f_code.co_filename
        self.line_number = exc_tb.tb_lineno
        self.error_message = str(error_message)
        self.traceback_str = ''.join(traceback.format_exception(*error_details.exc_info())) 
    def __str__(self):
        return f"""
        Error occurred in file: {self.file_name} at line: {self.line_number}
        Error Message: {self.error_message}
        Traceback Details: {self.traceback_str}"""
    
if __name__ == "__main__":
    try:
        # simulate an error
        a = 1 / 0
        print(a)
    except Exception as e:
        app_exp = DocumentPortalException(e,sys)
        logger.error(app_exp)
        raise app_exp