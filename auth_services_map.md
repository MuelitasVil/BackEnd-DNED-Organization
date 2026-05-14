# Mapeo de servicios de autenticacion y autorizacion

## 1) Endpoints de autenticacion (publicos)

- `POST /auth/register`
  - Archivo: `app/controllers/auth_controller.py`
  - DTO entrada: `app/domain/dtos/auth/register_input.py`
  - Servicio: `AuthService.register(...)`
  - Repositorio: `AuthRepository.create_user(...)`
  - Comportamiento actual: crea el usuario en `system_user` con `state = FALSE` (inactivo por defecto).

- `POST /auth/login`
  - Archivo: `app/controllers/auth_controller.py`
  - DTO entrada: `app/domain/dtos/auth/login_input.py`
  - Servicio: `AuthService.login(...)`
  - Repositorio: `AuthRepository.get_user_by_email(...)`, `AuthRepository.create_token(...)`
  - Comportamiento actual:
    - Solo autentica si el usuario existe y esta activo (`state = TRUE`).
    - Valida password con `bcrypt` + `salt`.
    - Genera JWT (`HS256`) y lo persiste en tabla `token`.

## 2) Servicios internos de autenticacion

- `AuthService` (`app/service/crud/auth_service.py`)
  - `register(email, password, session)`
    - Genera `salt`.
    - Hashea `password + salt`.
    - Crea `SystemUser`.
  - `login(email, password, session)`
    - Busca usuario por email.
    - Rechaza usuario inactivo.
    - Verifica hash.
    - Emite JWT con `sub=email` y expiracion.
    - Persiste token emitido.

- `AuthRepository` (`app/repository/auth_repository.py`)
  - `create_user(user)`
  - `get_user_by_email(email)`
  - `create_token(token)`
  - `token_exists(jwt_token)`

## 3) Autorizacion por token (protegido)

- Dependencia: `get_current_user(...)` en `app/utils/auth.py`
  - Extrae `Bearer token`.
  - Decodifica JWT.
  - Verifica que el token exista en tabla `token`.
  - Retorna `sub` (email).

- Wiring en `app/main.py`
  - `auth_controller` se mantiene publico.
  - Todos los demas routers se incluyen con `dependencies=[Depends(get_current_user)]`.

## 4) Persistencia asociada

- Modelo usuario: `app/domain/models/system_user.py`
  - Campo `state: bool = False`.

- SQL schema:
  - `db/create_tables.sql`: `system_user.state DEFAULT FALSE`
  - `db/delete_and_create_tables.sql`: `system_user.state DEFAULT FALSE`

## 5) Regla operativa vigente

- Registro: crea usuarios inactivos.
- Login: solo usuarios activos (activacion temporal via DB).
- Endpoints protegidos: todos excepto `/auth/login` y `/auth/register`.
