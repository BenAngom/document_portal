import os
import sys
from utils.model_loader import ModelLoader
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from model.models import Metadata
from prompt.prompt_library import prompt

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate


class DocumentAnalyzer:
    """
    Analyzes documents using a pre-trained model.
    Automatically logs all actions and supports session-based organization.
    """

    def __init__(self):
        try:
            self.log = CustomLogger().get_logger(__name__)
            self.loader = ModelLoader()
            self.llm = self.loader.load_llm()

            # Parser (LangChain 1.x–correct)
            self.parser = PydanticOutputParser(
                pydantic_object=Metadata
            )

            self.prompt = prompt

            self.log.info("DocumentAnalyzer initialized successfully")

        except Exception as e:
            self.log.error("Error initializing DocumentAnalyzer", error=str(e))
            raise DocumentPortalException(
                "Error in DocumentAnalyzer initialization", sys
            )

    def analyze_document(self, document_text: str) -> dict:
        """
        Analyze a document's text and extract structured metadata & summary.
        """
        try:
            chain = (
                self.prompt
                | self.llm
                | self.parser
            ).with_retry(stop_after_attempt=2)

            self.log.info("Meta-data analysis chain initialized")

            response = chain.invoke({
                "format_instructions": self.parser.get_format_instructions(),
                "document_text": document_text
            })

            # ✅ Convert ONCE from Pydantic → dict
            metadata = response.model_dump()

            self.log.info(
                "Metadata extraction successful",
                extra={"fields": list(metadata.keys())}
            )

            return metadata

        except Exception as e:
            self.log.error("Metadata analysis failed", error=str(e))
            raise DocumentPortalException(
                "Metadata extraction failed", sys
            )
