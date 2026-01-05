# Tardigrade Project

Este proyecto será usado como template para crear proyectos que sigan buenos estandares y prácticas para
el desarrollo de software maduro y resistente.

Los proyectos desarrollados con Tardigrade Project deben estar orientados para ser desarrollados con IDEs  empoderados con AI, por ejemplo Kiro, Cursor o Github Copilot. También deben estar orientados a que el equipo de desarrollo este enfocado en desarrollo y no romperse la cabeza con despliegues.

Los proyectos desarrollados en base a este template serán orientados a backend con python. No incluye el server side rendering. Sólo el desarrollo de APIs.

El stack inicial será:

- Python 3.12
- FastAPI
- SQLAlchemy
- Alembic
- Docker
- Docker Compose
- Terraform
- Gitlab CI
- Github Actions

Para asegurar la buena cálidad de código se usará de

- Virtualenv (venv)
- Black
- Flake8
- Isort
- Pytest

## Cálidad de código

Todo el proyecto debe estar en ingles y las variables deben estar en snake_case.

Cada que se crea un nuevo módulo o funcionalidad "importante" o "relevante" se deben crear las pruebas unitarias correspondientes.

Se debe considerar el uso de Arquitectura hexagonal, desarrollo con paradigma funcional, seguir el principio de funciones de unica responsabilidad, documentar con docstrings las funciones, clases y cualquier tipo de instancia.

Las configuraciones de flake8, editorconfig y black son:
- 120 caracteres de ancho
- 4 espacios de indentación
- Comillas dobles

Se deben considerar los githooks para que se ejecuten:
- pre-commit:  black, flake8, isort

Debe existir un archivo `.gitignore` con los archivos que no se deben subir a git.

## CI/CD

Se debe considerar el uso de variables de entorno para los secrets y las credenciales de AWS, incluso
para las configuraciones necesarias para el proyecto.

En la raíz del proyecto se deben considerar las carpetas de `terraform` y `docker`, en las que se incluiran los archivos correspondientes ordenados en diferentes carpentas para los entornos `local`, `qa` y `production`.

El CI/CD de Gitlab y Github deben estar orientados a
 MR hacia `staging` o `dev`
- Revisar la cálidad del código
- Ejecutar las pruebas unitarias (80% de coverage). Genera un reporte descargable.
- Compila la imagen docker para `qa` y el artefacto puede ser descargable durante 7 días.

 MR hacia `main`:
- Revisar la cálidad del código
- Ejecutar las pruebas unitarias (80% de coverage). Genera un reporte descargable.
- Compila la imagen docker para `production` y el artefacto puede ser descargable durante 7 días.
- Ejecuta `terraform plan`
- Prepara `terraform apply` como un trigger manual
- El MR sólo puede ser aceptado si `terraform plan` fue exitoso.

Cualquier paso o job de los pipelines de CI/CD deben de considerar que el repositorio de código está enlazado con OIDC para los despliegues de recursos, y debe dejar comentada la opción de obtener las credenciales por medio de variables de entorno.

En terraform se deben de incluir los servicios básicos de AWS para el desarrollo y despliegue del API.
Los archivos de configuración de terraform deben estar organizados con archivos independientes por cada servicio, así facilitando el trabajo para los desarrolladores.

## Desarrollo

El proyecto debe incluir una carpeta `scripts` en los que se encuentren los archivos necesarios para cada miembro del proyecto pueda interactuar con el proyecto, por ejemplo:

- `scripts/setup.sh`: Crea el entorno virtual si no existe, instala las dependencias y prepara los githooks.
- `scripts/run.sh`: Ejecuta el proyecto en modo desarrollo.
- `scripts/test.sh`: Ejecuta las pruebas unitarias.
- `scripts/terraform.sh`: Ejecuta terraform.
- `scripts/init-terraform.sh`: Inicualiza terraform. Está pensado para ser ejecutado una sola vez por el líder técnico para preparar los despliegues.
