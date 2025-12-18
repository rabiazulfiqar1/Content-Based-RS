# Content-Based Recommendation System

It is a intelligent platform designed to connect developers with open-source projects, Kaggle competitions, and datasets that perfectly match their skills, interests, and learning goals.

At its core is a **Hybrid Recommendation Engine** that combines the power of semantic vector search with traditional collaborative filtering techniques to provide highly personalized suggestions.

## 🚀 Key Features

* **🧠 Semantic Search:** Uses **Sentence Transformers** (`all-MiniLM-L6-v2`) and **cosine similarity** to understand the meaning behind project descriptions and user profiles.
* **🎯 Hybrid Scoring Algorithm:** Weighted system for ranking projects:
  - **50% Semantic Similarity**: How well the project matches your profile.
  - **25% Skill Match**: Direct mapping of your known skills to project requirements.
  - **15% Difficulty Alignment**: Ensures projects fit your skill level.
  - **10% Growth Opportunity**: Rewards projects that teach 1–3 new skills.
* **👤 Comprehensive User Profiles:** Tracks proficiency levels, interests, GitHub activity, and preferred project types.
* **📊 Interaction Learning:** Learns from user interactions (views, bookmarks, starts, completions) to improve recommendations.

---

## 🗄️ Data Generation & Recommendation System

### Key Features


"""
1. **Skill Categories & Core Skills**(26 Core Skills)
On startup, the system seeds 26 fundamental technical skills across 4 categories:
==============================

| Category     | Skills                                                                 |
|--------------|------------------------------------------------------------------------|
| Languages    | Python, JavaScript, TypeScript, Java, Go                                
| Frameworks   | React, Next.js, Vue.js, HTML/CSS, Node.js, FastAPI, Django, Flask       
| Tools        | PostgreSQL, MongoDB, Redis, Docker, Kubernetes, AWS, Git               
| Domains      | Machine Learning, Deep Learning, NLP, Computer Vision, API Development, Web Development 
"""

2. **Embedding Generation**
   - Converts project metadata (title, description, topics, skills) into **384-dimensional semantic vectors**.
   - Supports **natural language search** and **similarity-based project discovery**.
   - Fast batch processing with optional IVFFlat indexing.

3. **Difficulty Inference**
   - ML-based classification into **Beginner**, **Intermediate**, or **Advanced**.
   - Evaluates 20+ factors including stars, forks, topics, language, size, and project activity.
   - Ensures **consistent, objective difficulty scoring**.

4. **User Profile Matching**

   - Generates personalized **match scores** combining:
     - Semantic similarity (50%)
     - Skill match (25%)
     - Difficulty alignment (15%)
     - Growth opportunity (10%)
   - Helps users find projects that **fit their skill level and learning goals**.

* FinalScore=(0.50⋅Semantic_Similarity)+(0.25⋅Skill_Overlap)+(0.15⋅Difficulty_Match)+(0.10⋅Growth_Bonus)

**Benefits:** Automatic difficulty classification, personalized learning paths, and explainable scoring.

---

## 🖥️ Recommender System API

### Features

* **Project Search & Recommendations**
  - `/projects/search`: Search projects via keywords or semantic similarity.
  - `/projects/{project_id}`: Get project details with optional hybrid match analysis.
  - Kaggle-specific endpoints for competitions and datasets.

* **User Profile Management**
  - `/users/{user_id}/profile` (POST/GET): Create, update, or fetch user profiles.
  - Stores skill proficiency, interests, bio, GitHub username, and preferred project types.

* **Interaction Tracking**
  - `/interactions`: Create, update, delete interactions with projects (viewed, bookmarked, started, completed).
  - `/interactions/{user_id}`: Fetch user interactions.
  - `/interactions/{user_id}/stats`: Get interaction stats and activity summaries.
  - `/users/{user_id}/activity-summary`: Comprehensive user activity insights.

* ** Recommendation Engine**
  - Combines semantic similarity with skill matching, difficulty alignment, and growth opportunities.
  - Provides **explainable reasons** for each recommendation.

---
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
