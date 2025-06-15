## Getting Started

### 1. **Environment Setup**
```bash
# Clone repository
git clone <your-repository-url>
cd coding-test-2nd

# Set up Python virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. **Backend Setup**
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (create .env file)
HUGGINGFACE_TOKEN=your_huggingface_token

# Run server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. **Frontend Setup**
```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

**Build a smarter document Q&A system with RAG technology!** 