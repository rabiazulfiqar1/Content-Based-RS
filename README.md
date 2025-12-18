# Content-Based Recommendation System

It is a intelligent platform designed to connect developers with open-source projects, Kaggle competitions, and datasets that perfectly match their skills, interests, and learning goals.

At its core is a **Hybrid Recommendation Engine** that combines the power of semantic vector search with traditional collaborative filtering techniques to provide highly personalized suggestions.

## 🚀 Key Features

*   **🧠 Semantic Search:**  Uses **Sentence Transformers** (`all-MiniLM-L6-v2`) and **cosine similarity** to understand the *meaning* behind project descriptions and user bios, not just keyword matching.
*   **🎯 Hybrid Scoring Algorithm:** Recommendations are ranked using a weighted system:
    *   **50% Semantic Similarity:** How well the project matches your profile context.
    *   **25% Skill Match:** Direct mapping of your known skills to project requirements.
    *   **15% Difficulty Alignment:** Ensures projects aren't too easy or too hard (Flow State).
    *   **10% Growth Opportunity:** explicitly rewards projects that teach you 1-3 new skills.
*   **👤 Comprehensive User Profiles:** Tracks proficiency levels, interests, GitHub activity, and preferred methodologies.
*   **📊 Interaction Learning:** The system learns from your interactions (views, bookmarks, starts, completions) to refine future recommendations.

## 🛠️ Tech Stack

### Backend
*   **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (High-performance Python API)
*   **Database:** PostgreSQL (via Supabase)
*   **ORM:** SQLAlchemy (Async)
*   **ML & Data:** 
    *   `sentence-transformers` for embedding generation
    *   `numpy` for cosine similarity calculations
    *   `celery` for background tasks

### Frontend
*   **Framework:** [Next.js](https://nextjs.org/)
*   **Styling:** Tailwind CSS

## 📦 Installation & Setup

### Backend

1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```

2.  Create and activate a virtual environment:
    ```bash
    python -m venv .venv
    # Windows
    .\.venv\Scripts\activate
    # Linux/Mac
    source .venv/bin/activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4.  Set up environment variables in `.env` (see `.env.sample`).

5.  Run the server:
    ```bash
    uvicorn app.main:app --reload
    ```

### Frontend

1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```

2.  Install dependencies:
    ```bash
    npm install
    # or
    yarn install
    ```

3.  Run the development server:
    ```bash
    npm run dev
    ```

Open [http://localhost:3000](http://localhost:3000) to see the application. The backend API is available at [http://localhost:8000](http://localhost:8000) (docs at `/docs`).
