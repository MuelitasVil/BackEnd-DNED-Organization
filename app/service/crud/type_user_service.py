from sqlalchemy.orm import Session
from typing import List, Optional

from app.repository.type_user_repository import TypeUserRepository
from app.domain.models.type_user import TypeUser
from app.domain.dtos.type_user.type_user_input import TypeUserInput


class TypeUserService:
    @staticmethod
    def get_all(
        session: Session, start: int = 0, limit: int = 100
    ) -> List[TypeUser]:
        repo = TypeUserRepository(session)
        return repo.get_all(start=start, limit=limit)

    @staticmethod
    def get_by_name(name: str, session: Session) -> Optional[TypeUser]:
        repo = TypeUserRepository(session)
        return repo.get_by_name(name)

    @staticmethod
    def create(input_data: TypeUserInput, session: Session) -> TypeUser:
        obj = TypeUser(**input_data.model_dump(exclude_unset=True))
        return TypeUserRepository(session).create(obj)

    @staticmethod
    def update(
        type_user_name: str,
        input_data: TypeUserInput,
        session: Session
    ) -> Optional[TypeUser]:
        return TypeUserRepository(session).update(type_user_name, input_data)

    @staticmethod
    def delete(type_user_name: str, session: Session) -> bool:
        return TypeUserRepository(session).delete(type_user_name)

    @staticmethod
    def bulk_insert_ignore(users: List[TypeUserInput], session: Session):
        """
        Inserta en bulk tipos de usuario.
        Si hay duplicados en name, MySQL los ignora.
        """
        user_models = [
            TypeUser(**u.model_dump(exclude_unset=True))
            for u in users
        ]
        TypeUserRepository(session).bulk_insert_ignore(user_models)
        return {"inserted": len(users), "duplicates_ignored": True}
