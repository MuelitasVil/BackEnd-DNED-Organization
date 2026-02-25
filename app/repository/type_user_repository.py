from sqlmodel import Session, insert, select
from typing import List, Optional

from app.domain.models.type_user import TypeUser
from app.domain.dtos.type_user.type_user_input import TypeUserInput


class TypeUserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(
            self, start: int = 0, limit: int = 100
    ) -> List[TypeUser]:
        return self.session.exec(
            select(TypeUser).offset(start).limit(limit)
        ).all()

    def get_by_name(self, name: str) -> Optional[TypeUser]:
        return self.session.get(TypeUser, name)

    def create(self, type_user: TypeUser) -> TypeUser:
        self.session.add(type_user)
        self.session.commit()
        self.session.refresh(type_user)
        return type_user

    def update(
        self,
        type_user_name: str,
        data: TypeUserInput
    ) -> Optional[TypeUser]:
        record = self.get_by_name(type_user_name)
        if not record:
            return None

        update_data = data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(record, key, value)

        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)
        return record

    def delete(self, type_user_name: str) -> bool:
        record = self.get_by_name(type_user_name)
        if record:
            self.session.delete(record)
            self.session.commit()
            return True
        return False
    
    def bulk_insert_ignore(self, type_users: List[TypeUser]):
        """
        Inserta múltiples tipos de usuario en la tabla.
        Si encuentra PK duplicada (name), ignora ese registro.
        """
        stmt = insert(TypeUser).values(
            [u.model_dump() for u in type_users]
        )
        stmt = stmt.prefix_with("IGNORE")
        self.session.exec(stmt)
        self.session.commit()
