from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.issue import SeverityLevel, IssueStatus


# These Pydantic models are used for validating and serializing data in your API endpoints. 
# They define the structure of the data that your API expects to receive (for creating and updating issues) and the structure of the data that it will return in responses (for issue details). 
# By using these models, you can ensure that the data being processed by your API is consistent and adheres to the expected format, which helps prevent errors and makes it easier to work with the data throughout your application.

#what the user sends when creating an issue (no id, no created_at, no resolved_at)
class IssueCreate(BaseModel):
    title: str
    description: Optional[str] = None
    pipeline_name: str
    error_message: Optional[str] = None
    severity: SeverityLevel = SeverityLevel.MEDIUM
    assigned_to: Optional[str] = None

#what the user sends when updating an issue (only fields they're allowed to change)
class IssueUpdate(BaseModel):
    severity: Optional[SeverityLevel] = None
    status: Optional[IssueStatus] = None
    assigned_to: Optional[str] = None
    resolution: Optional[str] = None
    resolved_at: Optional[datetime] = None

#what your API sends back (everything including id, created_at etc)
class IssueResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    pipeline_name: str
    error_message: Optional[str] = None
    severity: SeverityLevel
    assigned_to: Optional[str] = None
    status: IssueStatus
    resolution: Optional[str] = None
    resolved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True