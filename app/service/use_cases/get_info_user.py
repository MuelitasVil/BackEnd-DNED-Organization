from typing import Dict, List, Optional, Set, Tuple
from sqlmodel import Session
from fastapi import HTTPException
from sqlalchemy import text

from app.domain.models.user_unal import UserUnal
from app.domain.dtos.user_unal.user_info import (
    UserAcademicAssociation,
    UserInfoAssociation,
    UserInfoData,
)

from app.service.crud.user_unal_service import UserUnalService
from app.utils.app_logger import AppLogger

logger = AppLogger(__file__)


def get_info_user(
    email_unal: str,
    session: Session
) -> Optional[UserInfoAssociation]:
    """
    Llama al SP GetUserAcademicData y procesa los resultados en un DTO
    con la informacion del usuario separada de sus asociaciones por periodo.
    """

    user: UserUnal = UserUnalService.get_by_email(email_unal, session)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    stmt = (
        text("CALL get_user_academic_data(:email)")
        .bindparams(email=email_unal)
    )

    result = session.exec(stmt).mappings().all()
    user_info = UserInfoAssociation(
        user_info=UserInfoData(
            email_unal=email_unal,
            document=user.document,
            name=user.name,
            lastname=user.lastname,
            full_name=user.full_name,
            gender=user.gender,
            birth_date=user.birth_date,
            headquarters=user.headquarters,
        ),
        periods={}
    )

    temp_dict: Dict[str, List[UserAcademicAssociation]] = {}
    seen_associations: Set[
        Tuple[
            str,
            Optional[str],
            Optional[str],
            Optional[str],
            Optional[str],
        ]
    ] = set()

    for row in result:
        period = row["cod_period"]
        headquarters_code = row["cod_headquarters"]
        headquarters_name = row["headquarters_name"]
        school_code = row["cod_school"]
        school_name = row["school_name"]
        unit_code = row["cod_unit"]
        unit_name = row["unit_name"]
        type_user_name = row.get("type_user_name")
        type_user_description = row.get("type_user_description")

        association_key = (
            period,
            headquarters_code,
            school_code,
            unit_code,
            type_user_name,
        )
        if association_key in seen_associations:
            continue
        seen_associations.add(association_key)

        if period not in temp_dict:
            temp_dict[period] = []

        temp_dict[period].append(
            UserAcademicAssociation(
                headquarters_code=headquarters_code,
                headquarters_name=headquarters_name,
                school_code=school_code,
                school_name=school_name,
                unit_code=unit_code,
                unit_name=unit_name,
                type_user_name=type_user_name,
                type_user_description=type_user_description,
            )
        )

    user_info.periods = temp_dict
    return user_info
