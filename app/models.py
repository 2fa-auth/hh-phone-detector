from pydantic import BaseModel, ConfigDict, Field

class VacancyInput(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    url: str | None = None
    title: str = ""
    company: str = ""
    description: str = ""
    contacts: object | None = None

class PhoneContact(BaseModel):
    raw: str
    normalized: str
    source: str

class VacancyPhoneResult(BaseModel):
    vacancy_id: str
    url: str | None = None
    title: str = ""
    company: str = ""
    has_phone: bool
    phones: list[PhoneContact] = Field(default_factory=list)
