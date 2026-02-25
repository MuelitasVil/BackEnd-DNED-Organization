from dataclasses import dataclass
from http.client import HTTPException
from typing import Dict, Any, List, Tuple, Set
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.cell.cell import Cell
from sqlmodel import Session

from app.domain.dtos.school_headquarters_associate.school_headquarters_associate_input import (  # noqa: E501 ignora error flake8
    SchoolHeadquartersAssociateInput,
)

from app.domain.dtos.type_user.type_user_input import (
    TypeUserInput
)

from app.domain.dtos.type_user_association.type_user_association_input import (
    TypeUserAssociationInput
)

from app.domain.dtos.unit_school_associate.unit_school_associate_input import (
    UnitSchoolAssociateInput,
)

from app.domain.dtos.user_unit_associate.user_unit_associate_input import (
    UserUnitAssociateInput,
)

from app.service.crud.school_headquarters_associate_service import (
    SchoolHeadquartersAssociateService
)

from app.service.crud.type_user_association_service import (
    TypeUserAssociationService
)

from app.service.crud.type_user_service import (
    TypeUserService
)

from app.service.crud.unit_school_associate_service import (
    UnitSchoolAssociateService
)

from app.service.crud.user_unit_associate_service import (
    UserUnitAssociateService,
)

from app.service.excel_processor.utils.collection_utils import (
    is_unique_entity_in_set
)

from app.service.excel_processor.utils.error_utils import (
    add_invalid_headquarters_error,
    rails_if_errors
)


from app.service.excel_processor.utils.excel_validator import (
    get_value_from_row,
    is_header_row,
    validate_row_blank_or_incomplete,
)


from app.domain.dtos.user_unal.user_unal_input import UserUnalInput
from app.domain.dtos.unit_unal.unit_unal_input import UnitUnalInput
from app.domain.dtos.school.school_input import SchoolInput
from app.domain.dtos.headquarters.headquarters_input import HeadquartersInput

from app.domain.enums.files.general import General_Values
from app.domain.enums.files.estudiante_activos import (
    EstudianteActivos,
    EstActSedeEnum
)

from app.service.crud.user_unal_service import UserUnalService
from app.service.crud.unit_unal_service import UnitUnalService
from app.service.crud.school_service import SchoolService
from app.service.crud.headquarters_service import HeadquartersService

from app.utils.app_logger import AppLogger

logger = AppLogger(__file__)
logger2 = AppLogger(__file__, "user_unit_association.log")


@dataclass
class Collections:
    users: List[UserUnalInput]
    units: List[UnitUnalInput]
    schools: List[SchoolInput]
    headquarters: List[HeadquartersInput]
    user_unit_assocs: List[UserUnitAssociateInput]
    unit_school_assocs: List[UnitSchoolAssociateInput]
    school_headquarters_assocs: List[SchoolHeadquartersAssociateInput]
    user_types: List[TypeUserInput]
    type_user_unit_assocs: List[TypeUserAssociationInput]


@dataclass
class Seen:
    users: Set[str]
    units: Set[str]
    schools: Set[str]
    headquarters: Set[str]
    user_unit_assocs: Set[str]
    unit_school_assocs: Set[str]
    school_headquarters_assocs: Set[str]
    unit_with_school: Set[str]
    type_user_assocs: Set[str]
    type_user_unit_assocs: Set[str]


def case_estudiantes_activos(
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
        units=[],
        schools=[],
        headquarters=[],
        user_unit_assocs=[],
        unit_school_assocs=[],
        school_headquarters_assocs=[],
        user_types=[],
        type_user_unit_assocs=[]
    )

    seen = Seen(
        users=set(),
        units=set(),
        schools=set(),
        headquarters=set(),
        user_unit_assocs=set(),
        unit_school_assocs=set(),
        school_headquarters_assocs=set(),
        unit_with_school=set(),
        type_user_unit_assocs=set(),
        user_types=set()
    )

    sorted_rows = _sort_rows_by_sede(ws, errors)
    _excel_processing(
        sorted_rows,
        collections,
        seen,
        cod_period,
        errors,
    )
    results = _persist_collections(collections, session)
    # defult not log persist results.
    log_persist_results(results)
    return build_summary(collections)


