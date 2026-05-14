import re

from googleapiclient.errors import HttpError


ALLOWED_DOMAIN = "unal.edu.co"


class GoogleEmailValidator:
    """
    Validador de emails usando Google Admin Directory API.
    Requiere una service account con permisos en Google Workspace.
    """

    @staticmethod
    def validate_unal_email_format(email: str) -> bool:
        """
        Valida que el email tenga el formato correcto de @unal.edu.co
        """
        pattern = r"^[a-zA-Z0-9._%+-]+@unal\.edu\.co$"
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_email_exists_in_google(email: str) -> bool:
        """
        Valida que el email existe en Google usando la API de Google.

        Para usar en producción, necesitas:
        1. Crear una service account en Google Cloud Console
        2. Otorgarle permisos en Google Admin (Directory API)
        3. Guardar la credencial JSON en una variable de entorno

        Por ahora, retorna True si el formato es válido
        (sin validación real en Google, para no romper en dev)

        Futuro: implementar con service account credenciales desde env var
        """
        try:
            # TODO: Implementar validación real en Google cuando tengas
            # Google Workspace admin credentials.
            # Por ahora, solo validamos formato.
            return GoogleEmailValidator.validate_unal_email_format(email)

        except HttpError:
            # Email no existe o error en la API
            return False
        except Exception:
            # Otros errores (credenciales, conexión, etc)
            return False

    @staticmethod
    def validate_and_raise(email: str) -> None:
        """
        Valida el email y levanta excepción si no es válido.
        """
        if not GoogleEmailValidator.validate_unal_email_format(email):
            raise ValueError(
                f"Email must be from @{ALLOWED_DOMAIN} domain"
            )

        if not GoogleEmailValidator.validate_email_exists_in_google(email):
            raise ValueError(
                "Email does not exist in Google or validation failed"
            )
