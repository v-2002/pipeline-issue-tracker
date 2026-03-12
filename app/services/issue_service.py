from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.issue import Issue, IssueStatus
from app.schemas.issue import IssueCreate, IssueUpdate

# This service layer contains the core business logic for managing issues. 
# It interacts directly with the database using SQLAlchemy sessions and performs operations such as creating, retrieving, updating, and deleting issues. 
# By centralizing this logic in a service layer, you can keep your API endpoints clean and focused on handling HTTP requests and responses,
# while the service layer takes care of the underlying data manipulation and business rules. 
# This separation of concerns makes your code more modular, easier to maintain, and testable.
def create_issue(db: Session, issue_data: IssueCreate):
    db_issue = Issue(
        title=issue_data.title,
        description=issue_data.description,
        pipeline_name=issue_data.pipeline_name,
        error_message=issue_data.error_message,
        severity=issue_data.severity,
        assigned_to=issue_data.assigned_to
    )
    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)
    return db_issue

#get_issue retrieves a single issue by its ID. If the issue doesn't exist, it raises a 404 HTTPException.
def get_issue(db: Session, id: int):
    db_issue = db.query(Issue).filter(Issue.id == id).first()
    if not db_issue:
        raise HTTPException(status_code=404, detail=f"Issue with id {id} not found")
    return db_issue

#get_all_issues retrieves a list of issues, optionally filtered by pipeline name, severity, status, or assigned user. 
# It builds a query based on the provided filters and returns the results.
def get_all_issues(db: Session, pipeline_name=None, severity=None, status=None, assigned_to=None):
    query = db.query(Issue)
    if pipeline_name:
        query = query.filter(Issue.pipeline_name == pipeline_name)
    if severity:
        query = query.filter(Issue.severity == severity)
    if status:
        query = query.filter(Issue.status == status)
    if assigned_to:
        query = query.filter(Issue.assigned_to == assigned_to)
    return query.all()

#update_issue allows updating certain fields of an existing issue. 
# It first retrieves the issue by ID, checks if it exists, and then updates the fields that were provided in the IssueUpdate schema.
def update_issue(db: Session, id: int, issue_data: IssueUpdate):
    db_issue = db.query(Issue).filter(Issue.id == id).first()
    if not db_issue:
        raise HTTPException(status_code=404, detail=f"Issue with id {id} not found")
    update_data = issue_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_issue, key, value)
    db.commit()
    db.refresh(db_issue)
    return db_issue

#delete_issue doesn't actually delete the record from the database. 
#Instead, it marks the issue as "CLOSED" by updating its status. 
# This is a common practice in issue tracking systems to preserve the history of issues while indicating that they are no longer active.
def delete_issue(db: Session, id: int):
    db_issue = db.query(Issue).filter(Issue.id == id).first()
    if not db_issue:
        raise HTTPException(status_code=404, detail=f"Issue with id {id} not found")
    setattr(db_issue, "status", IssueStatus.CLOSED)
    db.commit()
    db.refresh(db_issue)
    return db_issue