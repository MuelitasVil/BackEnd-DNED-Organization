from openpyxl import Workbook

from app.domain.models.user_unal import UserUnal
import app.service.excel_processor.case_work_space as case_ws
from app.service.excel_processor.case_work_space import (
    Collections,
    _excel_processing,
    validate_is_person,
)


def build_workspace_sheet(rows):
    wb = Workbook()
    ws = wb.active
    ws.append([
        "FIRST_NAME",
        "LAST_NAME",
        "EMAIL",
        "STATUS",
        "LAST_SING_IN",
        "EMAIL_USAGE",
        "STORAGE_USED",
        "STORAGE_LIMIT",
    ])
    for row in rows:
        ws.append(row)
    return ws


def test_validate_is_person_false_if_name_is_empty():
    users = {"ana@unal.edu.co": UserUnal(email_unal="ana@unal.edu.co")}

    result = validate_is_person("", "ana@unal.edu.co", users)

    assert result is False


def test_validate_is_person_false_if_email_not_in_users():
    users = {"ana@unal.edu.co": UserUnal(email_unal="ana@unal.edu.co")}

    result = validate_is_person(
        "Ana Maria",
        "otro@unal.edu.co",
        users,
    )

    assert result is False


def test_validate_is_person_uses_verify_is_person_when_email_exists(
    monkeypatch,
):
    users = {"ana@unal.edu.co": UserUnal(email_unal="ana@unal.edu.co")}

    monkeypatch.setattr(case_ws, "verify_is_person", lambda name: True)
    assert validate_is_person("Ana Maria", "ana@unal.edu.co", users) is True

    monkeypatch.setattr(case_ws, "verify_is_person", lambda name: False)
    assert validate_is_person("Ana Maria", "ana@unal.edu.co", users) is False


def test_excel_processing_sets_is_person_from_validation(monkeypatch):
    ws = build_workspace_sheet([
        [
            "Ana",
            "Ruiz",
            "ana@unal.edu.co",
            "Active",
            "Never logged in",
            "0.0GB",
            "0.0GB",
            "15.0GB",
        ]
    ])
    collections = Collections(data_work_space=[])
    errors = []
    all_users = {"ana@unal.edu.co": UserUnal(email_unal="ana@unal.edu.co")}

    monkeypatch.setattr(case_ws, "verify_is_person", lambda name: True)

    _excel_processing(
        ws=ws,
        collections=collections,
        cod_period="2025-1",
        all_users=all_users,
        active_users_period={"ana@unal.edu.co"},
        errors=errors,
    )

    assert len(collections.data_work_space) == 1
    assert collections.data_work_space[0].email_unal == "ana@unal.edu.co"
    assert collections.data_work_space[0].is_person is True
