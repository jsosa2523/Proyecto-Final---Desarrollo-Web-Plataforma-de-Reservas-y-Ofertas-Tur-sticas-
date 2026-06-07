# frontend/turistica_rd/pages/inicio.py
import reflex as rx
import httpx
from typing import List, Any

from turistica_rd.components.navbar import navbar, footer

API_BASE = "http://localhost:8000"


class OfertaItem(rx.Base):
    id: int = 0
    nombre: str = ""
    descripcion: str = ""
    precio: str = ""
    duracion_dias: int = 0
    imagen_url: str = ""
    destacada: bool = False
    disponible: bool = True


class InicioState(rx.State):
    ofertas: List[OfertaItem] = []
    busqueda: str = ""
    cargando: bool = False
    error: str = ""

    async def cargar_ofertas(self):
        self.cargando = True
        self.error = ""
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{API_BASE}/api/ofertas",
                    params={"disponible": "true"},
                    timeout=10,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    self.ofertas = [
                        OfertaItem(
                            id=o.get("id", 0),
                            nombre=o.get("nombre", ""),
                            descripcion=o.get("descripcion", ""),
                            precio=str(o.get("precio", "0")),
                            duracion_dias=o.get("duracion_dias", 1),
                            imagen_url=o.get("imagen_url", ""),
                            destacada=o.get("destacada", False),
                            disponible=o.get("disponible", True),
                        )
                        for o in data
                    ]
        except Exception:
            self.error = "No se pudieron cargar las ofertas. Verifica que la API esté corriendo."
        finally:
            self.cargando = False

    async def buscar(self):
        if not self.busqueda.strip():
            await self.cargar_ofertas()
            return
        self.cargando = True
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{API_BASE}/api/ofertas/buscar",
                    params={"q": self.busqueda},
                    timeout=10,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    self.ofertas = [
                        OfertaItem(
                            id=o.get("id", 0),
                            nombre=o.get("nombre", ""),
                            descripcion=o.get("descripcion", ""),
                            precio=str(o.get("precio", "0")),
                            duracion_dias=o.get("duracion_dias", 1),
                            imagen_url=o.get("imagen_url", ""),
                            destacada=o.get("destacada", False),
                        )
                        for o in data
                    ]
                else:
                    self.ofertas = []
        except Exception:
            self.error = "Error en la búsqueda."
        finally:
            self.cargando = False

    def set_busqueda(self, value: str):
        self.busqueda = value


def oferta_card(oferta: OfertaItem) -> rx.Component:
    return rx.box(
        rx.image(
            src=oferta.imagen_url,
            width="100%",
            height="200px",
            object_fit="cover",
            border_radius="12px 12px 0 0",
        ),
        rx.vstack(
            rx.text(
                oferta.nombre,
                font_weight="700",
                font_size="1rem",
                color="#1E293B",
            ),
            rx.text(
                oferta.descripcion,
                color="#475569",
                font_size="0.875rem",
            ),
            rx.hstack(
                rx.vstack(
                    rx.text(
                        oferta.precio,
                        font_size="1.2rem",
                        font_weight="800",
                        color="#0C4A6E",
                    ),
                    rx.text(
                        oferta.duracion_dias,
                        font_size="0.8rem",
                        color="#64748B",
                    ),
                    spacing="0",
                    align="start",
                ),
                rx.spacer(),
                rx.link(
                    rx.button(
                        "Ver detalles →",
                        background="#0C4A6E",
                        color="white",
                        border_radius="8px",
                        padding="0.5rem 1rem",
                        font_weight="600",
                        cursor="pointer",
                    ),
                    href="/descripcion",
                ),
                width="100%",
                align="end",
            ),
            padding="1.25rem",
            spacing="3",
            align="start",
        ),
        background="white",
        border_radius="12px",
        box_shadow="0 4px 20px rgba(0,0,0,0.08)",
        overflow="hidden",
    )


