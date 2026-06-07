# frontend/turistica_rd/pages/descripcion.py
import reflex as rx
import httpx
from typing import List

from turistica_rd.components.navbar import navbar, footer

API_BASE = "http://localhost:8000"


class DiaItinerario(rx.Base):
    dia: int = 0
    titulo: str = ""
    descripcion: str = ""


class OfertaDetalle(rx.Base):
    id: int = 0
    nombre: str = ""
    descripcion: str = ""
    descripcion_larga: str = ""
    precio: str = ""
    duracion_dias: int = 0
    imagen_url: str = ""
    itinerario: List[DiaItinerario] = []
    incluye: List[str] = []


class DescripcionState(rx.State):
    oferta: OfertaDetalle = OfertaDetalle()
    cargando: bool = True
    error: str = ""

    async def cargar_oferta(self):
        self.cargando = True
        self.error = ""
        oferta_id = self.router.page.params.get("id", "1")
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{API_BASE}/api/ofertas/{oferta_id}", timeout=10
                )
                if resp.status_code == 200:
                    o = resp.json()
                    itinerario = [
                        DiaItinerario(
                            dia=d.get("dia", 0),
                            titulo=d.get("titulo", ""),
                            descripcion=d.get("descripcion", ""),
                        )
                        for d in (o.get("itinerario") or [])
                    ]
                    incluye = [str(i) for i in (o.get("incluye") or [])]
                    self.oferta = OfertaDetalle(
                        id=o.get("id", 0),
                        nombre=o.get("nombre", ""),
                        descripcion=o.get("descripcion", ""),
                        descripcion_larga=o.get("descripcion_larga") or o.get("descripcion", ""),
                        precio=str(o.get("precio", "0")),
                        duracion_dias=o.get("duracion_dias", 1),
                        imagen_url=o.get("imagen_url", ""),
                        itinerario=itinerario,
                        incluye=incluye,
                    )
                else:
                    self.error = "Oferta no encontrada."
        except Exception:
            self.error = "Error al cargar los detalles."
        finally:
            self.cargando = False


def dia_card(dia: DiaItinerario) -> rx.Component:
    return rx.hstack(
        rx.box(
            rx.text(
                "Día",
                font_size="0.7rem",
                font_weight="700",
                color="white",
            ),
            rx.text(
                dia.dia,
                font_size="1.2rem",
                font_weight="800",
                color="white",
            ),
            background="#0C4A6E",
            padding="0.5rem 0.75rem",
            border_radius="8px",
            min_width="55px",
            text_align="center",
            flex_shrink="0",
        ),
        rx.vstack(
            rx.text(dia.titulo, font_weight="600", color="#1E293B"),
            rx.text(dia.descripcion, color="#64748B", font_size="0.9rem"),
            spacing="1",
            align="start",
        ),
        spacing="3",
        align="start",
        width="100%",
        padding="1rem",
        background="white",
        border_radius="10px",
        box_shadow="0 2px 8px rgba(0,0,0,0.06)",
    )


def incluye_item(item: str) -> rx.Component:
    return rx.hstack(
        rx.text("✅"),
        rx.text(item, color="#374151"),
        spacing="2",
    )


