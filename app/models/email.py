# app/models/email.py

from pydantic import BaseModel
from typing import List

class EmailResponse(BaseModel):
    emails: List[str]
