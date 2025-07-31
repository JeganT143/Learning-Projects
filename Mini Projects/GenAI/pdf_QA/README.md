# PDF Research Helper

Upload PDFs and ask questions about their content using AI.

## Setup

1. Install dependencies:
```bash
pip install streamlit PyPDF2 langchain langchain-openai python-dotenv faiss-cpu
```

2. Create `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

3. Run the app:
```bash
streamlit run app.py
```

## Usage

1. Upload a PDF file
2. Ask questions about the content
3. Get AI-powered answers with examples

## Features

- PDF text extraction
- Vector-based document search
- Clear explanations with real-world analogies
- Simple web interface