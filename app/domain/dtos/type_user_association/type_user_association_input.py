from pydantic import BaseModel


class TypeUserAssociationInput(BaseModel):
    email_unal: str
    type_user_name: str
    cod_period: str
