from dataclasses import dataclass
from fastapi import HTTPException
import re
from typing import Dict, Any, List, Tuple, Set
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.cell.cell import Cell
from sqlmodel import Session

from app.domain.dtos.type_user.type_user_input import (
    TypeUserInput
)

from app.domain.dtos.type_user_association.type_user_association_input import (
    TypeUserAssociationInput
)

from app.domain.enums.files.estudiantes_inactivos_enum import (
    EstInactSedeEnum,
    EstudianteInactivos
)

from app.service.crud.type_user_association_service import (
    TypeUserAssociationService
)

from app.service.crud.type_user_service import (
    TypeUserService
)

from app.service.excel_processor.utils.collection_utils import (
    is_unique_entity_in_set
)

from app.service.excel_processor.utils.excel_validator import (
    get_value_from_row,
    is_header_row,
    validate_row_blank_or_incomplete,
)

from app.domain.dtos.user_unal.user_unal_input import UserUnalInput
from app.service.crud.user_unal_service import UserUnalService

from app.utils.app_logger import AppLogger

logger = AppLogger(__file__)


@dataclass
class Collections:
    users: List[UserUnalInput]
    user_types: List[TypeUserInput]
    type_user_assocs: List[TypeUserAssociationInput]


@dataclass
class Seen:
    users: Set[str]
    type_user_assocs: Set[str]
    user_types: Set[str]


def case_estudiantes_inactivos(
    ws: Worksheet,
    cod_period: str,
    session: Session
) -> Dict[str, Any]:
    """
    - Valida filas vacías y celdas vacías (según Enum).
    - Construye listas de DTOs (sin duplicados por código).
    - Devuelve resumen: status, errores, conteos y previews.
    """
    errors: List[Dict[str, Any]] = []

    collections = Collections(
        users=[],
        user_types=[],
        type_user_assocs=[]
    )

    seen = Seen(
        users=set(),
        type_user_assocs=set(),
        user_types=set()
    )

    _excel_processing(
        ws,
        collections,
        seen,
        cod_period,
        errors,
    )
    results = _persist_collections(collections, session)
    # defult not log persist results.
    log_persist_results(results)
    return build_summary(collections)


def _excel_processing(
    ws: Worksheet,
    collections: Collections,
    seen: Seen,
    cod_period: str,
    errors: List[Dict[str, Any]] = [],
) -> None:
    """
    Función principal para procesar las filas del archivo Excel.
     - rows: Lista de tuplas con el índice de fila y el contenido de la fila.
    """
    logger.info(
        "Iniciando procesamiento de archivo de estudiantes inactivos"
    )
    for row_idx, row in enumerate(ws.iter_rows(), start=1):

        if is_header_row(row_idx):
            continue

        blank_or_incomplete_errors = validate_row_blank_or_incomplete(
            row,
            row_idx,
            EstudianteInactivos
        )

        if blank_or_incomplete_errors:
            errors.extend(blank_or_incomplete_errors)
            continue

        logger.debug(f"Procesando fila {row_idx}")
        logger.debug(f"Contenido de la fila: {[cell.value for cell in row]}")

        row_tuple: Tuple[Cell, ...] = row
        user: UserUnalInput = _get_user_from_row(row_tuple)
        _add_user_to_collections(user, seen, collections)
        type_user: TypeUserInput = __get_type_user_from_row(row_tuple)
        _add_type_user_to_collections(type_user, seen, collections)
        _add_user_type_assoc_to_collections(
            user,
            type_user,
            cod_period,
            seen,
            collections
        )


def _persist_collections(c: Collections, session: Session) -> Dict[str, Any]:
    try:
        resUsers = UserUnalService.bulk_insert_ignore(c.users, session)
        resTypeUser = TypeUserService.bulk_insert_ignore(
            c.user_types,
            session
        )
        resTypeUserUnitAssocs = TypeUserAssociationService.bulk_insert_ignore(
            c.type_user_assocs,
            session
        )

        return {
            "users": resUsers,
            "type_user": resTypeUser,
            "type_user_unit": resTypeUserUnitAssocs
        }

    except Exception as e:
        logger.error(f"Error durante el proceso de inserción: {str(e)}")
        logger.error(f"Detalles del error: {e}")
        raise HTTPException(status_code=500, detail={
            "status": False,
            "message": "Error interno durante la inserción de datos."
        })


