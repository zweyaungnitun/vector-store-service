import pandas as pd
from pypdf import PdfReader
from io import BytesIO
from typing import List, Dict, Any, Union
import logging

class FileProcessor:
    """
    Utility class to extract content from different file formats.
    """

    @staticmethod
    def extract_text_from_pdf(content: bytes) -> str:
        try:
            reader = PdfReader(BytesIO(content))
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            return text.strip()
        except Exception as e:
            logging.error(f"Error processing PDF: {str(e)}")
            raise ValueError(f"Failed to extract text from PDF: {str(e)}")

    @staticmethod
    def extract_data_from_csv(content: bytes) -> List[Dict[str, Any]]:
        try:
            df = pd.read_csv(BytesIO(content))
            # Replace NaN with None for JSON compatibility
            return df.where(pd.notnull(df), None).to_dict(orient="records")
        except Exception as e:
            logging.error(f"Error processing CSV: {str(e)}")
            raise ValueError(f"Failed to extract data from CSV: {str(e)}")

    @staticmethod
    def extract_data_from_excel(content: bytes) -> List[Dict[str, Any]]:
        try:
            df = pd.read_excel(BytesIO(content))
            # Replace NaN with None for JSON compatibility
            return df.where(pd.notnull(df), None).to_dict(orient="records")
        except Exception as e:
            logging.error(f"Error processing Excel: {str(e)}")
            raise ValueError(f"Failed to extract data from Excel: {str(e)}")

    @staticmethod
    def extract_text_from_txt(content: bytes) -> str:
        try:
            return content.decode("utf-8").strip()
        except UnicodeDecodeError:
            try:
                # Fallback for common encodings
                return content.decode("latin-1").strip()
            except Exception as e:
                raise ValueError(f"Failed to decode text file: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error processing text file: {str(e)}")

    @classmethod
    def process_file(cls, filename: str, content: bytes) -> Union[str, List[Dict[str, Any]]]:
        """
        Main entry point to process a file based on its extension.
        """
        ext = filename.split('.')[-1].lower()
        
        if ext == 'pdf':
            return cls.extract_text_from_pdf(content)
        elif ext == 'csv':
            return cls.extract_data_from_csv(content)
        elif ext in ['xlsx', 'xls']:
            return cls.extract_data_from_excel(content)
        elif ext == 'txt':
            return cls.extract_text_from_txt(content)
        else:
            raise ValueError(f"Unsupported file format: {ext}")
