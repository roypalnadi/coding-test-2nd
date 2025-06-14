from fastapi import FastAPI, Request, UploadFile, File, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from models.schemas import ChatRequest, ChatResponse, DocumentsResponse, UploadResponse, ChunksResponse, DocumentInfo
from services.pdf_processor import PDFProcessor
from services.vector_store import VectorStoreService
from services.rag_pipeline import RAGPipeline
from services.api import ApiResponse, ApiException
from config import settings
from sqlite.database import db, engine, Base
from sqlite.models import pdf
from datetime import datetime
import logging
import time
import static

# Configure logging
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="RAG-based Financial Statement Q&A System",
    description="AI-powered Q&A system for financial documents using RAG",
    version="1.0.0"
)

print(settings.allowed_origins)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
# TODO: Initialize your services here
pdf_processor: PDFProcessor
vector_store: VectorStoreService
rag_pipeline: RAGPipeline

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    # TODO: Initialize your services
    global pdf_processor
    global vector_store
    global rag_pipeline

    logger.info("Starting RAG Q&A System...")
    pdf_processor = PDFProcessor()
    vector_store = VectorStoreService()
    rag_pipeline = RAGPipeline(vector_store=vector_store)
    Base.metadata.create_all(bind=engine)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(exc)
    code = 500
    data = None

    message = "Internal Server Error"

    if isinstance(exc, ApiException):
        code = exc.code
        message = exc.message
        data = exc.data

    if data == {}:
        data = None

    return ApiResponse(
        message=message,
        code=code,
        data=data
    )

@app.get("/")
async def root():
    """Health check endpoint"""
    return ApiResponse(message="RAG-based Financial Statement Q&A System is running", code=200)

@app.post("/api/upload")
async def upload_pdf(file: UploadFile = File(...), db: Session= Depends(db)):
    """Upload and process PDF file"""
    # TODO: Implement PDF upload and processing
    # 1. Validate file type (PDF)
    # 2. Save uploaded file
    # 3. Process PDF and extract text
    # 4. Store documents in vector database
    # 5. Return processing results

    try:
        start_time = time.time()

        if file.content_type not in static.ALLOWED_EXTENSION:
            raise ApiException(400, message = "Only PDFs are allowed.")

        data = await file.read()    
        if len(data) >= static.MAX_SIZE:
            raise ApiException(400, message = "Maximum limit (10MB).")
        
        file_path = f"{settings.pdf_upload_path}/{file.filename}"

        with open(file_path, "wb") as f:
            f.write(data)

        data = pdf_processor.process_pdf(file_path, file.filename)

        chunk_count = len(data)

        pdf.create(
            filename=file.filename,
            chunks_count=chunk_count,
            path=file_path,
            status="proccess",
            upload_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            db=db
        )

        end_time = time.time()
        elapsed_time = end_time - start_time

        vector_store.add_documents(data)
    except Exception as e:
        logger.error(e)
        raise e
    
    data = UploadResponse(
        chunks_count=chunk_count,
        filename=file.filename,
        message="Success",
        processing_time=elapsed_time,
    )

    return ApiResponse(
        message="Success",
        code=200,
        data=data.model_dump(mode="json")
    )


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Process chat request and return AI response"""
    # TODO: Implement chat functionality
    # 1. Validate request
    # 2. Use RAG pipeline to generate answer
    # 3. Return response with sources

    start_time = time.time()
    rag_result = rag_pipeline.generate_answer(question=request.question, chat_history=request.chat_history)

    end_time = time.time()
    elapsed_time = end_time - start_time

    response = ChatResponse(
        answer=rag_result["answer"],
        sources=rag_result["sources"],
        processing_time=elapsed_time
    )

    return ApiResponse(code=200, message="Success", data=response.model_dump(mode="json"))


@app.get("/api/documents")
async def get_documents(db: Session= Depends(db)):
    """Get list of processed documents"""
    # TODO: Implement document listing
    # - Return list of uploaded and processed documents

    pdfs = pdf.get_all(db)
    documentInfo = [DocumentInfo(
        filename=doc.filename,
        chunks_count=doc.chunks_count,
        status=doc.status,
        upload_date=datetime.strptime(doc.upload_date, "%Y-%m-%d %H:%M:%S"),
        path=doc.path,
        
    ) for doc in pdfs]

    documentResponse = DocumentsResponse(
        documents = documentInfo
    )

    return ApiResponse(code=200, message="Success", data=documentResponse.model_dump(mode="json"))


@app.get("/api/chunks")
async def get_chunks():
    """Get document chunks (optional endpoint)"""
    # TODO: Implement chunk listing
    # - Return document chunks with metadata
    list_chunk = vector_store.get_all_document()
    data = ChunksResponse(
        chunks=list_chunk,
        total_count=len(list_chunk)
    )
    
    return ApiResponse(code=200, message="Success", data=data.model_dump(mode="json"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port, reload=settings.debug) 