from zipfile import BadZipFile

from fastapi import HTTPException
from io import BytesIO
from fastapi import UploadFile
from openpyxl import load_workbook, Workbook
from openpyxl.utils.exceptions import InvalidFileException


async def readExcelFile(file: UploadFile) -> Workbook:
    try:
        if not file.filename or not file.filename.endswith((".xlsx", ".xlsm")):
            raise HTTPException(
                status_code=400,
                detail="El archivo debe ser .xlsx o .xlsm"
            )

        contents = await file.read()
        excel_io = BytesIO(contents)
        wb: Workbook = load_workbook(excel_io)
        return wb

    except HTTPException:
        raise

    except (InvalidFileException, BadZipFile, ValueError):
        raise HTTPException(
            status_code=400,
            detail="El archivo Excel es inválido o está corrupto"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar el archivo: {str(e)}"
        )
