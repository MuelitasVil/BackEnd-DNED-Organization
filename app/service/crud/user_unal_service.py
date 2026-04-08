from typing import List, Optional
from app.repository.user_unal_repository import UserUnalRepository
from app.repository.user_unit_associate_repository import (
    UserUnitAssociateRepository,
)
from app.domain.models.user_unal import UserUnal
from app.domain.dtos.user_unal.user_unal_input import UserUnalInput
from sqlmodel import Session


class UserUnalService:
    @staticmethod
    def get_all(
        session: Session,
        start: int = 0,
        limit: int = 20,
    ) -> List[UserUnal]:
        return UserUnalRepository(session).get_all(start, limit)

    @staticmethod
    def get_all_no_pagination(session: Session) -> List[UserUnal]:
        repo = UserUnalRepository(session)
        start: int = 0
        limit: int = 5000
        users: List[UserUnal] = []
        while True:
            batch = repo.get_all(start=start, limit=limit)
            if not batch or len(batch) == 0:
                break
            users.extend(batch)
            start += limit
        return users

    @staticmethod
    def get_all_by_period(cod_period: str, session: Session) -> List[UserUnal]:
        associated_emails = (
            UserUnitAssociateRepository(session)
            .get_distinct_user_emails_by_period(cod_period)
        )
        return UserUnalRepository(session).get_by_emails(associated_emails)

    @staticmethod
    def get_by_email(email_unal: str, session: Session) -> Optional[UserUnal]:
        return UserUnalRepository(session).get_by_email(email_unal)

    @staticmethod
    def create(input_data: UserUnalInput, session: Session) -> UserUnal:
        user = UserUnal(**input_data.model_dump(exclude_unset=True))
        return UserUnalRepository(session).create(user)

    @staticmethod
    def update(
        email_unal: str,
        input_data: UserUnalInput,
        session: Session
    ) -> Optional[UserUnal]:
        return UserUnalRepository(session).update(email_unal, input_data)

    @staticmethod
    def save(input_data: UserUnalInput, session: Session) -> UserUnal:
        if UserUnalService.get_by_email(input_data.email_unal, session):
            return UserUnalService.update(
                input_data.email_unal, input_data, session
            )
        return UserUnalService.create(input_data, session)

    @staticmethod
    def delete(email_unal: str, session: Session) -> bool:
        return UserUnalRepository(session).delete(email_unal)

    @staticmethod
    def bulk_insert_ignore(users: List[UserUnalInput], session: Session):
        """
        Inserta en bulk usuarios.
        Si hay duplicados en email_unal, MySQL los ignora.
        """
        user_models = [
            UserUnal(**u.model_dump(exclude_unset=True))
            for u in users
        ]
        UserUnalRepository(session).bulk_insert_ignore(user_models)
        return {"inserted": len(users), "duplicates_ignored": True}
