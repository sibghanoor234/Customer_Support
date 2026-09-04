


from typing import Optional, Literal
from pydantic import BaseModel, EmailStr

class TicketsInput(BaseModel):
    customer_name: str
    category:Optional[str] = None
    priority: Literal["low", "Medium", "High","Urgent"]
    status: Literal["open", "closed", "In-progress"]
    description:Optional[str] = None