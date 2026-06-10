SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
SET collation_connection = utf8mb4_unicode_ci;

USE DB_CUIDADO_ANIMAL;

-- Roles
INSERT INTO ROLES VALUES
(null, 'Admin'),
(null, 'Veterinario'),
(null, 'Recepcionista');

-- Ciudades
INSERT INTO CITIES VALUES
(null, 'Bogotá'),
(null, 'Medellín'),
(null, 'Cali'),
(null, 'Barranquilla'),
(null, 'Cartagena'),
(null, 'Bucaramanga');

-- Usuarios (personal de la clínica) — contraseñas hasheadas con bcrypt
-- Admin
INSERT INTO USERS VALUES
(1, null, 'Laura', 'Gómez', 'Pérez', '3001112233', 'admin@cuidadoanimal.com', 'Calle 10 #20-30', '$2b$12$hmREs4WG7S0OOiUUCJnDs.ON2K5kgzEga8PC64yd9PLDpphJg/5MO', 1, '2026-01-01', 2);

-- Veterinarios
INSERT INTO USERS VALUES
(2, null, 'Andrés', 'Martínez', 'Ruiz', '3104445566', 'andres.martinez@cuidadoanimal.com', 'Carrera 15 #8-44', '$2b$12$OXu8PHeYRlPCe52XUSoB6eYOs9ZpL4V6izZ16sxF9nOzDTu/HbVm2', 1, '2026-01-05', 2),
(2, null, 'Camila', 'Torres', 'Vargas', '3117778899', 'camila.torres@cuidadoanimal.com', 'Calle 50 #22-10', '$2b$12$xxt/aCQt7oaPoG8N9GYYNO3N7EJnhKq4guyM2esyM/ALk.R8e4n6a', 1, '2026-01-10', 2),
(2, null, 'Felipe', 'Rodríguez', 'Castro', '3129990011', 'felipe.rodriguez@cuidadoanimal.com', 'Av. El Parque #5-12', '$2b$12$c6eRLMsX5qdGRWILiv2W4O2su6SL3luIF03TX2B44uHPRF6owu9cS', 1, '2026-02-01', 2);

-- Recepcionistas
INSERT INTO USERS VALUES
(3, null, 'Sofía', 'Herrera', 'Mora', '3151234567', 'sofia.herrera@cuidadoanimal.com', 'Cra 30 #15-20', '$2b$12$nw56lZgJS8WPf3/1r/G52ejfUyGxP2n13Jq8GiiRtXJw3IpLwOcYC', 1, '2026-01-08', 2),
(3, null, 'Diego', 'Salazar', 'Ríos', '3163456789', 'diego.salazar@cuidadoanimal.com', 'Cl. 100 #45-12', '$2b$12$SE/lNU.uOFSwZ1sSH3Nbvux1FPoJ3c.HtR1IdG5dfERJmgvwWXyl2', 1, '2026-01-15', 2);

-- Propietarios
INSERT INTO OWNERS VALUES
(null, 'Juan', 'Pérez', 'García', '3004567890', 'juan.perez@gmail.com', 'Calle 123 #45-67', 1, '2026-01-12', 2),
(null, 'María', 'López', 'Rodríguez', '3112345678', 'maria.lopez@gmail.com', 'Carrera 10 #20-30', 1, '2026-01-15', 2),
(null, 'Carlos', 'García', 'Moreno', '3121112233', 'carlos.garcia@yahoo.com', 'Calle 45 #12-30', 2, '2026-01-20', 2),
(null, 'Ana', 'Ramírez', 'Torres', '3134445566', 'ana.ramirez@hotmail.com', 'Av. Siempre Viva 742', 1, '2026-01-22', 2),
(null, 'Pedro', 'Herrera', 'Suárez', '3147778899', 'pedro.herrera@gmail.com', 'Transv. 56 #34-90', 3, '2026-02-01', 2),
(null, 'Valentina', 'Cárdenas', 'Prieto', '3159990011', 'valentina.cardenas@gmail.com', 'Zona Industrial 4', 1, '2026-02-05', 2),
(null, 'Javier', 'Morales', 'Rincón', '3168889900', 'javier.morales@gmail.com', 'Cl. 80 #10-55', 2, '2026-02-10', 2),
(null, 'Sandra', 'Fernández', 'Quintero', '3172223344', 'sandra.fernandez@gmail.com', 'Carrera 15 #8-44', 1, '2026-02-15', 2),
(null, 'Luisa', 'Rojas', 'Bedoya', '3185556677', 'luisa.rojas@gmail.com', 'Cl. 30 #22-18', 4, '2026-03-01', 2),
(null, 'Miguel', 'Castro', 'Salazar', '3193334455', 'miguel.castro@gmail.com', 'Cra 20 #5-18', 1, '2026-03-05', 2);

