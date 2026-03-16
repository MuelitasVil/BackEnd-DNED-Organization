from dataclasses import dataclass
import datetime
from http.client import HTTPException
from typing import Dict, Any, List, Optional, Tuple
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.cell.cell import Cell
from sqlmodel import Session

from app.domain.dtos.user_workspace.user_workspace_input import (
    UserWorkspaceInput
)


from app.domain.enums.files.work_space_enum import (
    WorkSpace
)

from app.domain.models.user_unal import UserUnal

from app.service.excel_processor.utils.error_utils import (
    raise_if_errors
)


from app.service.excel_processor.utils.excel_validator import (
    get_value_from_row,
    is_header_row,
    validate_row_blank_or_incomplete,
)

from app.service.crud.user_unal_service import (
    UserUnalService
)

from app.service.crud.user_workspace_service import (
    UserWorkspaceService
)

from app.utils.app_logger import AppLogger
from app.utils.keyword_not_person import verify_is_person

logger = AppLogger(__file__)
logger2 = AppLogger(__file__, "user_unit_association.log")


@dataclass
class Collections:
    data_work_space: List[UserWorkspaceInput]


def case_administrativos_activos(
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
    all_users: Dict[str, UserUnal] = _get_all_users(session)

    collections = Collections(
        data_work_space=[]
    )

    _excel_processing(
        ws,
        collections,
        cod_period,
        all_users,
        errors,
    )
    results = _persist_collections(collections, session)
    # defult not log persist results.
    log_persist_results(results)
    return build_summary(collections)


def _excel_processing(
    ws: Worksheet,
    collections: Collections,
    cod_period: str,
    all_users: Dict[str, UserUnal],
    errors: List[Dict[str, Any]] = [],
) -> None:
    """
    Función principal para procesar las filas del archivo Excel.
     - rows: Lista de tuplas con el índice de fila y el contenido de la fila.
    """
    logger.info(
        "Iniciando procesamiento de archivo de docentes administrativos"
    )

    for row_idx, row in enumerate(ws.iter_rows(), start=1):

        if is_header_row(row_idx):
            continue

        blank_or_incomplete_errors = validate_row_blank_or_incomplete(
            row,
            row_idx,
            errors,
            WorkSpace
        )

        if blank_or_incomplete_errors:
            errors.extend(blank_or_incomplete_errors)
            continue

        work_space: UserWorkspaceInput = _get_work_space_from_row(
            row,
            cod_period,
            all_users
        )
        collections.data_work_space.append(work_space)

        logger.debug(f"Procesando fila {row_idx}")
        logger.debug(f"Contenido de la fila: {[cell.value for cell in row]}")

    raise_if_errors(errors)


def _get_work_space_from_row(
        row: Tuple[Cell, ...],
        cod_period: str,
        users: Dict[str, UserUnal]
) -> UserWorkspaceInput:
    email = get_value_from_row(row, WorkSpace.EMAIL.value)
    last_connection = get_value_from_row(row, WorkSpace.LAST_SING_IN.value)
    status = get_value_from_row(row, WorkSpace.STATUS.value)
    email_usage = get_value_from_row(row, WorkSpace.EMAIL_USAGE.value)
    storage_used = get_value_from_row(row, WorkSpace.STORAGE_USED.value)
    storage_limit = get_value_from_row(row, WorkSpace.STORAGE_LIMIT.value)
    name = get_value_from_row(row, WorkSpace.FIRST_NAME.value)
    is_user = validate_is_person(name, email, users)
    return UserWorkspaceInput(
        email_unal=(email or None),
        last_connection=_get_date_time(last_connection or None),
        status=(status or None),
        email_usage=_get_float(email_usage or None),
        storage_used=_get_float(storage_used or None),
        storage_limit=_get_float(storage_limit or None),
        is_person=is_user,
        cod_period=cod_period,
    )


def _persist_collections(c: Collections, session: Session) -> Dict[str, Any]:
    try:
        res_user_work_space = UserWorkspaceService.bulk_insert_ignore(
            c.data_work_space, session
        )

        return {
            "users": res_user_work_space
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


def build_summary(c: Collections) -> Dict[str, Any]:
    return {
        "status": True,
        "cant_users": len(c.users),
        "cant_units": len(c.units),
        "cant_schools": len(c.schools),
        "cant_headquarters": len(c.headquarters),
        "cant_user_unit_assocs": len(c.user_unit_assocs),
        "cant_unit_school_assocs": len(c.unit_school_assocs),
        "cant_school_head_assocs": len(c.school_headquarters_assocs),
        "cant_type_user": len(c.user_types),
        "cant_type_user_unit_assocs": len(c.type_user_unit_assocs)
    }


def _get_all_users(session: Session) -> dict[str, UserUnal]:
    all_users = UserUnalService.get_all_no_pagination(session)
    if not all_users or len(all_users) == 0:
        raise HTTPException(status_code=400, detail={
            "status": False,
            "message": "No se encontraron usuarios en la base de datos."
        })
    return {user.email_unal: user for user in all_users}


def _get_date_time(value: str) -> Optional[datetime.datetime]:
    if not value:
        return None

    if isinstance(value, datetime.datetime):
        return value

    if WorkSpace.is_never_logged_in(value):
        return None

    try:
        return datetime.datetime.strptime(
            str(value), "%Y/%m/%d %H:%M:%S"
        )
    except (ValueError, TypeError):
        return None


def _get_float(value: str) -> Optional[float]:
    if not value:
        return None
    value = value.replace(',', '.').replace('GB', '')
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def validate_is_person(
        name: str,
        email: str,
        users: Dict[str, UserUnal]
) -> bool:
    if not name:
        return False
    if email in users:
        return True
    return verify_is_person(name)
