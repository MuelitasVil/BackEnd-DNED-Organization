from openpyxl import Workbook

from app.service.excel_processor.case_docentes_administrativos import (
    _excel_processing,
    Collections,
    Seen,
)


def build_worksheet(rows):
    wb = Workbook()
    ws = wb.active

    ws.append([
        "SEDE",
        "NOMBRES_Y_APELLIDOS",
        "EMAIL",
        "NOMBRE_CARGO",
        "UNIDAD",
        "NOMBRE_VINCULACION",
        "FACULTAD_NOMBRE_ZONA",
    ])

    for row in rows:
        ws.append(row)

    return ws


def build_empty_collections():
    return Collections(
        users=[],
        units=[],
        schools=[],
        headquarters=[],
        user_unit_assocs=[],
        unit_school_assocs=[],
        school_headquarters_assocs=[],
        user_types=[],
        type_user_assocs=[]
    )


def build_empty_seen():
    return Seen(
        users=set(),
        units=set(),
        schools=set(),
        headquarters=set(),
        user_unit_assocs=set(),
        unit_school_assocs=set(),
        school_headquarters_assocs=set(),
        unit_with_school=set(),
        type_user_assocs=set(),
        user_types=set()
    )


def test_excel_processing_un_registro_administrativo():
    rows = [[
        "BOGOTÁ",
        "Juan Pérez",
        "juan.perez@unal.edu.co",
        "PROFESIONAL",
        "DIRECCIÓN NACIONAL DE INFORMÁTICA",
        "ADMINISTRATIVO",
        "FACULTAD DE INGENIERÍA",
    ]]

    ws = build_worksheet(rows)
    collections = build_empty_collections()
    seen = build_empty_seen()
    errors = []

    _excel_processing(ws, collections, seen, "2025-1", errors)

    assert len(collections.users) == 1
    assert len(collections.units) == 1
    assert len(collections.schools) == 1
    assert len(collections.headquarters) == 1
    assert len(collections.user_unit_assocs) == 1
    assert len(collections.unit_school_assocs) == 1
    assert len(collections.school_headquarters_assocs) == 1
    assert len(collections.user_types) == 1
    assert len(collections.type_user_assocs) == 1

    assert collections.users[0].email_unal == "juan.perez@unal.edu.co"
    assert collections.users[0].full_name == "Juan Pérez"
    assert collections.users[0].headquarters == "BOGOTÁ"
    assert collections.user_types[0].name == "PROFESIONAL"


def test_excel_processing_no_duplica_usuario_y_agrega_nuevo_tipo_usuario():
    rows = [
        [
            "BOGOTÁ",
            "Juan Pérez",
            "juan.perez@unal.edu.co",
            "PROFESIONAL",
            "DIRECCIÓN NACIONAL DE INFORMÁTICA",
            "ADMINISTRATIVO",
            "FACULTAD DE INGENIERÍA",
        ],
        [
            "BOGOTÁ",
            "Juan Pérez",
            "juan.perez@unal.edu.co",
            "ASESOR",
            "DIRECCIÓN NACIONAL DE INFORMÁTICA",
            "ADMINISTRATIVO",
            "FACULTAD DE INGENIERÍA",
        ],
    ]

    ws = build_worksheet(rows)
    collections = build_empty_collections()
    seen = build_empty_seen()
    errors = []

    _excel_processing(ws, collections, seen, "2025-1", errors)

    assert len(collections.users) == 1
    assert len(collections.user_types) == 2
    assert len(collections.type_user_assocs) == 2

    assert collections.users[0].email_unal == "juan.perez@unal.edu.co"
    assert {t.name for t in collections.user_types} == {
        "PROFESIONAL",
        "ASESOR",
    }