def log_persist_results(
        results: Dict[str, Any],
        debug: bool = False
) -> None:
    if not debug:
        return

    logger.info("Inserciones completadas.")
    for k, v in results.items():
        logger.info(f"Resultado {k}: {v}")


def _add_user_to_collections(
    user: UserUnalInput,
    seen: Seen,
    collections: Collections
) -> None:
    if not user.email_unal:
        return

    if not is_unique_entity_in_set(seen.users, user.email_unal):
        return

    seen.users.add(user.email_unal)
    collections.users.append(user)


def _add_type_user_to_collections(
    type_user: TypeUserInput,
    seen: Seen,
    collections: Collections
) -> None:
    if not type_user.name:
        return

    if not is_unique_entity_in_set(
        seen.user_types, type_user.name
    ):
        return

    seen.user_types.add(type_user.name)
    collections.user_types.append(type_user)


def _add_user_type_assoc_to_collections(
    user: UserUnalInput,
    type_user: TypeUserInput,
    cod_period: str,
    seen: Seen,
    collections: Collections
) -> None:
    if not user.email_unal or not type_user.name:
        return

    assoc_key = f"{user.email_unal}{type_user.name}{cod_period}"
    if assoc_key in seen.type_user_assocs:
        return

    seen.type_user_assocs.add(assoc_key)
    collections.type_user_assocs.append(
        TypeUserAssociationInput(
            email_unal=user.email_unal,
            type_user_name=type_user.name,
            cod_period=cod_period
        )
    )


def _get_user_from_row(row: Tuple[Cell, ...]) -> UserUnalInput:

    name = get_value_from_row(
        row, EstudianteInactivos.NOMBRES.value
    ) or None

    apellido1 = get_value_from_row(
        row, EstudianteInactivos.APELLIDO1.value
    ) or None

    apellido2 = get_value_from_row(
        row, EstudianteInactivos.APELLIDO2.value
    ) or None

    return UserUnalInput(
        email_unal=(
            get_value_from_row(row, EstudianteInactivos.EMAIL.value) or None
        ),
        document=None,
        name=name,
        lastname=(
            f"{apellido1} {apellido2}".strip()
        ),
        full_name=(
            f"{name} {apellido1} {apellido2}".strip()
        ),
        gender=None,
        birth_date=None,
        headquarters=get_value_from_row(
            row, EstudianteInactivos.SEDE.value
        )
    )


def _get_clean_name(name: str) -> str:
    cleaned_name = re.sub(r"^\d+\s*-\s*", "", name).strip()
    return cleaned_name


def _get_name_type_user(name: str) -> str:
    cleaned_name = _get_clean_name(name)
    return f"ESTUDIANTE {cleaned_name.upper()} INACTIVO"


def __get_type_user_from_row(row: Tuple[Cell, ...]) -> TypeUserInput:
    tipo_nivel_value = get_value_from_row(
        row, EstudianteInactivos.TIPO_NIVEL.value
    )
    description_value = get_value_from_row(
        row, EstudianteInactivos.BLOQUEO.value
    )

    cargo: str = _get_name_type_user(tipo_nivel_value)
    description: str = description_value

    return TypeUserInput(
        name=cargo,
        description=description
    )


def build_summary(c: Collections) -> Dict[str, Any]:
    return {
        "status": True,
        "cant_users": len(c.users),
        "cant_type_user": len(c.user_types),
        "cant_type_user_assocs": len(c.type_user_assocs)
    }


def get_prefix_sede(sede: str) -> str:
    prefix_sede: str = sede.split(" ")[0][:3].lower()
    if sede == EstInactSedeEnum.SEDE_DE_LA_PAZ.file_name:
        prefix_sede = sede.split(" ")[2][:3].lower()
    elif sede == EstInactSedeEnum.NACIONAL.file_name:
        prefix_sede = sede.split(" ")[1][:3].lower()

    return prefix_sede
