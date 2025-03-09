# This is a Star Schema model:
# `hired_employees` is the **fact table**, storing hiring events.
# `departments` and `jobs` are **dimension tables**, providing descriptive data.

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class Department(Base):
    """Represents a department in the company."""
    
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)  
    employees = relationship("HiredEmployee", back_populates="department", cascade="all, delete")

class Job(Base):
    """Represents a job position."""
    
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    employees = relationship("HiredEmployee", back_populates="job", cascade="all, delete")

class HiredEmployee(Base):
    """Represents an employee who has been hired."""
    
    __tablename__ = "hired_employees"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Employee name is required
    datetime = Column(DateTime, nullable=False)  # Hire date is required

    # Foreign Keys (FK)
    department_id = Column(Integer, ForeignKey("departments.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    department = relationship("Department", back_populates="employees")
    job = relationship("Job", back_populates="employees")