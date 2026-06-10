USE DB_CUIDADO_ANIMAL;

-- Vista: detalle completo de mascotas
CREATE OR REPLACE VIEW V_PETS_FULL AS
SELECT
    p.pet_id,
    p.pet_name,
    p.pet_birthdate,
    p.pet_sex,
    p.pet_color,
    p.pet_weight,
    p.pet_status,
    p.pet_date,
    o.owner_id,
    CONCAT(o.owner_name, ' ', o.owner_first_surname) AS owner_full_name,
    o.owner_phone,
    o.owner_email,
    s.species_id,
    s.species_name,
    b.breed_id,
    b.breed_name
FROM PETS AS p
INNER JOIN OWNERS AS o ON p.owner_id = o.owner_id
INNER JOIN SPECIES AS s ON p.species_id = s.species_id
INNER JOIN BREEDS AS b ON p.breed_id = b.breed_id;

-- Vista: historial de vacunaciones por mascota
CREATE OR REPLACE VIEW V_VACCINATIONS_FULL AS
SELECT
    va.vaccination_id,
    va.vaccination_date,
    va.vaccination_next_date,
    va.vaccination_batch,
    va.vaccination_notes,
    p.pet_id,
    p.pet_name,
    s.species_name,
    vac.vaccine_id,
    vac.vaccine_name,
    vac.vaccine_disease,
    vac.vaccine_manufacturer,
    CONCAT(u.user_name, ' ', u.user_first_surname) AS vet_full_name
FROM VACCINATIONS AS va
INNER JOIN PETS AS p ON va.pet_id = p.pet_id
INNER JOIN SPECIES AS s ON p.species_id = s.species_id
INNER JOIN VACCINES AS vac ON va.vaccine_id = vac.vaccine_id
INNER JOIN USERS AS u ON va.user_id = u.user_id;

-- Vista: consultas con información completa
CREATE OR REPLACE VIEW V_CONSULTATIONS_FULL AS
SELECT
    c.consultation_id,
    c.consultation_date,
    c.consultation_weight,
    c.consultation_temperature,
    c.consultation_diagnosis,
    c.consultation_treatment,
    c.consultation_notes,
    p.pet_id,
    p.pet_name,
    s.species_name,
    b.breed_name,
    o.owner_id,
    CONCAT(o.owner_name, ' ', o.owner_first_surname) AS owner_full_name,
    o.owner_phone,
    CONCAT(u.user_name, ' ', u.user_first_surname) AS vet_full_name,
    u.user_id AS vet_id,
    c.appointment_id
FROM CONSULTATIONS AS c
INNER JOIN PETS AS p ON c.pet_id = p.pet_id
INNER JOIN SPECIES AS s ON p.species_id = s.species_id
INNER JOIN BREEDS AS b ON p.breed_id = b.breed_id
INNER JOIN OWNERS AS o ON p.owner_id = o.owner_id
INNER JOIN USERS AS u ON c.user_id = u.user_id;

-- Vista: citas con información completa
CREATE OR REPLACE VIEW V_APPOINTMENTS_FULL AS
SELECT
    a.appointment_id,
    a.appointment_date,
    a.appointment_time,
    a.appointment_reason,
    a.appointment_status,
    a.appointment_date_created,
    p.pet_id,
    p.pet_name,
    s.species_name,
    o.owner_id,
    CONCAT(o.owner_name, ' ', o.owner_first_surname) AS owner_full_name,
    o.owner_phone,
    CONCAT(u.user_name, ' ', u.user_first_surname) AS vet_full_name,
    u.user_id AS vet_id
FROM APPOINTMENTS AS a
INNER JOIN PETS AS p ON a.pet_id = p.pet_id
INNER JOIN SPECIES AS s ON p.species_id = s.species_id
INNER JOIN OWNERS AS o ON p.owner_id = o.owner_id
INNER JOIN USERS AS u ON a.user_id = u.user_id;

-- Vista: recetas con detalle de medicamentos
CREATE OR REPLACE VIEW V_PRESCRIPTIONS_FULL AS
SELECT
    pr.prescription_id,
    pr.prescription_date,
    pr.prescription_notes,
    c.consultation_id,
    c.consultation_date,
    p.pet_id,
    p.pet_name,
    CONCAT(o.owner_name, ' ', o.owner_first_surname) AS owner_full_name,
    CONCAT(u.user_name, ' ', u.user_first_surname) AS vet_full_name,
    pd.detail_id,
    m.medication_name,
    m.medication_presentation,
    m.medication_unit,
    pd.detail_dose,
    pd.detail_frequency,
    pd.detail_duration,
    pd.detail_instructions
FROM PRESCRIPTIONS AS pr
INNER JOIN CONSULTATIONS AS c ON pr.consultation_id = c.consultation_id
INNER JOIN PETS AS p ON c.pet_id = p.pet_id
INNER JOIN OWNERS AS o ON p.owner_id = o.owner_id
INNER JOIN USERS AS u ON c.user_id = u.user_id
INNER JOIN PRESCRIPTION_DETAILS AS pd ON pr.prescription_id = pd.prescription_id
INNER JOIN MEDICATIONS AS m ON pd.medication_id = m.medication_id;
