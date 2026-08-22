# SHL Assessment Recommendation System

This project is an AI-driven recommendation engine designed to help technical recruiters select appropriate SHL assessments for candidates based on conversational context and specific job requirements.

## Architecture

The system is built with a modular decoupled architecture:

- **Backend**: FastAPI-based REST API that handles conversation logic and retrieval.
- **Frontend**: Streamlit-based chatbot interface for recruiters.
- **Intelligence**: Google Gemini 2.5 Flash for natural language understanding and search query extraction.
- **Vector Database**: FAISS (Facebook AI Similarity Search) for efficient semantic retrieval of assessments.
- **Embeddings**: Sentence-Transformers (`all-MiniLM-L6-v2`) for transforming catalog data into searchable vectors.

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Configuration**:
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

3. **Prepare Database**:
   If the catalog has been cleaned, run the following to build the FAISS index:
   ```bash
   python build_vector_db.py
   ```

## Running the Application

The system requires both the backend and frontend services to be running.

### 1. Start the Backend
```bash
python main.py
```
The API will be available at `http://127.0.0.1:8000`.

### 2. Start the Frontend
```bash
python -m streamlit run frontend/app.py
```
The interface will open in your default browser at `http://localhost:8501`.

## API Usage

The backend exposes a POST endpoint for chat interactions.

- **Endpoint**: `/chat`
- **Method**: `POST`
- **Payload**:
  ```json
  {
    "messages": [
      {"role": "user", "content": "I need a technical assessment for a Java role."}
    ]
  }
  ```

## Frontend Usage

The Streamlit interface provides a simple chat window:
- Type your requirements in the input box at the bottom.
- Recommendations appear as interactive cards with direct links to the SHL product pages.
- The assistant maintains context throughout the conversation, allowing for follow-up questions.

## Sample Recruiter Queries

- "Suggest some assessments for a junior Python developer."
- "Do you have any cognitive ability tests that support remote proctoring?"
- "Compare the personality assessments available in the catalog."
- "What would be good for a leadership role in a tech team?"

rebuilding it
