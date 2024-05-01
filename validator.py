from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class VacancyValidator(BaseModel):
    published_at: str
    created_at: str
    position: str
    salary_from: Optional[int] = None
    salary_to: Optional[int] = None
    currency: str
    city: Optional[str] = None
    description: str
    link: str

    def get_fields(self) -> list[str]:
        return list(self.__fields__.keys())
        



    
    