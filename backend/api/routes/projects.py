"""
Projects API Routes
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict

router = APIRouter()

# Temporary in-memory storage for projects
projects_db: List[Dict] = []


@router.get("", response_model=List[Dict])
async def get_projects():
    """Get all projects"""
    return projects_db


@router.get("/{project_id}", response_model=Dict)
async def get_project(project_id: str):
    """Get a specific project by ID"""
    for project in projects_db:
        if project.get("id") == project_id:
            return project
    raise HTTPException(status_code=404, detail="Project not found")


@router.post("", response_model=Dict)
async def create_project(project: Dict):
    """Create a new project"""
    import uuid
    new_project = {
        "id": str(uuid.uuid4()),
        **project
    }
    projects_db.append(new_project)
    return new_project


@router.put("/{project_id}", response_model=Dict)
async def update_project(project_id: str, project_update: Dict):
    """Update an existing project"""
    for i, project in enumerate(projects_db):
        if project.get("id") == project_id:
            projects_db[i] = {**project, **project_update}
            return projects_db[i]
    raise HTTPException(status_code=404, detail="Project not found")


@router.delete("/{project_id}")
async def delete_project(project_id: str):
    """Delete a project"""
    for i, project in enumerate(projects_db):
        if project.get("id") == project_id:
            projects_db.pop(i)
            return {"message": "Project deleted"}
    raise HTTPException(status_code=404, detail="Project not found")
