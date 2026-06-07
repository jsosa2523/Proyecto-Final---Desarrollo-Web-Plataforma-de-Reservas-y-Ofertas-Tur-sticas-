# 🌴 TuristicaRD — Plataforma de Reservas y Ofertas Turísticas

[![Deploy on Render](https://img.shields.io/badge/Deploy-Render-46E3B7?logo=render)](https://render.com)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python)](https://python.org)
[![Reflex](https://img.shields.io/badge/Reflex-0.4.x-8B5CF6)](https://reflex.dev)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?logo=mysql)](https://mysql.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Plataforma web completa para reservas y publicación de ofertas turísticas en República Dominicana. Desarrollada con **Reflex** (Python), una **API REST** con FastAPI y una base de datos **MySQL**.

---

## 📸 Vista Previa

```
┌──────────────────────────────────────┐
│   🌴 TuristicaRD                     │
│   Inicio | Descripción | Reservas    │
│                                      │
│  [Buscar destino...]  [Buscar →]     │
│                                      │
│  🏖️ Ofertas Destacadas              │
│  ┌──────┐ ┌──────┐ ┌──────┐         │
│  │Punta │ │Santo │ │Samaná│         │
│  │Cana  │ │Domingo│ │     │         │
│  └──────┘ └──────┘ └──────┘         │
└──────────────────────────────────────┘
```

---

## 📋 Descripción del Proyecto

**TuristicaRD** es una plataforma turística que permite:

- 🔍 **Buscar** destinos y paquetes turísticos en República Dominicana
- 🏷️ **Explorar** ofertas con imágenes, precios e itinerarios detallados
- 📅 **Reservar** actividades turísticas directamente en línea
- 📞 **Contactar** a la empresa para información personalizada

### Tecnologías Utilizadas

| Capa | Tecnología |
|------|-----------|
| Frontend | Reflex (Python) |
| Backend / API | FastAPI |
| Base de Datos | MySQL 8.0 |
| ORM | SQLAlchemy |
| Despliegue | Render |
| Control de Versiones | Git / GitFlow |

---

## 🚀 Cómo Instalar y Ejecutar

### Prerrequisitos

- Python 3.11+
- MySQL 8.0+
- Node.js 18+ (requerido por Reflex)
- Git

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/turistica-rd.git
cd turistica-rd
```

### 2. Crear Entorno Virtual

```bash
python -m venv venv

# En Windows
venv\Scripts\activate

# En macOS/Linux
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

```bash
cp .env.example .env
```

Edita el archivo `.env` con tus datos:

```env
# Base de datos
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=turistica_db

# API
API_HOST=0.0.0.0
API_PORT=8000
SECRET_KEY=tu_clave_secreta_muy_larga

# Entorno
ENV=development
```

### 5. Configurar Base de Datos

```bash
# Crear la base de datos
mysql -u root -p < database/schema.sql

# Cargar datos de ejemplo
mysql -u root -p turistica_db < database/seed.sql
```

### 6. Ejecutar la API (Terminal 1)

```bash
cd api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

La API estará disponible en: `http://localhost:8000`  
Documentación Swagger: `http://localhost:8000/docs`

### 7. Ejecutar el Frontend Reflex (Terminal 2)

```bash
reflex run
```

El sitio estará disponible en: `http://localhost:3000`

---

## 📁 Estructura de Carpetas

```
turistica-rd/
│
├── 📂 api/                     # Backend FastAPI
│   ├── main.py                 # Punto de entrada de la API
│   ├── models.py               # Modelos SQLAlchemy
│   ├── schemas.py              # Esquemas Pydantic
│   ├── routes/
│   │   ├── ofertas.py          # Endpoints de ofertas turísticas
│   │   └── reservas.py         # Endpoints de reservas
│   └── database.py             # Configuración de la DB
│
├── 📂 frontend/                # Frontend Reflex
│   ├── turistica_rd/           # App Reflex principal
│   │   ├── pages/
│   │   │   ├── inicio.py       # Página de inicio
│   │   │   ├── descripcion.py  # Página de descripción
│   │   │   └── reservas.py     # Página de reservas
│   │   ├── components/
│   │   │   ├── navbar.py       # Barra de navegación
│   │   │   ├── footer.py       # Pie de página
│   │   │   ├── oferta_card.py  # Tarjeta de oferta
│   │   │   └── formulario_reserva.py
│   │   └── turistica_rd.py     # Estado global de la app
│
├── 📂 database/                # Scripts SQL
│   ├── schema.sql              # Estructura de tablas
│   └── seed.sql                # Datos de ejemplo
│
├── 📂 docs/                    # Documentación adicional
│   ├── api_endpoints.md        # Documentación de la API
│   └── gitflow.md              # Guía de GitFlow
│
├── .env.example                # Variables de entorno de ejemplo
├── .gitignore                  # Archivos ignorados por Git
├── requirements.txt            # Dependencias Python
├── render.yaml                 # Configuración de Render
└── README.md                   # Este archivo
```

---

## 🔌 API Endpoints

### Ofertas Turísticas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/ofertas` | Listar todas las ofertas |
| `GET` | `/api/ofertas/{id}` | Obtener oferta por ID |
| `GET` | `/api/ofertas/buscar?q={texto}` | Buscar ofertas |

### Reservas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/reservas` | Crear nueva reserva |
| `GET` | `/api/reservas` | Listar todas las reservas |
| `GET` | `/api/reservas/{id}` | Obtener reserva por ID |

### Ejemplo de Respuesta — GET /api/ofertas

```json
[
  {
    "id": 1,
    "nombre": "Punta Cana Todo Incluido",
    "descripcion": "5 días en el paraíso caribeño",
    "precio": 45000.00,
    "duracion_dias": 5,
    "imagen_url": "/assets/punta-cana.jpg",
    "disponible": true
  }
]
```

### Ejemplo de Body — POST /api/reservas

```json
{
  "nombre_cliente": "Juan Pérez",
  "email": "juan@email.com",
  "telefono": "809-555-1234",
  "oferta_id": 1,
  "fecha_viaje": "2025-08-15",
  "num_personas": 2,
  "metodo_pago": "tarjeta"
}
```

---

## 🌿 Flujo de Trabajo con GitFlow

Este proyecto sigue la metodología **GitFlow**. Las ramas principales son:

```
main          ← Producción (código estable)
develop       ← Desarrollo (integración)
feature/*     ← Nuevas funcionalidades
hotfix/*      ← Correcciones urgentes
release/*     ← Preparación de versiones
```

### Historial de Commits Principales

| Commit | Mensaje | Descripción |
|--------|---------|-------------|
| `a1b2c3d` | `feat: init project structure and base config` | Estructura inicial del proyecto |
| `e4f5g6h` | `feat: add MySQL schema and seed data` | Base de datos y datos de prueba |
| `i7j8k9l` | `feat: implement REST API with FastAPI` | API completa con todos los endpoints |
| `m1n2o3p` | `feat: add Reflex frontend pages` | Páginas de Inicio, Descripción y Reservas |
| `q4r5s6t` | `feat: add form validation and error handling` | Validaciones y manejo de errores |
| `u7v8w9x` | `fix: cors policy and mobile responsive fixes` | Correcciones de CORS y responsive |
| `y1z2a3b` | `deploy: render config and env setup` | Configuración de despliegue en Render |

---

## ☁️ Despliegue en Render

El proyecto está desplegado en dos servicios de Render:

- **Frontend (Static Site):** `https://turistica-rd.onrender.com`
- **API (Web Service):** `https://api-turistica-rd.onrender.com`

### Configuración (`render.yaml`)

```yaml
services:
  - type: web
    name: turistica-api
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: cd api && uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DB_HOST
        sync: false
      - key: SECRET_KEY
        generateValue: true
```

---

## 👥 Créditos

**Desarrollado como proyecto final de Desarrollo Web**

- 👨‍💻 **Desarrollador:** Tu Nombre
- 📚 **Institución:** Tu Universidad / Instituto
- 📅 **Año:** 2025

### Recursos y Referencias

- [Reflex Documentation](https://reflex.dev/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org)
- [Render Deploy Guide](https://render.com/docs)
- [GitFlow Workflow](https://nvie.com/posts/a-successful-git-branching-model/)

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.
