import os
from typing import List, Dict, Any
from uuid import uuid4
import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from config import settings
import logging

logger = logging.getLogger(__name__)


class PDFProcessor:
    def __init__(self):
        # TODO: Initialize text splitter with chunk size and overlap settings
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=settings.chunk_size, chunk_overlap=settings.chunk_overlap)
    
    def extract_text_from_pdf(self, file_path: str, filename: str) -> List[Dict[str, Any]]:
        """Extract text from PDF and return page-wise content"""
        # TODO: Implement PDF text extraction
        # - Use pdfplumber or PyPDF2 to extract text from each page
        # - Return list of dictionaries with page content and metadata
        result = []
        with pdfplumber.open(file_path) as file:
            for page in file.pages:
                result.append({
                    'page': page.page_number,
                    'filename': filename,
                    'content': page.extract_text() or ""
                })

        return result
    
    def split_into_chunks(self, pages_content: List[Dict[str, Any]]) -> List[Document]:
        """Split page content into chunks"""
        # TODO: Implement text chunking
        # - Split each page content into smaller chunks
        # - Create Document objects with proper metadata
        # - Return list of Document objects
        list_document: List[Document] = []
        
        for content in pages_content:
            chunks = self.splitter.split_text(content['content'])
            for chunk in chunks:
                document = Document(
                    id=str(uuid4()),
                    page_content=chunk,
                    metadata=content
                )
                list_document.append(document)
        
        return list_document
    
    def process_pdf(self, file_path: str, filename: str) -> List[Document]:
        """Process PDF file and return list of Document objects"""
        # TODO: Implement complete PDF processing pipeline
        # 1. Extract text from PDF
        # 2. Split text into chunks
        # 3. Return processed documents
        pages_content = self.extract_text_from_pdf(file_path, filename)
        return self.split_into_chunks(pages_content)