from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from sqlalchemy.orm import Session

from app.domain.enums.files.estudiante_activos_enum import EstudianteActivos
from app.domain.enums.files.funcionarios_activos_enum import (
    FuncionariosActivos
)

from app.service.excel_processor.case_estudiantes_activos import (
    case_estudiantes_activos
)

from app.service.excel_processor.case_docentes_administrativos import (
    case_administrativos_activos
)

from app.exceptions.excel_exceptions import InvalidExcelStructureError


def process_file(file: Workbook, cod_period: str, session: Session):
    ws: Worksheet = file[file.sheetnames[0]]
    headers = get_headers(ws)

    if not headers:
        raise InvalidExcelStructureError(ws.title, [])

    if EstudianteActivos.validate_headers(headers):
        return case_estudiantes_activos(ws, cod_period, session)

    if FuncionariosActivos.validate_headers(headers):
        return case_administrativos_activos(ws, cod_period, session)

    raise InvalidExcelStructureError(ws.title, headers)


def get_headers(ws: Worksheet) -> list[str]:
    return [
        str(cell.value).strip()
        for cell in ws[1]
        if cell.value is not None and str(cell.value).strip() != ""
    ]
