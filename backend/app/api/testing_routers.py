from typing import Optional
from fastapi import Depends, HTTPException, Query, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, insert
from datetime import datetime
from app.database.sql_engine import get_db_session
from app.database.tables import (
    projects,
    project_embeddings
)
from app.models.schemas import InteractionCreate
from app.api.rs import ( 
    ensure_project_embedding,
    user_project_interactions,
    generate_recommendations
)

router = APIRouter()

# ------ RECOMMENDATIONS (VECTOR-ENHANCED) ------

@router.get("/recommendations/{user_id}")
async def get_recommendations(
    user_id: str,
    limit: int = Query(10, le=50),
    algorithm: str = Query("hybrid", regex="^(hybrid|semantic|traditional)$"),
    source_filter: Optional[str] = Query(None, regex="^(github|kaggle_competition|kaggle_dataset|curated|all)$"),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get personalized project recommendations
    
    Algorithms:
    - hybrid (default): Combines semantic search + skill matching
    - semantic: Pure vector similarity
    - traditional: Legacy keyword/skill matching
    
    Source Filters:
    - github: GitHub repositories
    - kaggle_competition: Kaggle competitions
    - kaggle_dataset: Kaggle datasets (analysis projects)
    - curated: Hand-picked projects
    - all (default): All sources
    """
    
    return await generate_recommendations(
        user_id=user_id,
        db=db,
        limit=limit,
        algorithm=algorithm,
        source_filter=source_filter
    )

# ------ INTERACTIONS ------

@router.post("/interactions/{user_id}")
async def log_interaction(
    user_id: str,
    interaction: InteractionCreate,
    db: AsyncSession = Depends(get_db_session)
):
    """Log user interaction with project"""
    
    await db.execute(
        insert(user_project_interactions).values(
            user_id=user_id,
            project_id=interaction.project_id,
            interaction_type=interaction.interaction_type,
            rating=interaction.rating,
            created_at=datetime.utcnow()
        )
    )
    
    return {"message": "Interaction logged successfully"}

@router.get("/interactions/{user_id}")
async def get_user_interactions(
    user_id: str,
    db: AsyncSession = Depends(get_db_session)
):
    """Get user's project interactions"""
    
    result = await db.execute(
        select(user_project_interactions, projects.c.title)
        .join(projects, user_project_interactions.c.project_id == projects.c.id)
        .where(user_project_interactions.c.user_id == user_id)
        .order_by(user_project_interactions.c.created_at.desc())
    )
    
    interactions = [
        {
            'id': row.id,
            'project_id': row.project_id,
            'project_title': row.title,
            'interaction_type': row.interaction_type,
            'rating': row.rating,
            'created_at': row.created_at
        }
        for row in result.fetchall()
    ]
    
    return {"interactions": interactions}

# ------ EMBEDDING MANAGEMENT ------

@router.post("/admin/embeddings/generate")
async def generate_all_embeddings(
    db: AsyncSession = Depends(get_db_session)
):
    """Generate embeddings for all projects (admin endpoint)"""
    
    result = await db.execute(select(projects.c.id))
    project_ids = [row[0] for row in result.fetchall()]
    
    generated = 0
    skipped = 0
    
    for project_id in project_ids:
        result = await db.execute(
            select(project_embeddings).where(project_embeddings.c.project_id == project_id)
        )
        
        if result.first():
            skipped += 1
            continue
        
        await ensure_project_embedding(project_id, db)
        generated += 1
    
    return {
        "message": "Embedding generation complete",
        "generated": generated,
        "skipped": skipped,
        "total": len(project_ids)
    }

@router.post("/admin/embeddings/regenerate/{project_id}")
async def regenerate_project_embedding(
    project_id: int,
    db: AsyncSession = Depends(get_db_session)
):
    """Regenerate embedding for a specific project"""
    
    # Delete existing
    await db.execute(
        delete(project_embeddings).where(project_embeddings.c.project_id == project_id)
    )
    
    # Generate new
    await ensure_project_embedding(project_id, db)
    
    return {"message": f"Embedding regenerated for project {project_id}"}