-- Especies
INSERT INTO SPECIES VALUES
(null, 'Perro', 2),
(null, 'Gato', 2),
(null, 'Conejo', 2),
(null, 'Hámster', 2),
(null, 'Ave', 2),
(null, 'Reptil', 2);

-- Razas (por especie)
-- Perros (species_id = 1)
INSERT INTO BREEDS VALUES
(null, 1, 'Labrador Retriever', 2),
(null, 1, 'Bulldog Francés', 2),
(null, 1, 'Golden Retriever', 2),
(null, 1, 'Pastor Alemán', 2),
(null, 1, 'Beagle', 2),
(null, 1, 'Poodle', 2),
(null, 1, 'Chihuahua', 2),
(null, 1, 'Mestizo', 2);

-- Gatos (species_id = 2)
INSERT INTO BREEDS VALUES
(null, 2, 'Persa', 2),
(null, 2, 'Siamés', 2),
(null, 2, 'Maine Coon', 2),
(null, 2, 'Ragdoll', 2),
(null, 2, 'Bengalí', 2),
(null, 2, 'Mestizo', 2);

-- Conejos (species_id = 3)
INSERT INTO BREEDS VALUES
(null, 3, 'Holland Lop', 2),
(null, 3, 'Mini Rex', 2),
(null, 3, 'Angora', 2);

-- Hámsters (species_id = 4)
INSERT INTO BREEDS VALUES
(null, 4, 'Sirio', 2),
(null, 4, 'Ruso', 2);

-- Aves (species_id = 5)
INSERT INTO BREEDS VALUES
(null, 5, 'Periquito', 2),
(null, 5, 'Canario', 2),
(null, 5, 'Loro', 2);

-- Mascotas
INSERT INTO PETS VALUES
(null, 1, 1, 1, 'Toby', '2021-03-15', 'M', 'Amarillo', 28.50, '2026-01-12', 2),
(null, 2, 2, 9, 'Mimi', '2020-07-22', 'F', 'Blanco', 4.20, '2026-01-15', 2),
(null, 3, 1, 4, 'Rex', '2019-11-10', 'M', 'Negro con café', 32.80, '2026-01-20', 2),
(null, 4, 2, 10, 'Luna', '2022-05-01', 'F', 'Gris', 3.80, '2026-01-22', 2),
(null, 5, 1, 6, 'Max', '2023-02-18', 'M', 'Blanco', 5.50, '2026-02-01', 2),
(null, 6, 2, 14, 'Nube', '2021-09-30', 'F', 'Naranja', 4.00, '2026-02-05', 2),
(null, 7, 1, 2, 'Bruno', '2020-12-25', 'M', 'Atigrado blanco y negro', 12.30, '2026-02-10', 2),
(null, 8, 3, 15, 'Coco', '2022-08-14', 'F', 'Marrón', 2.10, '2026-02-15', 2),
(null, 9, 5, 22, 'Piolín', '2021-04-05', 'M', 'Amarillo', 0.08, '2026-03-01', 2),
(null, 10, 1, 3, 'Rocky', '2022-06-20', 'M', 'Dorado', 29.00, '2026-03-05', 2);

-- Catálogo de vacunas
-- Para perros (species_id = 1)
INSERT INTO VACCINES VALUES
(null, 1, 'Moquillo Canino', 'Moquillo (Distemper)', 'MSD Animal Health', 2),
(null, 1, 'Parvovirus Canino', 'Parvovirus', 'Boehringer Ingelheim', 2),
(null, 1, 'Rabia Canina', 'Rabia', 'Zoetis', 2),
(null, 1, 'Hepatitis Infecciosa', 'Hepatitis infecciosa canina', 'MSD Animal Health', 2),
(null, 1, 'Polivalente Canina (DHPPi)', 'Distemper, Hepatitis, Parvo, Parainfluenza', 'Virbac', 2),
(null, 1, 'Leptospirosis', 'Leptospirosis', 'Zoetis', 2);

-- Para gatos (species_id = 2)
INSERT INTO VACCINES VALUES
(null, 2, 'Trivalente Felina (FVRCP)', 'Rinotraqueítis, Calicivirus, Panleucopenia', 'Zoetis', 2),
(null, 2, 'Rabia Felina', 'Rabia', 'Boehringer Ingelheim', 2),
(null, 2, 'Leucemia Felina (FeLV)', 'Leucemia viral felina', 'MSD Animal Health', 2);

-- Para conejos (species_id = 3)
INSERT INTO VACCINES VALUES
(null, 3, 'Mixomatosis', 'Mixomatosis', 'MSD Animal Health', 2),
(null, 3, 'Enfermedad Hemorrágica Viral', 'VHD/RHD', 'Hipra', 2);