def seccion_hero() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(
                "Descubre la Magia de",
                font_size=["1.5rem", "2rem", "2.5rem"],
                color="#BAE6FD",
                font_weight="400",
            ),
            rx.text(
                "República Dominicana",
                font_size=["2rem", "3rem", "3.5rem"],
                font_weight="800",
                color="white",
                text_align="center",
            ),
            rx.text(
                "Playas, montañas, cultura e historia. Tu aventura comienza aquí.",
                font_size="1rem",
                color="#CBD5E1",
                text_align="center",
                max_width="600px",
            ),
            rx.box(
                rx.hstack(
                    rx.input(
                        placeholder="¿A dónde quieres ir? Ej: Punta Cana...",
                        value=InicioState.busqueda,
                        on_change=InicioState.set_busqueda,
                        flex="1",
                        height="52px",
                        font_size="1rem",
                        border="none",
                        outline="none",
                        padding="0 1rem",
                        background="white",
                        border_radius="10px 0 0 10px",
                    ),
                    rx.button(
                        "Buscar",
                        on_click=InicioState.buscar,
                        height="52px",
                        padding="0 1.5rem",
                        background="#FBBF24",
                        color="#1C1917",
                        font_weight="700",
                        font_size="1rem",
                        border_radius="0 10px 10px 0",
                        cursor="pointer",
                        border="none",
                    ),
                    spacing="0",
                    width="100%",
                ),
                border_radius="10px",
                width=["100%", "90%", "680px"],
                overflow="hidden",
            ),
            spacing="5",
            align="center",
            padding=["4rem 1.5rem", "6rem 2rem"],
        ),
        background="linear-gradient(135deg, #0C4A6E 0%, #0E7490 50%, #1D4ED8 100%)",
        width="100%",
        display="flex",
        justify_content="center",
        min_height="480px",
    )


def seccion_ofertas() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(
                "Ofertas Turísticas",
                font_size=["1.8rem", "2.5rem"],
                font_weight="800",
                color="#0F172A",
                text_align="center",
            ),
            rx.text(
                "Los destinos más populares con los mejores precios",
                color="#64748B",
                text_align="center",
            ),
            rx.cond(
                InicioState.cargando,
                rx.spinner(size="3"),
                rx.cond(
                    InicioState.error != "",
                    rx.text(InicioState.error, color="red"),
                    rx.grid(
                        rx.foreach(InicioState.ofertas, oferta_card),
                        columns="3",
                        gap="1.5rem",
                        width="100%",
                    ),
                ),
            ),
            spacing="6",
            width="100%",
            max_width="1200px",
            margin="0 auto",
            padding=["3rem 1.5rem", "5rem 2rem"],
            on_mount=InicioState.cargar_ofertas,
        ),
        id="ofertas",
        background="#F8FAFC",
        width="100%",
    )


def seccion_contacto() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(
                "Contáctanos",
                font_size="2rem",
                font_weight="800",
                color="white",
                text_align="center",
            ),
            rx.text(
                "Estamos aquí para ayudarte a planificar el viaje perfecto.",
                color="#94A3B8",
                text_align="center",
            ),
            rx.hstack(
                rx.vstack(
                    rx.text("📍 Av. Abraham Lincoln 1205, Santo Domingo", color="#94A3B8"),
                    rx.text("📞 (809) 555-0100", color="#94A3B8"),
                    rx.text("✉️ info@turistica-rd.com", color="#94A3B8"),
                    rx.text("🕐 Lun–Vie 8:00am–6:00pm", color="#94A3B8"),
                    spacing="2",
                    align="start",
                ),
                rx.spacer(),
                rx.link(
                    rx.button(
                        "Hacer mi Reserva →",
                        background="#FBBF24",
                        color="#1C1917",
                        font_weight="700",
                        font_size="1.1rem",
                        padding="0.875rem 2rem",
                        border_radius="10px",
                        cursor="pointer",
                        border="none",
                    ),
                    href="/reservas",
                ),
                flex_wrap="wrap",
                gap="2rem",
                width="100%",
                max_width="1200px",
                padding="0 1.5rem",
            ),
            spacing="6",
            width="100%",
            padding=["3rem 0", "5rem 0"],
        ),
        background="linear-gradient(135deg, #0F172A 0%, #1E293B 100%)",
        width="100%",
    )


def inicio_page() -> rx.Component:
    return rx.box(
        navbar(),
        seccion_hero(),
        seccion_ofertas(),
        seccion_contacto(),
        footer(),
        width="100%",
        min_height="100vh",
        font_family="'Inter', system-ui, sans-serif",
    )
