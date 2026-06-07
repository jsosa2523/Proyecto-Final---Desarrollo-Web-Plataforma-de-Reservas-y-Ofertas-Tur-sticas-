-- ============================================================
--  TuristicaRD — Datos de Ejemplo (Seed)
--  Archivo: database/seed.sql
-- ============================================================

USE turistica_db;

-- ------------------------------------------------------------
-- Destinos
-- ------------------------------------------------------------
INSERT INTO destinos (nombre, region) VALUES
  ('Punta Cana',   'Este'),
  ('Santo Domingo','Ozama'),
  ('Samaná',       'Nordeste'),
  ('Puerto Plata',  'Norte'),
  ('Jarabacoa',    'Cibao');

-- ------------------------------------------------------------
-- Ofertas Turísticas
-- ------------------------------------------------------------
INSERT INTO ofertas_turisticas
  (destino_id, nombre, descripcion, descripcion_larga, precio, precio_original,
   duracion_dias, imagen_url, disponible, destacada, itinerario, incluye)
VALUES
(1,
 'Punta Cana Todo Incluido',
 '5 días en el paraíso caribeño con playas de arena blanca y aguas cristalinas.',
 'Disfruta de los mejores resorts de Punta Cana con todo incluido. Piscinas, playa, gastronomía internacional y entretenimiento sin límites.',
 45000.00, 55000.00, 5,
 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800',
 TRUE, TRUE,
 '[{"dia":1,"titulo":"Llegada y bienvenida","descripcion":"Recibimiento en el aeropuerto y traslado al resort"},{"dia":2,"titulo":"Playa Bávaro","descripcion":"Día libre en la playa con deportes acuáticos"},{"dia":3,"titulo":"Isla Saona","descripcion":"Excursión en catamarán a Isla Saona"},{"dia":4,"titulo":"Spa y Descanso","descripcion":"Día de spa y actividades recreativas"},{"dia":5,"titulo":"Regreso","descripcion":"Check-out y traslado al aeropuerto"}]',
 '["Traslado aeropuerto-hotel","5 noches en habitación estándar","Alimentación todo incluido","Excursión Isla Saona","Seguro de viaje"]'
),
(3,
 'Samaná y Las Terrazas',
 '4 días rodeado de naturaleza, ballenas y paisajes tropicales únicos.',
 'Samaná es uno de los destinos más hermosos de República Dominicana. Observa ballenas jorobadas (temporada enero-marzo) y descubre cascadas impresionantes.',
 38000.00, NULL, 4,
 'https://images.unsplash.com/photo-1559827291-72ee739d0d9a?w=800',
 TRUE, TRUE,
 '[{"dia":1,"titulo":"Llegada a Samaná","descripcion":"Traslado y primer recorrido por el malecón"},{"dia":2,"titulo":"Tour Ballenas","descripcion":"Excursión marítima de avistamiento de ballenas"},{"dia":3,"titulo":"El Limón","descripcion":"Caminata hasta la cascada El Limón (40m de altura)"},{"dia":4,"titulo":"Playa Rincón","descripcion":"Visita a una de las mejores playas del Caribe"}]',
 '["Traslado ida y vuelta","4 noches en hotel boutique","Desayuno incluido","Tour de ballenas","Guía local certificado"]'
),
(5,
 'Jarabacoa Aventura',
 '3 días de naturaleza, rafting y senderismo en la montaña dominicana.',
 'Escapa del calor y sumérgete en la frescura de Jarabacoa. Rafting en el Río Yaque del Norte, tirolesa, senderismo y gastronomía local.',
 22000.00, 27000.00, 3,
 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800',
 TRUE, FALSE,
 '[{"dia":1,"titulo":"Llegada y senderismo","descripcion":"Llegada a Jarabacoa y caminata al Salto Baiguate"},{"dia":2,"titulo":"Rafting","descripcion":"Día completo de rafting en el Río Yaque del Norte"},{"dia":3,"titulo":"Tirolesa y regreso","descripcion":"Tirolesa sobre el cañón y regreso"}]',
 '["Transporte desde Santo Domingo","3 noches en eco-lodge","Todas las comidas","Equipo de seguridad","Instructor certificado"]'
),
(4,
 'Puerto Plata Colonial',
 '4 días explorando la Novia del Atlántico: fortaleza, teleférico y playas.',
 'Puerto Plata combina historia colonial, naturaleza y playas paradisíacas. Visita la Fortaleza San Felipe, sube al Pico Isabel de Torres y relájate en Playa Dorada.',
 31500.00, NULL, 4,
 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800',
 TRUE, FALSE,
 '[{"dia":1,"titulo":"Llegada","descripcion":"Recibimiento y recorrido colonial por el centro histórico"},{"dia":2,"titulo":"Teleférico","descripcion":"Teleférico al Pico Isabel de Torres y jardín botánico"},{"dia":3,"titulo":"Playa Dorada","descripcion":"Día completo en las playas de Playa Dorada"},{"dia":4,"titulo":"Fortaleza y regreso","descripcion":"Visita Fortaleza San Felipe y regreso"}]',
 '["Traslado","4 noches en hotel 3 estrellas","Desayuno y cena","Ticket teleférico","Tour colonial guiado"]'
);
