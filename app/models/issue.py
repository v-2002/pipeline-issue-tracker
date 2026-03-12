from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.sql import func
import enum
from app.db.session import Base

#`SeverityLevel` and `IssueStatus` are Python enums — they restrict what values are allowed. can't set status to "BANANA" — SQLAlchemy will reject it.
class SeverityLevel(enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class IssueStatus(enum.Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"

class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)  # Unique identifier for each issue, auto-incremented by the database.
    title = Column(String(200), nullable=False)  # A short title for the issue, required and limited to 200 characters.
    description = Column(Text, nullable=True)  # A detailed description of the issue, optional and can be of any length.
    pipeline_name = Column(String(100), nullable=False)  # The name of the data pipeline where the issue occurred, required and limited to 100 characters.
    error_message = Column(Text, nullable=False)  # The error message associated with the issue, required and can be of any length.
    severity = Column(Enum(SeverityLevel), default=SeverityLevel.MEDIUM, nullable=False)  # The severity level of the issue, required and must be one of the defined enum values.
    status = Column(Enum(IssueStatus), default=IssueStatus.OPEN, nullable=False)  # The current status of the issue, required and must be one of the defined enum values.
    assigned_to = Column(String(50), nullable=True)  # The name of the person assigned to resolve the issue, optional and limited to 50 characters.
    resolution = Column(Text, nullable=True)  # A detailed description of how the issue was resolved, optional and can be of any length.
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Timestamp for when the issue was created, automatically set to the current time when the record is created.
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())  # Timestamp for when the issue was last updated, automatically set to the current time whenever the record is updated.
    resolved_at = Column(DateTime(timezone=True), nullable=True)  # Timestamp for when the issue was resolved, optional and can be set when the issue is marked as resolved.
