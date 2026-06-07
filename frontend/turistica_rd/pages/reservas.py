# frontend/turistica_rd/pages/reservas.py
import reflex as rx
import httpx
from typing import List

from turistica_rd.components.navbar import navbar, footer

API_BASE = "http://localhost:8000"


class OfertaOpcion(rx.Base):
    id: int = 0
    nombre: str = ""
    descripcion: str = ""
    precio: str = ""
    duracion_dias: int = 0


class ReservasState(rx.State):
    nombre: str = ""
    apellido: str = ""
    email: str = ""
    telefono: str = ""
    fecha_viaje: str = ""
    num_personas: int = 1
    metodo_pago: str = "tarjeta"
    notas: str = ""

    oferta_id: int = 1
    oferta_nombre: str = ""
    oferta_descripcion: str = ""
    oferta_precio: str = "0"
    oferta_duracion: int = 0
    ofertas_lista: List[OfertaOpcion] = []

    enviando: bool = False
    exito: bool = False
    error: str = ""
    mensaje_exito: str = ""

    @rx.var
    def monto_total(self) -> str:
        try:
            precio = float(self.oferta_precio)
            total = precio * self.num_personas
            return f"RD$ {total:,.0f}"
        except Exception:
            return "RD$ 0"

    async def cargar_datos_iniciales(self):
        oferta_id = self.router.page.params.get("id", "")
        try:
            async with httpx.AsyncClient() as client:
                resp_lista = await client.get(
                    f"{API_BASE}/api/ofertas", params={"disponible": "true"}
                )
                if resp_lista.status_code == 200:
                    self.ofertas_lista = [
                        OfertaOpcion(
                            id=o.get("id", 0),
                            nombre=o.get("nombre", ""),
                            descripcion=o.get("descripcion", ""),
                            precio=str(o.get("precio", "0")),
                            duracion_dias=o.get("duracion_dias", 1),
                        )
                        for o in resp_lista.json()
                    ]

                target_id = oferta_id if oferta_id else (
                    str(self.ofertas_lista[0].id) if self.ofertas_lista else "1"
                )
                self.oferta_id = int(target_id)

                resp = await client.get(f"{API_BASE}/api/ofertas/{self.oferta_id}")
                if resp.status_code == 200:
                    o = resp.json()
                    self.oferta_nombre = o.get("nombre", "")
                    self.oferta_descripcion = o.get("descripcion", "")
                    self.oferta_precio = str(o.get("precio", "0"))
                    self.oferta_duracion = o.get("duracion_dias", 1)
        except Exception:
            self.error = "Error al cargar las ofertas."

    async def enviar_reserva(self):
        self.error = ""
        if not all([self.nombre, self.apellido, self.email, self.fecha_viaje]):
            self.error = "Por favor completa todos los campos obligatorios (*)"
            return
        self.enviando = True
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    f"{API_BASE}/api/reservas",
                    json={
                        "oferta_id": self.oferta_id,
                        "nombre_cliente": self.nombre,
                        "apellido_cliente": self.apellido,
                        "email": self.email,
                        "telefono": self.telefono,
                        "fecha_viaje": self.fecha_viaje,
                        "num_personas": self.num_personas,
                        "metodo_pago": self.metodo_pago,
                        "notas": self.notas,
                    },
                    timeout=10,
                )
                data = resp.json()
                if resp.status_code == 201:
                    self.exito = True
                    self.mensaje_exito = data.get("mensaje", "¡Reserva creada!")
                else:
                    self.error = str(data.get("detail", "Error al procesar."))
        except Exception:
            self.error = "Error de conexión. Verifica que la API esté corriendo."
        finally:
            self.enviando = False

    def nueva_reserva(self):
        self.exito = False
        self.nombre = self.apellido = self.email = ""
        self.telefono = self.notas = ""
        self.num_personas = 1

    def set_nombre(self, v): self.nombre = v
    def set_apellido(self, v): self.apellido = v
    def set_email(self, v): self.email = v
    def set_telefono(self, v): self.telefono = v
    def set_fecha_viaje(self, v): self.fecha_viaje = v
    def set_num_personas(self, v): self.num_personas = int(v) if v else 1
    def set_metodo_pago(self, v): self.metodo_pago = v
    def set_notas(self, v): self.notas = v


def campo(label: str, componente) -> rx.Component:
    return rx.vstack(
        rx.text(label, font_weight="600", font_size="0.9rem", color="#374151"),
        componente,
        spacing="1",
        align="start",
        width="100%",
    )


