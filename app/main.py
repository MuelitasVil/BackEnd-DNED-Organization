from fastapi.responses import JSONResponse
from fastapi import Depends

from app.exceptions.base_exceptions import (
    AppError
)

from .controllers import (
    period_controller,
    unit_school_associate_controller,
    user_workspace_controller,
    auth_controller,
    user_unal_controller,
    unit_unal_controller,
    user_unit_associate_controller,
    school_controller,
    headquarters_controller,
    school_headquarters_associate_controller,
    type_user_controller,
    type_user_association_controller,
    email_sender_controller,
    email_sender_unit_controller,
    email_sender_school_controller,
    email_sender_headquarters_controller,
    upload_controller,
    workspace_job_controller,
)

from fastapi import FastAPI, Request
from app.utils.validate_token import get_current_user

app = FastAPI()

protected_dependencies = [Depends(get_current_user)]


@app.get("/")
def read_root(_current_user: str = Depends(get_current_user)):
    print("Hello World Endpoint Called")
    return {"Hello": "World"}


app.include_router(auth_controller.router)
app.include_router(
    upload_controller.router,
    dependencies=protected_dependencies
)
app.include_router(
    period_controller.router,
    dependencies=protected_dependencies
)
app.include_router(
    user_workspace_controller.router,
    dependencies=protected_dependencies
)
app.include_router(
    user_unal_controller.router,
    dependencies=protected_dependencies
)
app.include_router(
    unit_unal_controller.router,
    dependencies=protected_dependencies
)
app.include_router(
    user_unit_associate_controller.router,
    dependencies=protected_dependencies
)
app.include_router(
    school_controller.router,
    dependencies=protected_dependencies
)
app.include_router(
    unit_school_associate_controller.router,
    dependencies=protected_dependencies
)
app.include_router(
    headquarters_controller.router,
    dependencies=protected_dependencies
)
app.include_router(
    school_headquarters_associate_controller.router,
    dependencies=protected_dependencies
)
app.include_router(
    type_user_controller.router,
    dependencies=protected_dependencies
)
app.include_router(
    type_user_association_controller.router,
    dependencies=protected_dependencies
)
app.include_router(
    email_sender_controller.router,
    dependencies=protected_dependencies
)
app.include_router(
    email_sender_unit_controller.router,
    dependencies=protected_dependencies
)
app.include_router(
    email_sender_school_controller.router,
    dependencies=protected_dependencies
)
app.include_router(
    email_sender_headquarters_controller.router,
    dependencies=protected_dependencies
)
app.include_router(
    workspace_job_controller.router,
    dependencies=protected_dependencies
)


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.code,
            "message": exc.message,
            "details": exc.extra
        }
    )
