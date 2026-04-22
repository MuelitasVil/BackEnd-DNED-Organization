from openpyxl import Workbook
from app.service.excel_processor.case_estudiantes_activos import (
    _excel_processing,
    Collections,
    Seen,
    log_collections
)


def build_sorted_rows(rows):
    wb = Workbook()
    ws = wb.active

    ws.append([
        "NOMBRES_APELLIDOS",
        "EMAIL",
        "SEDE",
        "FACULTAD",
        "COD_PLAN",
        "PLAN",
        "TIPO_NIVEL",
    ])

    for row in rows:
        ws.append(row)

    return [
        (idx, row) for idx, row in enumerate(ws.iter_rows(min_row=2), start=2)
    ]


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
        user_types=set(),
        type_user_assocs=set(),
        primary_unit_by_base={}
    )


def test_excel_processing_un_registro():
    rows = [[
        "Lina Sofia Espinal Daza",
        "lespinal@unal.edu.co",
        "SEDE BOGOTÁ",
        "FACULTAD DE INGENIERÍA",
        "2A74",
        "INGENIERÍA DE SISTEMAS Y COMPUTACIÓN",
        "PREGRADO",
    ]]

    sorted_rows = build_sorted_rows(rows)
    collections = build_empty_collections()
    seen = build_empty_seen()
    errors = []

    _excel_processing(sorted_rows, collections, seen, "2025-1", errors)

    assert len(collections.users) == 1
    assert len(collections.units) == 1
    assert len(collections.schools) == 1


def test_excel_processing_no_duplica_unidad_assoc_school():
    rows = [
        ["A", "a@unal.edu.co", "SEDE BOGOTÁ", "FACULTAD", "2A74", "PLAN", "PREGRADO"],  # noqa: E501
        ["B", "b@unal.edu.co", "SEDE ORINOQUÍA", "SEDE ORINOQUIA", "2A74", "PLAN", "PREGRADO"],  # noqa: E501
    ]

    sorted_rows = build_sorted_rows(rows)
    collections = build_empty_collections()
    seen = build_empty_seen()
    errors = []

    _excel_processing(sorted_rows, collections, seen, "2025-1", errors)
    log_collections(collections)

    assert (
        len(collections.unit_school_assocs) == 1 and
        len(collections.units) == 1
    )


def test_excel_processing_no_duplica_usuario():
    rows = [
        ["A", "a@unal.edu.co", "SEDE BOGOTÁ", "FACULTAD", "2A74", "PLAN", "PREGRADO"],  # noqa: E501
        ["A", "a@unal.edu.co", "SEDE BOGOTÁ", "FACULTAD", "2A74", "PLAN", "PREGRADO"],  # noqa: E501
    ]

    sorted_rows = build_sorted_rows(rows)
    collections = build_empty_collections()
    seen = build_empty_seen()
    errors = []

    _excel_processing(sorted_rows, collections, seen, "2025-1", errors)

    assert len(collections.users) == 1
