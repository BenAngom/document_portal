import os
from utils.model_load import module_for_loader
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from model.models import *
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser

class DocumentAnalyzer:
    """
    Analyzes documents using a pre-trained language model.
    Automatically logs all actions and supports session-based organization.
    """
    
    def __init__(self):
        pass
    
    def analyze_metadata(self): 
                