def descripcion_page() -> rx.Component:
    return rx.box(
        navbar(),
        rx.cond(
            DescripcionState.cargando,
            rx.center(rx.spinner(size="3"), padding="8rem"),
            rx.cond(
                DescripcionState.error != "",
                rx.center(
                    rx.text(DescripcionState.error, color="red"),
                    padding="4rem",
                ),
                rx.box(
                    # Hero con imagen
                    rx.box(
                        rx.image(
                            src=DescripcionState.oferta.imagen_url,
                            width="100%",
                            height="400px",
                            object_fit="cover",
                        ),
                        rx.box(
                            rx.vstack(
                                rx.text(
                                    DescripcionState.oferta.nombre,
                                    font_size=["1.8rem", "2.5rem"],
                                    font_weight="800",
                                    color="white",
                                ),
                                rx.hstack(
                                    rx.badge(
                                        DescripcionState.oferta.duracion_dias,
                                        color_scheme="blue",
                                    ),
                                    rx.badge(
                                        DescripcionState.oferta.precio,
                                        color_scheme="green",
                                    ),
                                ),
                                spacing="3",
                                align="start",
                                max_width="1200px",
                                width="100%",
                                margin="0 auto",
                                padding="2rem 1.5rem",
                            ),
                        ),
                        position="relative",
                        width="100%",
                        background="linear-gradient(to top, rgba(0,0,0,0.7) 0%, transparent 50%)",
                    ),
                    # Contenido
                    rx.box(
                        rx.hstack(
                            # Columna izquierda
                            rx.vstack(
                                rx.box(
                                    rx.text(
                                        "Descripción General",
                                        font_size="1.4rem",
                                        font_weight="700",
                                        color="#0F172A",
                                    ),
                                    rx.text(
                                        DescripcionState.oferta.descripcion_larga,
                                        color="#475569",
                                        line_height="1.8",
                                        margin_top="0.75rem",
                                    ),
                                    background="white",
                                    border_radius="12px",
                                    padding="1.5rem",
                                    box_shadow="0 2px 10px rgba(0,0,0,0.06)",
                                ),
                                rx.box(
                                    rx.text(
                                        "¿Qué incluye?",
                                        font_size="1.2rem",
                                        font_weight="700",
                                        color="#0F172A",
                                    ),
                                    rx.vstack(
                                        rx.foreach(
                                            DescripcionState.oferta.incluye,
                                            incluye_item,
                                        ),
                                        spacing="2",
                                        align="start",
                                        margin_top="0.75rem",
                                    ),
                                    background="white",
                                    border_radius="12px",
                                    padding="1.5rem",
                                    box_shadow="0 2px 10px rgba(0,0,0,0.06)",
                                ),
                                rx.box(
                                    rx.text(
                                        "Itinerario",
                                        font_size="1.4rem",
                                        font_weight="700",
                                        color="#0F172A",
                                    ),
                                    rx.vstack(
                                        rx.foreach(
                                            DescripcionState.oferta.itinerario,
                                            dia_card,
                                        ),
                                        spacing="3",
                                        width="100%",
                                        margin_top="1rem",
                                    ),
                                    background="#F8FAFC",
                                    border_radius="12px",
                                    padding="1.5rem",
                                ),
                                spacing="5",
                                flex="2",
                                min_width="0",
                            ),
                            # Card reserva
                            rx.box(
                                rx.vstack(
                                    rx.text(
                                        "Reserva este paquete",
                                        font_weight="700",
                                        font_size="1.1rem",
                                        color="#0F172A",
                                    ),
                                    rx.divider(),
                                    rx.hstack(
                                        rx.text("Precio:", color="#64748B"),
                                        rx.spacer(),
                                        rx.text(
                                            DescripcionState.oferta.precio,
                                            font_weight="700",
                                            color="#0C4A6E",
                                            font_size="1.2rem",
                                        ),
                                        width="100%",
                                    ),
                                    rx.hstack(
                                        rx.text("Duración:", color="#64748B"),
                                        rx.spacer(),
                                        rx.text(
                                            DescripcionState.oferta.duracion_dias,
                                            font_weight="600",
                                        ),
                                        width="100%",
                                    ),
                                    rx.link(
                                        rx.button(
                                            "Reservar Ahora →",
                                            background="#0C4A6E",
                                            color="white",
                                            width="100%",
                                            height="50px",
                                            font_size="1rem",
                                            font_weight="700",
                                            border_radius="10px",
                                            cursor="pointer",
                                            border="none",
                                        ),
                                        href="/reservas",
                                        width="100%",
                                    ),
                                    rx.text(
                                        "🔒 Reserva 100% segura",
                                        color="#64748B",
                                        font_size="0.8rem",
                                        text_align="center",
                                    ),
                                    spacing="3",
                                    width="100%",
                                ),
                                background="white",
                                border_radius="12px",
                                padding="1.5rem",
                                box_shadow="0 4px 20px rgba(0,0,0,0.1)",
                                position="sticky",
                                top="90px",
                                align_self="flex-start",
                                flex="1",
                                min_width="280px",
                            ),
                            flex_wrap="wrap",
                            gap="2rem",
                            width="100%",
                            max_width="1200px",
                            margin="0 auto",
                            padding=["2rem 1.5rem", "3rem 2rem"],
                            align="start",
                        ),
                        background="#F8FAFC",
                        width="100%",
                    ),
                    on_mount=DescripcionState.cargar_oferta,
                    width="100%",
                ),
            ),
        ),
        footer(),
        width="100%",
        min_height="100vh",
        font_family="'Inter', system-ui, sans-serif",
    )
