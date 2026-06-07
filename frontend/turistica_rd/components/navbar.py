# frontend/turistica_rd/components/navbar.py
"""
Barra de navegación responsive para todas las páginas.
"""
import reflex as rx


def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            # Logo
            rx.link(
                rx.hstack(
                    rx.text("🌴", font_size="1.5rem"),
                    rx.text(
                        "TuristicaRD",
                        font_weight="700",
                        font_size="1.3rem",
                        color="white",
                        letter_spacing="-0.5px",
                    ),
                    spacing="2",
                    align="center",
                ),
                href="/",
                text_decoration="none",
            ),

            rx.spacer(),

            # Links de navegación (desktop)
            rx.hstack(
                rx.link("Inicio",       href="/",            color="white", font_weight="500",
                        _hover={"color": "#FDE68A"}, text_decoration="none"),
                rx.link("Destinos",     href="/#ofertas",    color="white", font_weight="500",
                        _hover={"color": "#FDE68A"}, text_decoration="none"),
                rx.link("Descripción",  href="/descripcion", color="white", font_weight="500",
                        _hover={"color": "#FDE68A"}, text_decoration="none"),
                rx.link(
                    "Reservar Ahora",
                    href="/reservas",
                    background="#FBBF24",
                    color="#1C1917",
                    font_weight="700",
                    padding="0.5rem 1.25rem",
                    border_radius="8px",
                    text_decoration="none",
                    _hover={"background": "#F59E0B"},
                    transition="background 0.2s",
                ),
                spacing="6",
                display=["none", "none", "flex"],
            ),
        ),
        width="100%",
        max_width="1200px",
        margin="0 auto",
        padding="0 1.5rem",
        height="70px",
        align_items="center",
        display="flex",
    ),
    background="linear-gradient(135deg, #0C4A6E 0%, #075985 100%)",
    position="sticky",
    top="0",
    z_index="1000",
    box_shadow="0 2px 20px rgba(0,0,0,0.25)",
    width="100%",


def footer() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.text("🌴 TuristicaRD", font_weight="700", color="white", font_size="1.2rem"),
                    rx.text(
                        "Tu destino de confianza en República Dominicana",
                        color="#94A3B8",
                        font_size="0.9rem",
                    ),
                    align="start",
                    spacing="2",
                ),
                rx.spacer(),
                rx.vstack(
                    rx.text("Contacto", font_weight="600", color="white"),
                    rx.text("📞 (809) 555-0100", color="#94A3B8", font_size="0.9rem"),
                    rx.text("✉️ info@turistica-rd.com", color="#94A3B8", font_size="0.9rem"),
                    rx.text("📍 Santo Domingo, RD", color="#94A3B8", font_size="0.9rem"),
                    align="start",
                    spacing="1",
                ),
                width="100%",
                max_width="1200px",
                margin="0 auto",
                padding="0 1.5rem",
                flex_wrap="wrap",
                gap="2rem",
            ),
            rx.divider(border_color="#334155"),
            rx.text(
                "© 2025 TuristicaRD. Todos los derechos reservados.",
                color="#64748B",
                font_size="0.85rem",
                text_align="center",
            ),
            width="100%",
            spacing="4",
            padding="3rem 0 2rem",
        ),
        background="#0F172A",
        width="100%",
    )
