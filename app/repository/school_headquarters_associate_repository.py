from sqlmodel import Session, and_, insert, select
from typing import List, Optional

from app.domain.models.school_headquarters_associate import (
    SchoolHeadquartersAssociate
)


class SchoolHeadquartersAssociateRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(
        self, start: int = 0, limit: int = 100
    ) -> List[SchoolHeadquartersAssociate]:
        return self.session.exec(
            select(SchoolHeadquartersAssociate).offset(start).limit(limit)
        ).all()

    def get_by_id(
            self,
            cod_school: str,
            cod_headquarters: str,
            cod_period: str
    ) -> Optional[SchoolHeadquartersAssociate]:
        return self.session.get(
            SchoolHeadquartersAssociate,
            (cod_school, cod_headquarters, cod_period)
        )

    def get_by_school(
        self, cod_school: str, cod_period: str = None
    ) -> List[SchoolHeadquartersAssociate]:
        statement = select(SchoolHeadquartersAssociate).where(
            and_(
                SchoolHeadquartersAssociate.cod_school == cod_school,
                SchoolHeadquartersAssociate.cod_period == cod_period
            )
        )
        return self.session.exec(statement).all()

    def get_by_headquarters(
            self,
            cod_headquarters: str,
            cod_period: str = None
    ) -> List[SchoolHeadquartersAssociate]:
        statement = select(SchoolHeadquartersAssociate).where(
            and_(
                SchoolHeadquartersAssociate.cod_headquarters == cod_headquarters,  # noqa: E501
                SchoolHeadquartersAssociate.cod_period == cod_period
            )
        )
        return self.session.exec(statement).all()

    def create(
            self,
            assoc: SchoolHeadquartersAssociate
    ) -> SchoolHeadquartersAssociate:
        self.session.add(assoc)
        self.session.commit()
        self.session.refresh(assoc)
        return assoc

    def delete(
            self,
            cod_school: str,
            cod_headquarters: str,
            cod_period: str
    ) -> bool:
        assoc = self.get_by_id(cod_school, cod_headquarters, cod_period)
        if assoc:
            self.session.delete(assoc)
            self.session.commit()
            return True
        return False

    def bulk_insert_ignore(
        self, unitUnal: List[SchoolHeadquartersAssociate]
    ):
        """
        Inserta múltiples usuarios en la tabla.
        Si encuentra PK duplicada (email_unal), ignora ese registro.
        """
        stmt = insert(SchoolHeadquartersAssociate).values(
            [u.model_dump() for u in unitUnal]
        )
        stmt = stmt.prefix_with("IGNORE")
        self.session.exec(stmt)
        self.session.commit()
