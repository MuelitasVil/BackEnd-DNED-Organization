# DNED Backend

Este proyecto es una API desarrollada en **FastAPI** con persistencia de datos en **MySQL**, orientada a proporcionar servicios backend para un sistema modular. Su diseño sigue una arquitectura basada en capas, que facilita la escalabilidad y el mantenimiento del código.

---

## Tecnologías utilizadas

- **FastAPI**: Framework moderno y rápido para construir APIs con Python 3.7+ basado en *type hints*.
- **MySQL**: Sistema de gestión de bases de datos relacional utilizado como almacenamiento persistente.
- **Uvicorn**: Servidor ASGI utilizado para ejecutar la aplicación FastAPI.
- **Docker (opcional)**: Para levantar el entorno completo con contenedores de forma sencilla.
- **JWT (JSON Web Tokens)**: Mecanismo para autenticación segura basada en tokens.
- **Flake8**: Herramienta de análisis estático de código que garantiza el cumplimiento de la guía de estilo PEP8.

---

## Requisitos

- requires-python = ">=3.13,<3.14"
- MySQL 8.0 o superior (si se ejecuta en local)
- PowerShell o terminal compatible para entornos virtuales

---
## Testing
Para ejecutar las pruebas unitarias del sistema ejecutar : 
   ```bash
   pytest
   ```
---

## Configuración local (ambiente virtual)

> Nota: Ingresar a la carpeta `app`.

1. **Crear el entorno virtual**

   ```bash
   python -m venv .venv
   ```

2. **Activar el entorno virtual**

   En PowerShell (Windows):

   ```bash
   .venv\Scripts\Activate.ps1
   ```

   En Linux/macOS:

   ```bash
   source .venv/bin/activate
   ```

3. **Instalar los requerimientos**

   ```bash
   pip install -r requirements.txt
   ```

4. **(Opcional) Crear o actualizar archivo de requerimientos**

   ```bash
   pip freeze > requirements.txt
   ```

5. **Levantar el sistema en local**

   ```bash
   fastapi dev main.py 
   ```

---

## 🐳 Uso con Docker

1. **Levantar el entorno completo**

   ```bash
   docker compose up --build
   ```

2. Acceder a la API:  
   [http://localhost:8000](http://localhost:8000)

3. Documentación Swagger:  
   [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔐 Autenticación

El sistema implementa autenticación mediante **JWT (JSON Web Tokens)**. Al iniciar sesión mediante el endpoint `/auth/login`, se emite un token firmado que debe incluirse en las cabeceras de autorización de cada petición protegida:

```http
Authorization: Bearer <tu_token>
```

---

## 🧱 Arquitectura del proyecto

El proyecto sigue una arquitectura en capas:

```
/app
├── configuration/     # Configuración del entorno y base de datos
├── controllers/       # Endpoints de la API (FastAPI routers)
├── domain/            # Modelos y estructuras de datos (DTOs, entidades)
├── repository/        # Acceso y lógica de persistencia de datos
├── service/           # Reglas de negocio y procesamiento principal
├── utils/             # Utilidades generales como autenticación
├── main.py            # Punto de entrada de la aplicación
└── requirements.txt   # Dependencias del proyecto
```

Este enfoque modular facilita el mantenimiento, testing y escalabilidad del sistema.

---

## 🧪 Calidad de código

El proyecto utiliza `flake8` como herramienta para asegurar el cumplimiento del estándar de estilo **PEP8**. Para ejecutarlo:

```bash
flake8 .
```

---

## 📦 Dependencias destacadas

```text
fastapi==0.115.14
uvicorn==0.35.0
pydantic==2.11.7
httpx==0.28.1
python-dotenv==1.1.1
email-validator==2.2.0
rich==14.0.0
flake8==7.0.0
passlib==1.7.4
pyjwt==2.8.0
```

## Exponer con ngrok 
```bash 
ngrok http 8000
```

---

## 📬 Contacto

Si tienes preguntas, sugerencias o deseas contribuir, no dudes en abrir un issue o pull request.

---

## Documentación

### SQLAlchemy:
- https://docs.sqlalchemy.org/en/20/tutorial/engine.html