def metodo_btn(valor: str, icono: str, label: str) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(icono, font_size="1.5rem"),
            rx.text(label, font_size="0.85rem", font_weight="600"),
            spacing="1",
            align="center",
        ),
        padding="1rem 1.5rem",
        border_radius="10px",
        cursor="pointer",
        border="2px solid",
        border_color=rx.cond(
            ReservasState.metodo_pago == valor,
            "#0C4A6E",
            "#E2E8F0",
        ),
        background=rx.cond(
            ReservasState.metodo_pago == valor,
            "#EFF6FF",
            "white",
        ),
        on_click=ReservasState.set_metodo_pago(valor),
    )


def reservas_page() -> rx.Component:
    return rx.box(
        navbar(),
        rx.cond(
            ReservasState.exito,
            # Pantalla de éxito
            rx.center(
                rx.vstack(
                    rx.text("🎉", font_size="4rem"),
                    rx.text(
                        "¡Reserva Confirmada!",
                        font_size="2rem",
                        font_weight="800",
                        color="#065F46",
                    ),
                    rx.text(
                        ReservasState.mensaje_exito,
                        color="#047857",
                        text_align="center",
                    ),
                    rx.button(
                        "Hacer otra reserva",
                        on_click=ReservasState.nueva_reserva,
                        background="#0C4A6E",
                        color="white",
                        padding="0.75rem 2rem",
                        border_radius="10px",
                        font_weight="700",
                        cursor="pointer",
                        border="none",
                        margin_top="1rem",
                    ),
                    rx.link("← Volver al inicio", href="/", color="#0C4A6E"),
                    spacing="4",
                    align="center",
                    background="white",
                    padding="4rem 2rem",
                    border_radius="16px",
                    box_shadow="0 8px 40px rgba(0,0,0,0.12)",
                    max_width="500px",
                    width="100%",
                ),
                padding=["3rem 1.5rem", "6rem 2rem"],
                background="#ECFDF5",
                min_height="80vh",
                width="100%",
            ),
            # Formulario
            rx.box(
                # Header
                rx.box(
                    rx.vstack(
                        rx.text(
                            "Hacer una Reserva",
                            font_size=["2rem", "2.5rem"],
                            font_weight="800",
                            color="white",
                        ),
                        rx.text(
                            "Completa los datos y confirma tu aventura",
                            color="#BAE6FD",
                        ),
                        spacing="2",
                        align="center",
                        padding=["3rem 1.5rem", "4rem 2rem"],
                        max_width="800px",
                        margin="0 auto",
                    ),
                    background="linear-gradient(135deg, #0C4A6E 0%, #0369A1 100%)",
                    text_align="center",
                    width="100%",
                ),
                rx.box(
                    rx.hstack(
                        # Formulario izquierda
                        rx.vstack(
                            # Sección 1: Contacto
                            rx.box(
                                rx.text(
                                    "1. Datos de Contacto",
                                    font_size="1.1rem",
                                    font_weight="700",
                                    color="#0C4A6E",
                                    border_left="4px solid #0C4A6E",
                                    padding_left="0.75rem",
                                ),
                                rx.grid(
                                    campo("Nombre *", rx.input(
                                        placeholder="Tu nombre",
                                        value=ReservasState.nombre,
                                        on_change=ReservasState.set_nombre,
                                        width="100%",
                                    )),
                                    campo("Apellido *", rx.input(
                                        placeholder="Tu apellido",
                                        value=ReservasState.apellido,
                                        on_change=ReservasState.set_apellido,
                                        width="100%",
                                    )),
                                    campo("Email *", rx.input(
                                        placeholder="correo@email.com",
                                        type="email",
                                        value=ReservasState.email,
                                        on_change=ReservasState.set_email,
                                        width="100%",
                                    )),
                                    campo("Teléfono", rx.input(
                                        placeholder="809-555-0000",
                                        value=ReservasState.telefono,
                                        on_change=ReservasState.set_telefono,
                                        width="100%",
                                    )),
                                    columns="2",
                                    gap="1rem",
                                    width="100%",
                                    margin_top="1rem",
                                ),
                                background="white",
                                border_radius="12px",
                                padding="1.5rem",
                                box_shadow="0 2px 10px rgba(0,0,0,0.06)",
                                width="100%",
                            ),
                            # Sección 2: Actividad
                            rx.box(
                                rx.text(
                                    "2. Detalles de la Actividad",
                                    font_size="1.1rem",
                                    font_weight="700",
                                    color="#0C4A6E",
                                    border_left="4px solid #0C4A6E",
                                    padding_left="0.75rem",
                                ),
                                rx.grid(
                                    campo("Fecha de Viaje *", rx.input(
                                        type="date",
                                        value=ReservasState.fecha_viaje,
                                        on_change=ReservasState.set_fecha_viaje,
                                        width="100%",
                                    )),
                                    campo("Número de Personas *", rx.input(
                                        type="number",
                                        value=ReservasState.num_personas.to_string(),
                                        on_change=ReservasState.set_num_personas,
                                        min="1",
                                        max="20",
                                        width="100%",
                                    )),
                                    campo("Notas adicionales", rx.text_area(
                                        placeholder="Solicitudes especiales, alergias, etc.",
                                        value=ReservasState.notas,
                                        on_change=ReservasState.set_notas,
                                        width="100%",
                                    )),
                                    columns="2",
                                    gap="1rem",
                                    width="100%",
                                    margin_top="1rem",
                                ),
                                background="white",
                                border_radius="12px",
                                padding="1.5rem",
                                box_shadow="0 2px 10px rgba(0,0,0,0.06)",
                                width="100%",
                            ),
                            # Sección 3: Pago
                            rx.box(
                                rx.text(
                                    "3. Método de Pago",
                                    font_size="1.1rem",
                                    font_weight="700",
                                    color="#0C4A6E",
                                    border_left="4px solid #0C4A6E",
                                    padding_left="0.75rem",
                                ),
                                rx.hstack(
                                    metodo_btn("tarjeta", "💳", "Tarjeta"),
                                    metodo_btn("transferencia", "🏦", "Transferencia"),
                                    metodo_btn("efectivo", "💵", "Efectivo"),
                                    spacing="3",
                                    flex_wrap="wrap",
                                    margin_top="1rem",
                                ),
                                background="white",
                                border_radius="12px",
                                padding="1.5rem",
                                box_shadow="0 2px 10px rgba(0,0,0,0.06)",
                                width="100%",
                            ),
                            rx.cond(
                                ReservasState.error != "",
                                rx.text(ReservasState.error, color="red", font_size="0.9rem"),
                                rx.box(),
                            ),
                            rx.button(
                                rx.cond(
                                    ReservasState.enviando,
                                    rx.spinner(size="2"),
                                    rx.text("Confirmar Reserva →"),
                                ),
                                on_click=ReservasState.enviar_reserva,
                                disabled=ReservasState.enviando,
                                background="#0C4A6E",
                                color="white",
                                width="100%",
                                height="54px",
                                font_size="1.1rem",
                                font_weight="700",
                                border_radius="10px",
                                cursor="pointer",
                                border="none",
                            ),
                            spacing="4",
                            flex="2",
                            min_width="0",
                        ),
                        # Panel resumen
                        rx.box(
                            rx.vstack(
                                rx.text(
                                    "Resumen de tu Reserva",
                                    font_weight="700",
                                    font_size="1rem",
                                    color="#0F172A",
                                ),
                                rx.divider(),
                                rx.text(
                                    ReservasState.oferta_nombre,
                                    font_weight="600",
                                    color="#1E293B",
                                ),
                                rx.text(
                                    ReservasState.oferta_descripcion,
                                    color="#64748B",
                                    font_size="0.85rem",
                                ),
                                rx.divider(),
                                rx.hstack(
                                    rx.text("Precio/persona:", color="#64748B", font_size="0.9rem"),
                                    rx.spacer(),
                                    rx.text(ReservasState.oferta_precio, font_weight="600"),
                                    width="100%",
                                ),
                                rx.hstack(
                                    rx.text("Personas:", color="#64748B", font_size="0.9rem"),
                                    rx.spacer(),
                                    rx.text(ReservasState.num_personas, font_weight="600"),
                                    width="100%",
                                ),
                                rx.divider(),
                                rx.hstack(
                                    rx.text("Total:", font_weight="700"),
                                    rx.spacer(),
                                    rx.text(
                                        ReservasState.monto_total,
                                        font_weight="800",
                                        font_size="1.3rem",
                                        color="#0C4A6E",
                                    ),
                                    width="100%",
                                ),
                                rx.box(
                                    rx.text("🔒 Pago 100% seguro", font_size="0.8rem", color="#059669"),
                                    rx.text("✅ Confirmación por email", font_size="0.8rem", color="#059669"),
                                    rx.text("📞 Soporte 24/7", font_size="0.8rem", color="#059669"),
                                    background="#ECFDF5",
                                    padding="1rem",
                                    border_radius="8px",
                                    width="100%",
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
                            min_width="260px",
                        ),
                        flex_wrap=["wrap", "wrap", "nowrap"],
                        gap="2rem",
                        max_width="1200px",
                        margin="0 auto",
                        padding=["2rem 1.5rem", "3rem 2rem"],
                        align="start",
                        width="100%",
                    ),
                    background="#F8FAFC",
                    width="100%",
                ),
                on_mount=ReservasState.cargar_datos_iniciales,
                width="100%",
            ),
        ),
        footer(),
        width="100%",
        min_height="100vh",
        font_family="'Inter', system-ui, sans-serif",
    )
