from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional, List
from app.db.session import get_db
from app.schemas.issue import IssueCreate, IssueUpdate, IssueResponse
from app.models.issue import SeverityLevel, IssueStatus
from app.services import issue_service

# This file defines the API routes for managing issues. Each route corresponds to a specific HTTP method and endpoint, 
# and it uses the service layer to perform the necessary operations on the database. 
# The routes handle incoming HTTP requests, validate the data using Pydantic schemas, and return appropriate responses. 
# router - It's a sub-router
router = APIRouter()

@router.post("/", response_model=IssueResponse)
def create_issue_endpoint(issue_data: IssueCreate, db: Session = Depends(get_db)):
    return issue_service.create_issue(db, issue_data)

@router.get("/", response_model=List[IssueResponse])
def get_all_issues_endpoint(
    pipeline_name: Optional[str] = None,
    severity: Optional[SeverityLevel] = None,
    status: Optional[IssueStatus] = None,
    assigned_to: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return issue_service.get_all_issues(db, pipeline_name, severity, status, assigned_to)

@router.get("/{id}", response_model=IssueResponse)
def get_issue_endpoint(id: int, db: Session = Depends(get_db)):
    return issue_service.get_issue(db, id)

@router.patch("/{id}", response_model=IssueResponse)
def update_issue_endpoint(id: int, issue_data: IssueUpdate, db: Session = Depends(get_db)):
    return issue_service.update_issue(db, id, issue_data)

@router.delete("/{id}", response_model=IssueResponse)
def delete_issue_endpoint(id: int, db: Session = Depends(get_db)):
    return issue_service.delete_issue(db, id)