-- Catálogo de medicamentos
INSERT INTO MEDICATIONS VALUES
(null, 'Amoxicilina', 'Tableta', 'mg', 2),
(null, 'Metronidazol', 'Tableta', 'mg', 2),
(null, 'Ivermectina', 'Inyectable', 'ml', 2),
(null, 'Meloxicam', 'Tableta', 'mg', 2),
(null, 'Prednisolona', 'Tableta', 'mg', 2),
(null, 'Enrofloxacina', 'Tableta', 'mg', 2),
(null, 'Omeprazol', 'Cápsula', 'mg', 2),
(null, 'Furosemida', 'Tableta', 'mg', 2),
(null, 'Enalapril', 'Tableta', 'mg', 2),
(null, 'Cefalexina', 'Jarabe', 'ml', 2),
(null, 'Dexametasona', 'Inyectable', 'ml', 2),
(null, 'Tramadol', 'Tableta', 'mg', 2);

-- Citas
INSERT INTO APPOINTMENTS VALUES
(null, 1, 2, '2026-01-15', '09:00:00', 'Revisión general anual', '2026-01-12', 3),
(null, 2, 3, '2026-01-18', '10:30:00', 'Vacunación trivalente', '2026-01-15', 3),
(null, 3, 2, '2026-01-22', '11:00:00', 'Control de peso y dieta', '2026-01-20', 3),
(null, 4, 4, '2026-01-25', '08:30:00', 'Tos persistente', '2026-01-22', 3),
(null, 5, 2, '2026-02-05', '14:00:00', 'Desparasitación', '2026-02-01', 3),
(null, 6, 3, '2026-02-08', '15:30:00', 'Revisión dental', '2026-02-05', 3),
(null, 7, 4, '2026-02-12', '09:00:00', 'Alergia en piel', '2026-02-10', 2),
(null, 8, 2, '2026-02-18', '10:00:00', 'Revisión post operatoria', '2026-02-15', 2),
(null, 9, 3, '2026-03-03', '11:30:00', 'Pérdida de plumas', '2026-03-01', 2),
(null, 10, 4, '2026-03-07', '08:00:00', 'Cojera miembro posterior', '2026-03-05', 2);

-- Consultas
INSERT INTO CONSULTATIONS VALUES
(null, 1, 2, 1, 29.20, 38.5, 'Animal en buen estado general. Sin alteraciones detectadas.', 'Vitaminas y dieta balanceada recomendada.', 'Próxima cita en 6 meses.', '2026-01-15'),
(null, 2, 3, 2, 4.10, 38.2, 'Gata sana. Se aplica vacuna trivalente FVRCP.', 'Vacuna aplicada sin reacciones adversas.', null, '2026-01-18'),
(null, 3, 2, 3, 33.50, 38.8, 'Sobrepeso. Dieta hipocalórica recomendada.', 'Reducción de 20% en porciones diarias. Ejercicio diario.', 'Control en 1 mes.', '2026-01-22'),
(null, 4, 4, 4, 3.75, 39.1, 'Infección respiratoria leve.', 'Antibiótico y antiinflamatorio por 7 días.', 'Aislar de otros animales.', '2026-01-25'),
(null, 5, 2, 5, 5.60, 38.3, 'Estado general óptimo. Desparasitación aplicada.', 'Ivermectina inyectable aplicada.', null, '2026-02-05'),
(null, 6, 3, 6, 4.05, 38.0, 'Sarro dental moderado. Limpieza programada.', 'Limpieza dental bajo anestesia programada para próxima semana.', null, '2026-02-08');

-- Vacunaciones
INSERT INTO VACCINATIONS VALUES
(null, 1, 5, 2, '2026-01-15', '2027-01-15', 'LOT-DVH-0045', 'Sin reacciones adversas'),
(null, 2, 7, 3, '2026-01-18', '2027-01-18', 'LOT-TRF-0012', null),
(null, 3, 1, 2, '2026-01-22', '2027-01-22', 'LOT-MOQ-0033', 'Animal algo ansioso pero toleró bien'),
(null, 4, 8, 4, '2026-01-25', '2027-01-25', 'LOT-RAB-0071', null),
(null, 5, 3, 2, '2026-02-05', '2027-02-05', 'LOT-RAB-0072', null),
(null, 2, 9, 3, '2026-02-08', '2027-02-08', 'LOT-FLV-0015', 'Primera dosis FeLV');

-- Recetas
INSERT INTO PRESCRIPTIONS VALUES
(null, 4, '2026-01-25', 'Mantener abrigada a la mascota durante el tratamiento');

INSERT INTO PRESCRIPTION_DETAILS VALUES
(null, 1, 1, '250mg', 'Cada 12 horas', '7 días', 'Administrar con comida'),
(null, 1, 4, '0.5mg/kg', 'Una vez al día', '5 días', 'No exceder la dosis indicada');

INSERT INTO PRESCRIPTIONS VALUES
(null, 3, '2026-01-22', 'Controlar el peso semanalmente');

INSERT INTO PRESCRIPTION_DETAILS VALUES
(null, 2, 7, '20mg', 'Una vez al día en ayunas', '30 días', 'Administrar 30 minutos antes del desayuno');
