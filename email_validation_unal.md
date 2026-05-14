# Validación de emails @unal.edu.co

## Descripción

El sistema ahora valida que los usuarios se registren **solo con correos @unal.edu.co** y que el correo sea válido, evitando registros falsos o inexistentes.

## Flujo de validación en registro

1. **Validación de dominio**
   - Solo acepta emails terminados en `@unal.edu.co`
   - Ejemplo válido: `student@unal.edu.co`, `professor.name@unal.edu.co`
   - Ejemplo inválido: `user@gmail.com`, `user@unal.com`

2. **Validación en Google** (estructura lista para implementación futura)
   - Actualmente valida formato
   - Futuro: Confirmar que el email existe en Google/Gmail mediante Admin Directory API

3. **Validación de duplicado**
   - Rechaza si el email ya está registrado en la BD

## Archivos modificados

### Nuevos

- **[app/utils/google_email_validator.py](app/utils/google_email_validator.py)**
  - `GoogleEmailValidator.validate_unal_email_format(email)` → Valida dominio @unal.edu.co
  - `GoogleEmailValidator.validate_email_exists_in_google(email)` → Valida existencia en Google (hoy: solo formato)
  - `GoogleEmailValidator.validate_and_raise(email)` → Levanta excepción si es inválido

- **[app/exceptions/auth_exceptions.py](app/exceptions/auth_exceptions.py)**
  - `InvalidEmailException` → Para emails con dominio incorrecto o inválidos
  - `EmailAlreadyRegisteredException` → Para emails ya registrados

### Actualizados

- **[app/service/crud/auth_service.py](app/service/crud/auth_service.py)**
  - `AuthService.register()` ahora valida el email antes de crear usuario
  - Lanza excepciones si el email no es válido o duplicado

- **[app/controllers/auth_controller.py](app/controllers/auth_controller.py)**
  - Maneja excepciones de validación email
  - Devuelve HTTP 400 para dominio incorrecto
  - Devuelve HTTP 409 para email duplicado

### Tests

- **[app/test/auth/test_google_email_validator.py](app/test/auth/test_google_email_validator.py)**
  - Tests de formato válido/inválido de @unal.edu.co

- **[app/test/auth/test_auth_service.py](app/test/auth/test_auth_service.py)**
  - Tests de rechazo de no-UNAL emails
  - Tests de rechazo de emails duplicados

- **[app/test/auth/test_auth_controller.py](app/test/auth/test_auth_controller.py)**
  - Tests de HTTP 400 para dominio inválido
  - Tests de HTTP 409 para duplicado

## Respuestas HTTP

### Registro con email válido
```
POST /auth/register
{
  "email": "student@unal.edu.co",
  "password": "secret123"
}

Response 200:
{
  "message": "User registered",
  "email": "student@unal.edu.co"
}
```

### Registro con email fuera de @unal.edu.co
```
POST /auth/register
{
  "email": "user@gmail.com",
  "password": "secret123"
}

Response 400:
{
  "detail": "Email must be from @unal.edu.co domain"
}
```

### Registro con email duplicado
```
POST /auth/register
{
  "email": "student@unal.edu.co",
  "password": "secret123"
}

Response 409:
{
  "detail": "Email student@unal.edu.co is already registered"
}
```

## Próximos pasos para producción

Para habilitar validación real en Google:

1. Crear Service Account en Google Cloud Console
2. Otorgar permisos de Directory API
3. Guardar credencial JSON en variable de entorno: `GOOGLE_ADMIN_CREDENTIALS`
4. Reemplazar el `TODO` en [app/utils/google_email_validator.py](app/utils/google_email_validator.py) con implementación que use `service_account.Credentials`
5. Llamar a `/admin/directory/v1/users/{email}` para verificar existencia

Ver: https://developers.google.com/admin-sdk/directory/reference/rest/v1/users/get
