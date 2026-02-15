from sqlalchemy import Column, Integer, String, Text, DateTime
from ..database import Base  # Import Base from the database.py file
from datetime import datetime

class Interview(Base):
    """
    Example Database Model for an Interview.
    This class represents a table in the database called 'interviews'.
    """
    __tablename__ = "interviews"  # This is the table name in SQL

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Explanation:
    # 1. Base: Inheriting from Base connects this Python class to the database table.
    # 2. Columns: Define the data types (Integer, String, etc.) for each field.
    # 3. primary_key=True: This field uniquely identifies each row.
    # 4. index=True: Makes searching by this column faster.
