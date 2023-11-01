from pydantic import BaseModel, EmailStr

from typing import List, Optional, Dict, Any

class EmailSchema(BaseModel):
    recipients: Optional[List[str]]=None
    body: Optional[str]=None
    subject: Optional[str]=None
    template_name:Optional[str]=None
    template_kwargs: Optional[Dict[str, Any]]=None