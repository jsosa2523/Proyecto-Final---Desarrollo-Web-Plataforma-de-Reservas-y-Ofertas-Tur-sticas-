# 📡 Documentación de la API — TuristicaRD

Base URL: `https://api-turistica-rd.onrender.com`  
Documentación interactiva: `/docs` (Swagger UI)

---

## Autenticación

La API actual no requiere autenticación (versión pública).  
Versiones futuras implementarán JWT Bearer tokens.

---

## Endpoints de Ofertas

### GET /api/ofertas
Lista todas las ofertas disponibles.

**Query params:**
| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `disponible` | boolean | Filtrar por disponibilidad |
| `destacada` | boolean | Solo destacadas |

**Respuesta 200:**
```json
[
  {
    "id": 1,
    "destino_id": 1,
    "nombre": "Punta Cana Todo Incluido",
    "descripcion": "5 días en el paraíso caribeño...",
    "descripcion_larga": "Disfruta de los mejores resorts...",
    "precio": "45000.00",
    "precio_original": "55000.00",
    "duracion_dias": 5,
    "imagen_url": "https://...",
    "incluye": ["Traslado", "Hotel", "Alimentación"],
    "itinerario": [{"dia": 1, "titulo": "Llegada", "descripcion": "..."}],
    "disponible": true,
    "destacada": true
  }
]
```

---

### GET /api/ofertas/buscar?q={texto}
Busca ofertas por nombre o descripción.

**Ejemplo:** `GET /api/ofertas/buscar?q=punta`

---

### GET /api/ofertas/{id}
Retorna el detalle completo de una oferta.

**Respuesta 404:** `{"detail": "Oferta no encontrada"}`

---

## Endpoints de Reservas

### POST /api/reservas
Crea una nueva reserva.

**Body:**
```json
{
  "oferta_id": 1,
  "nombre_cliente": "Juan",
  "apellido_cliente": "Pérez",
  "email": "juan@example.com",
  "telefono": "809-555-1234",
  "fecha_viaje": "2025-08-15",
  "num_personas": 2,
  "metodo_pago": "tarjeta",
  "notas": "Habitación con vista al mar"
}
```

**Métodos de pago válidos:** `tarjeta`, `transferencia`, `efectivo`

**Respuesta 201:**
```json
{
  "mensaje": "Reserva creada exitosamente. Total a pagar: RD$ 90,000.00",
  "id": 42
}
```

**Respuesta 422 (validación):**
```json
{
  "detail": [
    {
      "loc": ["body", "fecha_viaje"],
      "msg": "La fecha de viaje debe ser una fecha futura",
      "type": "value_error"
    }
  ]
}
```

---

### GET /api/reservas
Lista todas las reservas (requiere autenticación en v2).

---

### GET /api/reservas/{id}
Obtiene el detalle de una reserva específica.

---

## Códigos de Estado

| Código | Significado |
|--------|-------------|
| `200` | Éxito |
| `201` | Recurso creado |
| `404` | No encontrado |
| `422` | Error de validación |
| `500` | Error interno del servidor |