def _persist_collections(c: Collections, session: Session) -> Dict[str, Any]:
    try:
        resUsers = UserUnalService.bulk_insert_ignore(c.users, session)
        resUnits = UnitUnalService.bulk_insert_ignore(c.units, session)
        resSchools = SchoolService.bulk_insert_ignore(c.schools, session)
        resHeadquarters = HeadquartersService.bulk_insert_ignore(
            c.headquarters,
            session
        )
        resUserUnitAssocs = UserUnitAssociateService.bulk_insert_ignore(
            c.user_unit_assocs,
            session
        )
        resUnitSchoolAssocs = UnitSchoolAssociateService.bulk_insert_ignore(
            c.unit_school_assocs,
            session
        )
        resSchoolHeadquartersAssocs = SchoolHeadquartersAssociateService.bulk_insert_ignore(  # noqa: E501 ignora error flake8
            c.school_headquarters_assocs,
            session
        )
        resTypeUser = TypeUserService.bulk_insert_ignore(
            c.user_types,
            session
        )
        resTypeUserUnitAssocs = TypeUserAssociationService.bulk_insert_ignore(
            c.type_user_unit_assocs,
            session
        )

        return {
            "users": resUsers,
            "units": resUnits,
            "schools": resSchools,
            "headquarters": resHeadquarters,
            "user_unit": resUserUnitAssocs,
            "unit_school": resUnitSchoolAssocs,
            "school_headquarters": resSchoolHeadquartersAssocs,
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


def _excel_processing(
    sorted_rows: List[Tuple[int, Tuple[Cell, ...]]],
    collections: Collections,
    seen: Seen,
    cod_period: str,
    errors: List[Dict[str, Any]] = [],
) -> None:
    """
    Función principal para procesar las filas del archivo Excel.
     - rows: Lista de tuplas con el índice de fila y el contenido de la fila.
    """
    logger.info("Iniciando procesamiento de archivo de estudiantes activos")
    for row_idx, row in sorted_rows:
        isSpecialHeadquarters: bool = False
        logger.debug(f"Procesando fila {row_idx}")
        logger.debug(f"Contenido de la fila: {[cell.value for cell in row]}")

        row_tuple: Tuple[Cell, ...] = row
        user: UserUnalInput = _get_user_from_row(row_tuple)
        _add_user_to_collections(user, seen, collections)

        type_user: TypeUserInput = __get_type_user_from_row(row_tuple)
        _add_type_user_to_collections(type_user, seen, collections)

        unit: UnitUnalInput = _get_unit_from_row(row_tuple)
        _add_unit_to_collections(unit, seen, collections)

        school: SchoolInput
        school, isSpecialHeadquarters = _get_school_from_row(row_tuple)
        _add_school_to_collections(school, seen, collections)

        head: HeadquartersInput = _get_headquarters_from_row(row_tuple)
        _add_headquarters_to_collections(head, seen, collections)

        _add_user_unit_assoc_to_collections(
            user,
            unit,
            cod_period,
            seen,
            collections
        )

        _add_unit_school_assoc_to_collections(
            unit,
            school,
            cod_period,
            seen,
            collections,
            isSpecialHeadquarters
        )

        _add_school_headquarters_to_collections(
            school,
            head,
            cod_period,
            seen,
            collections
        )

        _add_user_type_assoc_to_collections(
            user,
            type_user,
            cod_period,
            seen,
            collections
        )


def _add_user_to_collections(
    user: UserUnalInput,
    seen: Seen,
    collections: Collections
) -> None:
    if not user.email_unal:
        return

    if not is_unique_entity_in_set(seen.users(), user.email_unal):
        return

    seen.users.add(user.email_unal)
    collections.users.append(user)


def _add_unit_to_collections(
    unit: UnitUnalInput,
    seen: Seen,
    collections: Collections
) -> None:
    if not unit.cod_unit:
        return

    if not is_unique_entity_in_set(seen.units(), unit.cod_unit):
        return

    seen.units.add(unit.cod_unit)
    collections.units.append(unit)


def _add_school_to_collections(
    school: SchoolInput,
    seen: Seen,
    collections: Collections
) -> None:
    if not school.cod_school:
        return

    if not is_unique_entity_in_set(seen.schools(), school.cod_school):
        return

    seen.schools.add(school.cod_school)
    collections.schools.append(school)


def _add_headquarters_to_collections(
    head: HeadquartersInput,
    seen: Seen,
    collections: Collections
) -> None:
    if not head.cod_headquarters:
        return

    if not is_unique_entity_in_set(
        seen.headquarters(), head.cod_headquarters
    ):
        return

    seen.headquarters.add(head.cod_headquarters)
    collections.headquarters.append(head)


def _add_user_unit_assoc_to_collections(
    user: UserUnalInput,
    unit: UnitUnalInput,
    cod_period: str,
    seen: Seen,
    collections: Collections
) -> None:
    if not user.email_unal or not unit.cod_unit:
        return

    assoc_key = f"{user.email_unal}{unit.cod_unit}{cod_period}"
    if assoc_key in seen.user_unit_assocs:
        return

    logger.info(
        f"Agregando asociación de usuario a plan: "
        f"{user.email_unal} -> {unit.cod_unit} para periodo {cod_period}"
    )

    seen.user_unit_assocs.add(assoc_key)
    collections.user_unit_assocs.append(
        UserUnitAssociateInput(
            email_unal=user.email_unal,
            cod_unit=unit.cod_unit,
            cod_period=cod_period
        )
    )


def _add_unit_school_assoc_to_collections(
    unit: UnitUnalInput,
    school: SchoolInput,
    cod_period: str,
    seen: Seen,
    collections: Collections,
    isSpecialHeadquarters: bool
) -> None:
    """
    Importante: Los estudiantes de las sedes de presencia nacional
    sus facultades perteneces a sedes mas grades es decir:
    - Sede Bogotá
    - Sede Medellín
    - Sede Manizales
    etc.

    Por lo tanto, si detectamos que una sede es de presencia nacional,
    no agregamos la asociación del plan a la facultad para evitar duplicados
    en la tabla de asociación plan-facultad, ya que estos planes estarán
    asociados a la sede más grande.
    """

    if not school.cod_school or not unit.cod_unit:
        return

    if isSpecialHeadquarters:
        logger.debug(
            "Sede de presencia nacional detectada"
        )

    if isSpecialHeadquarters and unit.cod_unit in seen.unit_with_school:
        logger.debug(
            f"El plan {unit.cod_unit} esta asociado a una sede mas grande"
            f"de sede {school.cod_school}, por lo que no se agregará la "
            f"asociación a colecciones para evitar duplicados."
        )
        return

    assoc_key = f"{unit.cod_unit}{school.cod_school}{cod_period}"
    if assoc_key in seen.unit_school_assocs:
        return

    seen.unit_school_assocs.add(assoc_key)
    collections.unit_school_assocs.append(
        UnitSchoolAssociateInput(
            cod_unit=unit.cod_unit,
            cod_school=school.cod_school,
            cod_period=cod_period
        )
    )


def _add_school_headquarters_to_collections(
    school: SchoolInput,
    headquarters: HeadquartersInput,
    cod_period: str,
    seen: Seen,
    collections: Collections
) -> None:
    if not school.cod_school or not headquarters.cod_headquarters:
        return

    assoc_key = (
        f"{school.cod_school}{headquarters.cod_headquarters}{cod_period}"
    )

    if assoc_key in seen.school_headquarters_assocs:
        return

    seen.school_headquarters_assocs.add(assoc_key)
    collections.school_headquarters_assocs.append(
        SchoolHeadquartersAssociateInput(
            cod_school=school.cod_school,
            cod_headquarters=headquarters.cod_headquarters,
            cod_period=cod_period
        )
    )


def _add_type_user_to_collections(
    type_user: TypeUserInput,
    seen: Seen,
    collections: Collections
) -> None:
    if not type_user.name:
        return

    if not is_unique_entity_in_set(
        seen.type_user_assocs, type_user.name
    ):
        return

    seen.type_user_assocs.add(type_user.name)
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
    if assoc_key in seen.type_user_unit_assocs:
        return

    seen.type_user_unit_assocs.add(assoc_key)
    collections.type_user_unit_assocs.append(
        TypeUserAssociationInput(
            email_unal=user.email_unal,
            type_user_id=type_user.name,
            cod_period=cod_period
        )
    )


def _get_user_from_row(row: Tuple[Cell, ...]) -> UserUnalInput:
    return UserUnalInput(
        email_unal=(
            get_value_from_row(row, EstudianteActivos.EMAIL.value) or None
        ),
        document=None,
        name=None,
        lastname=None,
        full_name=(
            get_value_from_row(
                row, EstudianteActivos.NOMBRES_APELLIDOS.value
            ) or None
        ),
        gender=None,
        birth_date=None,
        headquarters=get_value_from_row(
            row, EstudianteActivos.SEDE.value
        )
    )


def _get_unit_from_row(row: Tuple[Cell, ...]) -> UnitUnalInput:
    sede: str = get_value_from_row(row, EstudianteActivos.SEDE.value)
    tipoEstudiante: str = get_value_from_row(
        row, EstudianteActivos.TIPO_NIVEL.value
    )

    if tipoEstudiante == General_Values.PREGRADO.value:
        tipoEstudiante = "pre"
    elif tipoEstudiante == General_Values.POSGRADO.value:
        tipoEstudiante = "pos"

    prefix_sede: str = sede.split(" ")[1][:3].lower()
    if sede == EstActSedeEnum.SEDE_DE_LA_PAZ._name:
        prefix_sede = sede.split(" ")[3][:3].lower()

    cod_unit: str = get_value_from_row(row, EstudianteActivos.COD_PLAN.value)
    plan: str = get_value_from_row(row, EstudianteActivos.PLAN.value)
    tipo_nivel: str = get_value_from_row(
        row, EstudianteActivos.TIPO_NIVEL.value
    )
    cod_unit = f"{cod_unit}_{tipoEstudiante}_{prefix_sede}"
    email: str = f"{cod_unit}@unal.edu.co"
    return UnitUnalInput(
        cod_unit=cod_unit,
        email=email,
        name=plan or None,
        description=None,
        type_unit=tipo_nivel or None,
    )


def _get_school_from_row(
    row: Tuple[Cell, ...]
) -> Tuple[SchoolInput, bool]:
    isSpecialHeadquarters: bool = False
    facultad: str = get_value_from_row(row, EstudianteActivos.FACULTAD.value)
    sede: str = get_value_from_row(row, EstudianteActivos.SEDE.value)
    tipoEstudiante: str = get_value_from_row(
        row, EstudianteActivos.TIPO_NIVEL.value
    )
    prefix_sede: str = sede.split(" ")[1][:3].lower()

    logger.debug(f"Facultad: {facultad}, Sede: {sede}, Tipo: {tipoEstudiante}")

    if tipoEstudiante == General_Values.PREGRADO.value:
        logger.debug("Tipo de estudiante es pregrado")
        tipoEstudiante = "pre"
    elif tipoEstudiante == General_Values.POSGRADO.value:
        logger.debug("Tipo de estudiante es posgrado")
        tipoEstudiante = "pos"

    cod_school: str = ""

    if EstActSedeEnum.is_special_sede(sede):
        isSpecialHeadquarters = True
        cod_school = f"estf{tipoEstudiante}{prefix_sede}"
    else:
        acronimo = "".join(
            p[0].lower() for p in facultad.split() if len(p) > 2
        )
        cod_school = f"est{acronimo}{tipoEstudiante}_{prefix_sede}"

    email: str = f"{cod_school}@unal.edu.co"

    return SchoolInput(
        cod_school=cod_school,
        email=email,
        name=facultad or None,
        description=None,
        type_facultad=None,
    ), isSpecialHeadquarters


def _get_headquarters_from_row(row: Tuple[Cell, ...]) -> HeadquartersInput:
    sede: str = get_value_from_row(row, EstudianteActivos.SEDE.value)
    tipoEstudiante: str = get_value_from_row(
        row, EstudianteActivos.TIPO_NIVEL.value
    )

    if tipoEstudiante == General_Values.PREGRADO.value:
        tipoEstudiante = "pre"
    elif tipoEstudiante == General_Values.POSGRADO.value:
        tipoEstudiante = "pos"

    prefix_sede: str = sede.split(" ")[1][:3].lower()
    if sede == EstActSedeEnum.SEDE_DE_LA_PAZ._name:
        prefix_sede = sede.split(" ")[3][:3].lower()

    cod_sede: str = f"estudiante{tipoEstudiante}_{prefix_sede}"
    type_facultad: str = f"estudiante_{prefix_sede}"

    email: str = f"{cod_sede}@unal.edu.co"

    return HeadquartersInput(
        cod_headquarters=cod_sede,
        email=email,
        name=sede,
        description=None,
        type_facultad=type_facultad,
    )


def __get_type_user_from_row(row: Tuple[Cell, ...]) -> TypeUserInput:
    tipoEstudiante: str = get_value_from_row(
        row, EstudianteActivos.TIPO_NIVEL.value
    )

    if tipoEstudiante == General_Values.PREGRADO.value:
        tipoEstudiante = "pregrado"
    elif tipoEstudiante == General_Values.POSGRADO.value:
        tipoEstudiante = "posgrado"

    name: str = f"Estudiante {tipoEstudiante.capitalize()}"

    return TypeUserInput(
        name=name,
        description=None
    )


def _sort_rows_by_sede(
    ws: Worksheet,
    errors: List[Dict[str, Any]]
) -> List[Tuple[int, Tuple[Cell, ...]]]:
    """
    Organiza las filas del archivo Excel según la sede
    {
    1: [
        (2, ('SEDE BOGOTÁ', 'ejemplo@bogota.com', 'Juan Pérez')),
        (4, ('SEDE BOGOTÁ', 'ejemplo2@bogota.com', 'Luis García'))
    ],
    2: [
        (3, ('SEDE MANIZALES', 'ejemplo@manizales.com', 'Ana Gómez'))
    ],
    3: [
        (5, ('SEDE MEDELLÍN', 'ejemplo@medellin.com', 'María López'))
    ]
    }

    :param ws: Worksheet del archivo de Excel.
    :param errors: Lista de errores donde se agregarán los errores encontrados.
    :return: Lista de filas organizadas por sede.
    """

    sort_sede_dict: Dict[int, List[Tuple[int, Tuple[Cell, ...]]]] = {
        order.number: [] for order in EstActSedeEnum
    }

    logger.info(
        "Start sort excel rows by headquarters"
    )

    for row_idx, row in enumerate(ws.iter_rows(), start=1):

        if is_header_row(row_idx):
            continue

        blank_or_incomplete_errors = validate_row_blank_or_incomplete(
            row,
            row_idx,
            errors,
            EstudianteActivos
        )

        if blank_or_incomplete_errors:
            errors.extend(blank_or_incomplete_errors)
            continue

        sede = get_value_from_row(row, EstudianteActivos.SEDE.value)
        info_sede = EstActSedeEnum.get_by_name(sede)
        if info_sede is None:
            add_invalid_headquarters_error(
                errors,
                row_idx,
                EstudianteActivos.SEDE.value,
                sede
            )
            continue

        sede_order = info_sede.number
        sort_sede_dict[sede_order].append((row_idx, row))

    sorted_rows = get_sort_rows_by_dict_sede(sort_sede_dict)
    logger.info("Finalizando organizacion de archivo de estudiantes activos")
    rails_if_errors(errors)
    return sorted_rows


def get_sort_rows_by_dict_sede(
    sort_sede_dict: Dict[int, List[Tuple[int, Tuple[Cell, ...]]]]
) -> List[Tuple[int, Tuple[Cell, ...]]]:
    """
    Ordenar las filas según el valor de SedeOrder (de menor a mayor)
    Docstring for get_sort_rows_by_dict_sede

    :param sort_sede_dict: Description
    :type sort_sede_dict: Dict[int, List[Tuple[int, Tuple[Cell, ...]]]]
    :return: Description
    :rtype: List[Tuple[int, Tuple[Cell, ...]]]
    """
    sorted_rows = []
    for order in sorted(sort_sede_dict.keys()):
        sorted_rows.extend(sort_sede_dict[order])


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
    }
