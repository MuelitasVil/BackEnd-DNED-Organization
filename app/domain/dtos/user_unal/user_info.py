from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class UserInfoData(BaseModel):
    email_unal: str
    document: Optional[str] = None
    name: str
    lastname: str
    full_name: Optional[str] = None
    gender: Optional[str] = None
    birth_date: Optional[str] = None
    headquarters: Optional[str] = None


class UserAcademicAssociation(BaseModel):
    headquarters_code: Optional[str] = None
    headquarters_name: Optional[str] = None
    school_code: Optional[str] = None
    school_name: Optional[str] = None
    unit_code: Optional[str] = None
    unit_name: Optional[str] = None
    type_user_name: Optional[str] = None
    type_user_description: Optional[str] = None


class UserInfoAssociation(BaseModel):
    user_info: UserInfoData
    periods: Dict[str, List[UserAcademicAssociation]] = Field(
        default_factory=dict
    )
