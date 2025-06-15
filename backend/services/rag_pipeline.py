from collections import defaultdict
from typing import List, Dict, Any
from langchain_huggingface import HuggingFaceEndpoint
from langchain.prompts.prompt import PromptTemplate
from services.vector_store import VectorStoreService
from models.schemas import DocumentSource
from config import settings
import logging

logger = logging.getLogger(__name__)


class RAGPipeline:
    def __init__(self, vector_store: VectorStoreService):
        # TODO: Initialize RAG pipeline components
        # - Vector store service
        # - LLM client
        # - Prompt templates

        self.vector_store = vector_store
        self.llm = HuggingFaceEndpoint(
            repo_id=settings.llm_model,
            temperature=settings.llm_temperature,
            max_new_tokens=settings.max_tokens,
            huggingfacehub_api_token=settings.huggingface_token,
        )
        
        self.prompt_template = PromptTemplate(
            input_variables=['context', 'question', 'chat_history'],
            template="""
                <s>[INST] 
                You are a helpful AI assistant. 
                You must answer the question using ONLY the provided context. 

                Conversation History:
                {chat_history}

                Context:
                {context}

                Question:
                {question}

                Answer:
                [/INST]
                """.strip()
        )
    
    def generate_answer(self, question: str, chat_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """Generate answer using RAG pipeline"""
        # TODO: Implement RAG pipeline
        # 1. Retrieve relevant documents
        # 2. Generate context from retrieved documents
        # 3. Generate answer using LLM
        # 4. Return answer with sources

        documents = self._retrieve_documents(question)
        context = self._generate_context(documents)
        response = self._generate_llm_response(question, context, chat_history)
        try:

            return {
                "answer": response,
                "sources": documents
            }
        except Exception as e:
            logger.error(e)
            return {
                "answer": "Sorry, an error occurred while processing your request.",
                "sources": []
            }
    
    def _retrieve_documents(self, query: str) -> List[DocumentSource]:
        """Retrieve relevant documents for the query"""
        # TODO: Implement document retrieval
        # - Search vector store for similar documents
        # - Filter by similarity threshold
        # - Return top-k documents
        result_search = self.vector_store.similarity_search(query, settings.retrieval_k)
        documents: List[DocumentSource] = []
        for doc, score in result_search: 
            if not doc.page_content.strip():
                continue

            if score <= settings.similarity_threshold:
                document_source = DocumentSource(
                    content=doc.page_content,
                    page=doc.metadata.get("page", 0),
                    metadata=doc.metadata,
                    score=score
                )
                documents.append(document_source)
        return documents

    def _generate_context(self, documents: List[DocumentSource]) -> str:
        """Generate context from retrieved documents"""
        # TODO: Generate context string from documents
        return "\n\n".join(f"[Source: Page {document.page}] {document.content}" for document in documents)
    
    def _generate_llm_response(self, question: str, context: str, chat_history: List[Dict[str, str]] = None) -> str:
        """Generate response using LLM"""
        # TODO: Implement LLM response generation
        # - Create prompt with question and context
        # - Call LLM API
        # - Return generated response

        chat_history_str: str = ""
        if chat_history:
            for chat in chat_history:
                chat_history_str += f"User: {chat['user']}\nAssistant: {chat['assistant']}\n"

        inputs = {
            "chat_history": chat_history_str.strip(),
            "context": context,
            "question": question
        }

        formatted = self.prompt_template.format(**inputs)
        # Gunakan raw_response untuk mendapatkan objek Response
        return self.llm.invoke(formatted)