from typing import List, Tuple
from langchain.schema import Document
from langchain_chroma import Chroma
from langchain_community.vectorstores import VectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from services.api import ApiException
from config import settings
from models.schemas import ChunkInfo
from uuid import uuid4
import logging

logger = logging.getLogger(__name__)

class VectorStoreService:
    def __init__(self):
        # TODO: Initialize vector store (ChromaDB, FAISS, etc.)

        self.vector_store = self._initial_vector_store()
    
    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to the vector store"""
        # TODO: Implement document addition to vector store
        # - Generate embeddings for documents
        # - Store documents with embeddings in vector database

        self.vector_store.add_documents(documents=documents)
    
    def similarity_search(self, query: str, k: int = None) -> List[Tuple[Document, float]]:
        """Search for similar documents"""
        # TODO: Implement similarity search
        # - Generate embedding for query
        # - Search for similar documents in vector store
        # - Return documents with similarity scores

        result = self.vector_store.similarity_search_with_score(query, k=k or settings.retrieval_k)
        return result
    
    def delete_documents(self, document_ids: List[str]) -> None:
        """Delete documents from vector store"""
        # TODO: Implement document deletion
        
        self.vector_store.delete(ids=document_ids)
    
    def get_all_document(self) -> List[ChunkInfo]:
        return self._get_all_document()

    def get_document_count(self) -> int:
        """Get total number of documents in vector store"""
        # TODO: Return document count

        if hasattr(self.vector_store, "collection") and hasattr(self.vector_store.collection, "count"):  # Chroma
            return self.vector_store.collection.count()
    
        logger.error("Document count not supported for this vector store.")
        raise ApiException("Document count not supported for this vector store.", code=500)

    def _initial_vector_store(self) -> Chroma:
        vector_db_type = settings.vector_db_type
        persist_directory = settings.vector_db_path
        embeddings = HuggingFaceEmbeddings(model_name=settings.embedding_model)

        if vector_db_type == "chromadb":
            return Chroma(
                collection_name="vector_collection",
                embedding_function=embeddings,
                persist_directory=persist_directory,
            )
        
        logger.error(f"Vector DB type '{vector_db_type}' is not supported.")
        raise ApiException(f"Unsupported vector_db_type: {vector_db_type}", code=500)
    
    def _get_all_document(self) -> List[ChunkInfo]:
        vector_db_type = settings.vector_db_type
        if vector_db_type == "chromadb":
            results = self.vector_store.get()
            return [
                ChunkInfo(
                    content=doc,
                    id=id_,
                    metadata=metadata,
                    page=metadata.get("page", 0)
                )
                for id_, doc, metadata in zip(results['ids'], results['documents'], results['metadatas'])
            ]
        
        logger.error(f"Vector DB type '{vector_db_type}' is not supported.")
        raise ApiException(code=500, message=f"Unsupported vector_db_type: {vector_db_type}")