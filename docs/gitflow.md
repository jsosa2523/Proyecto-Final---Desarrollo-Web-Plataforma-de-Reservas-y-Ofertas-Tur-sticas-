# 🌿 Guía de GitFlow — TuristicaRD

Este documento describe la organización de ramas y el historial de commits del proyecto.

---

## Estructura de Ramas (GitFlow)

```
main
├── develop
│   ├── feature/base-datos-schema
│   ├── feature/api-rest-ofertas
│   ├── feature/api-rest-reservas
│   ├── feature/frontend-pagina-inicio
│   ├── feature/frontend-pagina-descripcion
│   ├── feature/frontend-pagina-reservas
│   ├── feature/validaciones-formulario
│   └── feature/deploy-render
├── release/v1.0.0
└── hotfix/cors-fix
```

---

## Historial Completo de Commits

### 🚀 Commit 1 — Estructura inicial
```
commit a1b2c3d4e5f6789012345678901234567890abcd
Author: Tu Nombre <tu@email.com>
Date:   Mon Jan 06 09:00:00 2025 -0400

feat: init project structure and base configuration

- Crear estructura de carpetas del proyecto
- Agregar .gitignore y .env.example
- Configurar requirements.txt con dependencias
- Inicializar README.md con descripción del proyecto
```

### 🗄️ Commit 2 — Base de datos
```
commit b2c3d4e5f6789012345678901234567890abcde1
Author: Tu Nombre <tu@email.com>
Date:   Tue Jan 07 10:30:00 2025 -0400

feat: add MySQL database schema and seed data

- Crear database/schema.sql con tablas: destinos,
  ofertas_turisticas, reservas
- Agregar índices para optimizar consultas
- Crear database/seed.sql con 4 ofertas de ejemplo
- Definir relaciones con foreign keys
```

### 🔌 Commit 3 — API REST completa
```
commit c3d4e5f6789012345678901234567890abcde12f
Author: Tu Nombre <tu@email.com>
Date:   Thu Jan 09 14:15:00 2025 -0400

feat: implement full REST API with FastAPI

- Crear api/database.py con conexión SQLAlchemy + MySQL
- Definir modelos ORM en api/models.py
- Crear esquemas Pydantic en api/schemas.py
- Implementar api/routes/ofertas.py:
    GET  /api/ofertas         (listar con filtros)
    GET  /api/ofertas/buscar  (búsqueda por texto)
    GET  /api/ofertas/{id}    (detalle)
- Implementar api/routes/reservas.py:
    POST /api/reservas        (crear reserva)
    GET  /api/reservas        (listar)
    GET  /api/reservas/{id}   (detalle)
- Configurar CORS middleware en main.py
- Agregar endpoint /health para Render
```

### 🎨 Commit 4 — Frontend Reflex (páginas)
```
commit d4e5f6789012345678901234567890abcde12f3a
Author: Tu Nombre <tu@email.com>
Date:   Sat Jan 11 11:00:00 2025 -0400

feat: add Reflex frontend with three pages

- Crear components/navbar.py con nav responsive y footer
- Implementar pages/inicio.py:
    + Hero section con búsqueda
    + Grid de ofertas turísticas (carga desde API)
    + Sección de contacto/CTA
- Implementar pages/descripcion.py:
    + Hero con imagen de portada
    + Descripción general del paquete
    + Lista de qué incluye
    + Itinerario día a día
    + Card sticky de reserva
- Implementar pages/reservas.py:
    + Sección de datos de contacto
    + Selector de paquete y fecha
    + Opciones de método de pago
    + Panel de resumen con total calculado
- Configurar rutas en turistica_rd.py
```

### ✅ Commit 5 — Validaciones y manejo de errores
```
commit e5f6789012345678901234567890abcde12f3a4b
Author: Tu Nombre <tu@email.com>
Date:   Mon Jan 13 16:45:00 2025 -0400

feat: add form validation and comprehensive error handling

- Validar campos obligatorios antes de enviar reserva
- Agregar validación de fecha futura en Pydantic schema
- Mostrar mensajes de error amigables al usuario
- Agregar estado de carga (spinner) en botones
- Mostrar pantalla de éxito con mensaje de confirmación
- Manejar errores de red con catch en peticiones HTTP
- Agregar validación de num_personas (mínimo 1)
```

### 🐛 Commit 6 — Fix CORS y mejoras responsive
```
commit f6789012345678901234567890abcde12f3a4b5c
Author: Tu Nombre <tu@email.com>
Date:   Wed Jan 15 09:20:00 2025 -0400

fix: cors policy update and mobile responsive improvements

- Agregar URL de producción a allowed origins en CORS
- Corregir layout en pantallas móviles (< 768px)
- Hacer navbar funcional en dispositivos pequeños
- Ajustar tamaños de fuente en hero sections
- Corregir grid de ofertas en mobile (1 columna)
- Mejorar espaciado en formulario de reservas
```

### ☁️ Commit 7 — Configuración de despliegue
```
commit a7b8c9d0e1f2345678901234567890abcde12f3a
Author: Tu Nombre <tu@email.com>
Date:   Fri Jan 17 13:00:00 2025 -0400

deploy: add Render configuration and production setup

- Crear render.yaml con dos servicios (API + Frontend)
- Agregar variables de entorno para producción
- Configurar healthcheck endpoint en /health
- Actualizar README con instrucciones de despliegue
- Documentar endpoints de la API con ejemplos
- Agregar badge de deploy en el README
```

---

## Comandos Git Usados

```bash
# Clonar y configurar
git clone https://github.com/tu-usuario/turistica-rd.git
git config user.name "Tu Nombre"
git config user.email "tu@email.com"

# Flujo de trabajo GitFlow
git checkout -b develop
git checkout -b feature/base-datos-schema

# Commits
git add database/
git commit -m "feat: add MySQL database schema and seed data"

# Merge a develop
git checkout develop
git merge feature/base-datos-schema --no-ff

# Release
git checkout -b release/v1.0.0
git tag -a v1.0.0 -m "Primera versión estable"
git checkout main
git merge release/v1.0.0
git push origin main --tags
```
