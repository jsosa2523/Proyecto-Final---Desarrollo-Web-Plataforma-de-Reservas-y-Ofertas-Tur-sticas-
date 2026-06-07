import reflex as rx

from turistica_rd.pages.inicio      import inicio_page
from turistica_rd.pages.descripcion import descripcion_page
from turistica_rd.pages.reservas    import reservas_page

app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
    ],
)

app.add_page(inicio_page,      route="/",            title="TuristicaRD - Inicio")
app.add_page(descripcion_page, route="/descripcion", title="TuristicaRD - Descripción")
app.add_page(reservas_page,    route="/reservas",    title="TuristicaRD - Reservar")
