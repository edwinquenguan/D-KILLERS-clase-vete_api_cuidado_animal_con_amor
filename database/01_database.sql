SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
SET collation_connection = utf8mb4_unicode_ci;

DROP DATABASE IF EXISTS DB_CUIDADO_ANIMAL;

CREATE SCHEMA DB_CUIDADO_ANIMAL DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE DB_CUIDADO_ANIMAL;

-- -----------------------------------------------------
-- Table ROLES
-- -----------------------------------------------------
CREATE TABLE ROLES (
  rol_id INT NOT NULL AUTO_INCREMENT,
  rol_name VARCHAR(100) NOT NULL,
  PRIMARY KEY (rol_id),
  UNIQUE INDEX rol_id_UNIQUE (rol_id ASC)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table CITIES
-- -----------------------------------------------------
CREATE TABLE CITIES (
  city_id INT NOT NULL AUTO_INCREMENT,
  city_name TEXT NOT NULL,
  PRIMARY KEY (city_id),
  UNIQUE INDEX city_id_UNIQUE (city_id ASC)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table USERS  (personal de la clínica)
-- -----------------------------------------------------
CREATE TABLE USERS (
  rol_id INT NOT NULL,
  user_id INT NOT NULL AUTO_INCREMENT,
  user_name VARCHAR(255) NOT NULL,
  user_first_surname VARCHAR(255) NOT NULL,
  user_second_surname VARCHAR(255) NOT NULL,
  user_phone VARCHAR(255) NOT NULL,
  user_email VARCHAR(255) NOT NULL,
  user_address VARCHAR(255) NOT NULL,
  user_password VARCHAR(255) NOT NULL,
  user_city INT NOT NULL,
  user_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  user_status INT NOT NULL DEFAULT 2 COMMENT '1 = deshabilitado, 2 = activo',
  PRIMARY KEY (user_id),
  UNIQUE INDEX users_id_UNIQUE (user_id ASC),
  INDEX fk_rol_users_idx (rol_id ASC),
  CONSTRAINT fk_rol_user
    FOREIGN KEY (rol_id) REFERENCES ROLES (rol_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_city_user
    FOREIGN KEY (user_city) REFERENCES CITIES (city_id)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table OWNERS  (propietarios de mascotas)
-- -----------------------------------------------------
CREATE TABLE OWNERS (
  owner_id INT NOT NULL AUTO_INCREMENT,
  owner_name VARCHAR(255) NOT NULL,
  owner_first_surname VARCHAR(255) NOT NULL,
  owner_second_surname VARCHAR(255) NOT NULL,
  owner_phone VARCHAR(255) NOT NULL,
  owner_email VARCHAR(255) NOT NULL,
  owner_address VARCHAR(255) NOT NULL,
  owner_city INT NOT NULL,
  owner_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  owner_status INT NOT NULL DEFAULT 2 COMMENT '1 = deshabilitado, 2 = activo',
  PRIMARY KEY (owner_id),
  UNIQUE INDEX owner_id_UNIQUE (owner_id ASC),
  CONSTRAINT fk_owner_city
    FOREIGN KEY (owner_city) REFERENCES CITIES (city_id)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table SPECIES  (especies animales)
-- -----------------------------------------------------
CREATE TABLE SPECIES (
  species_id INT NOT NULL AUTO_INCREMENT,
  species_name VARCHAR(100) NOT NULL,
  species_status INT NOT NULL DEFAULT 2 COMMENT '1 = deshabilitada, 2 = activa',
  PRIMARY KEY (species_id),
  UNIQUE INDEX species_id_UNIQUE (species_id ASC)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table BREEDS  (razas por especie)
-- -----------------------------------------------------
CREATE TABLE BREEDS (
  breed_id INT NOT NULL AUTO_INCREMENT,
  species_id INT NOT NULL,
  breed_name VARCHAR(100) NOT NULL,
  breed_status INT NOT NULL DEFAULT 2 COMMENT '1 = deshabilitada, 2 = activa',
  PRIMARY KEY (breed_id),
  UNIQUE INDEX breed_id_UNIQUE (breed_id ASC),
  INDEX fk_breed_species_idx (species_id ASC),
  CONSTRAINT fk_breed_species
    FOREIGN KEY (species_id) REFERENCES SPECIES (species_id)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table PETS  (mascotas / pacientes)
-- -----------------------------------------------------
CREATE TABLE PETS (
  pet_id INT NOT NULL AUTO_INCREMENT,
  owner_id INT NOT NULL,
  species_id INT NOT NULL,
  breed_id INT NOT NULL,
  pet_name VARCHAR(255) NOT NULL,
  pet_birthdate DATE NOT NULL,
  pet_sex ENUM('M', 'F') NOT NULL,
  pet_color VARCHAR(100) NOT NULL,
  pet_weight DECIMAL(5,2) NOT NULL COMMENT 'Peso en kilogramos',
  pet_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  pet_status INT NOT NULL DEFAULT 2 COMMENT '1 = inactivo, 2 = activo',
  PRIMARY KEY (pet_id),
  UNIQUE INDEX pet_id_UNIQUE (pet_id ASC),
  INDEX fk_pet_owner_idx (owner_id ASC),
  INDEX fk_pet_species_idx (species_id ASC),
  INDEX fk_pet_breed_idx (breed_id ASC),
  CONSTRAINT fk_pet_owner
    FOREIGN KEY (owner_id) REFERENCES OWNERS (owner_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_pet_species
    FOREIGN KEY (species_id) REFERENCES SPECIES (species_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_pet_breed
    FOREIGN KEY (breed_id) REFERENCES BREEDS (breed_id)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table APPOINTMENTS  (citas)
-- -----------------------------------------------------
CREATE TABLE APPOINTMENTS (
  appointment_id INT NOT NULL AUTO_INCREMENT,
  pet_id INT NOT NULL,
  user_id INT NOT NULL COMMENT 'Veterinario asignado',
  appointment_date DATE NOT NULL,
  appointment_time TIME NOT NULL,
  appointment_reason VARCHAR(500) NOT NULL,
  appointment_date_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  appointment_status INT NOT NULL DEFAULT 2 COMMENT '1 = cancelada, 2 = pendiente, 3 = atendida',
  PRIMARY KEY (appointment_id),
  UNIQUE INDEX appointment_id_UNIQUE (appointment_id ASC),
  INDEX fk_appointment_pet_idx (pet_id ASC),
  INDEX fk_appointment_user_idx (user_id ASC),
  CONSTRAINT fk_appointment_pet
    FOREIGN KEY (pet_id) REFERENCES PETS (pet_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_appointment_user
    FOREIGN KEY (user_id) REFERENCES USERS (user_id)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table CONSULTATIONS  (consultas médicas)
-- -----------------------------------------------------
CREATE TABLE CONSULTATIONS (
  consultation_id INT NOT NULL AUTO_INCREMENT,
  pet_id INT NOT NULL,
  user_id INT NOT NULL COMMENT 'Veterinario que atiende',
  appointment_id INT NULL COMMENT 'Cita origen, puede ser NULL si es urgencia',
  consultation_weight DECIMAL(5,2) NOT NULL COMMENT 'Peso registrado en consulta (kg)',
  consultation_temperature DECIMAL(4,1) NOT NULL COMMENT 'Temperatura en °C',
  consultation_diagnosis TEXT NOT NULL,
  consultation_treatment TEXT NOT NULL,
  consultation_notes TEXT NULL,
  consultation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (consultation_id),
  UNIQUE INDEX consultation_id_UNIQUE (consultation_id ASC),
  INDEX fk_consultation_pet_idx (pet_id ASC),
  INDEX fk_consultation_user_idx (user_id ASC),
  INDEX fk_consultation_appointment_idx (appointment_id ASC),
  CONSTRAINT fk_consultation_pet
    FOREIGN KEY (pet_id) REFERENCES PETS (pet_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_consultation_user
    FOREIGN KEY (user_id) REFERENCES USERS (user_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_consultation_appointment
    FOREIGN KEY (appointment_id) REFERENCES APPOINTMENTS (appointment_id)
    ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table VACCINES  (catálogo de vacunas)
-- -----------------------------------------------------
CREATE TABLE VACCINES (
  vaccine_id INT NOT NULL AUTO_INCREMENT,
  species_id INT NOT NULL COMMENT 'Especie para la que aplica',
  vaccine_name VARCHAR(255) NOT NULL,
  vaccine_disease VARCHAR(255) NOT NULL COMMENT 'Enfermedad que previene',
  vaccine_manufacturer VARCHAR(255) NOT NULL,
  vaccine_status INT NOT NULL DEFAULT 2 COMMENT '1 = descontinuada, 2 = activa',
  PRIMARY KEY (vaccine_id),
  UNIQUE INDEX vaccine_id_UNIQUE (vaccine_id ASC),
  INDEX fk_vaccine_species_idx (species_id ASC),
  CONSTRAINT fk_vaccine_species
    FOREIGN KEY (species_id) REFERENCES SPECIES (species_id)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table VACCINATIONS  (aplicaciones de vacunas)
-- -----------------------------------------------------
CREATE TABLE VACCINATIONS (
  vaccination_id INT NOT NULL AUTO_INCREMENT,
  pet_id INT NOT NULL,
  vaccine_id INT NOT NULL,
  user_id INT NOT NULL COMMENT 'Veterinario que aplica',
  vaccination_date DATE NOT NULL,
  vaccination_next_date DATE NOT NULL COMMENT 'Fecha de próximo refuerzo',
  vaccination_batch VARCHAR(100) NOT NULL COMMENT 'Número de lote',
  vaccination_notes VARCHAR(500) NULL,
  PRIMARY KEY (vaccination_id),
  UNIQUE INDEX vaccination_id_UNIQUE (vaccination_id ASC),
  INDEX fk_vaccination_pet_idx (pet_id ASC),
  INDEX fk_vaccination_vaccine_idx (vaccine_id ASC),
  INDEX fk_vaccination_user_idx (user_id ASC),
  CONSTRAINT fk_vaccination_pet
    FOREIGN KEY (pet_id) REFERENCES PETS (pet_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_vaccination_vaccine
    FOREIGN KEY (vaccine_id) REFERENCES VACCINES (vaccine_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_vaccination_user
    FOREIGN KEY (user_id) REFERENCES USERS (user_id)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table MEDICATIONS  (catálogo de medicamentos)
-- -----------------------------------------------------
CREATE TABLE MEDICATIONS (
  medication_id INT NOT NULL AUTO_INCREMENT,
  medication_name VARCHAR(255) NOT NULL,
  medication_presentation VARCHAR(100) NOT NULL COMMENT 'Tableta, Jarabe, Inyectable, etc.',
  medication_unit VARCHAR(50) NOT NULL COMMENT 'mg, ml, UI, etc.',
  medication_status INT NOT NULL DEFAULT 2 COMMENT '1 = descontinuado, 2 = activo',
  PRIMARY KEY (medication_id),
  UNIQUE INDEX medication_id_UNIQUE (medication_id ASC)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table PRESCRIPTIONS  (recetas médicas)
-- -----------------------------------------------------
CREATE TABLE PRESCRIPTIONS (
  prescription_id INT NOT NULL AUTO_INCREMENT,
  consultation_id INT NOT NULL,
  prescription_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  prescription_notes TEXT NULL,
  PRIMARY KEY (prescription_id),
  UNIQUE INDEX prescription_id_UNIQUE (prescription_id ASC),
  INDEX fk_prescription_consultation_idx (consultation_id ASC),
  CONSTRAINT fk_prescription_consultation
    FOREIGN KEY (consultation_id) REFERENCES CONSULTATIONS (consultation_id)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table PRESCRIPTION_DETAILS  (detalle de receta)
-- -----------------------------------------------------
CREATE TABLE PRESCRIPTION_DETAILS (
  detail_id INT NOT NULL AUTO_INCREMENT,
  prescription_id INT NOT NULL,
  medication_id INT NOT NULL,
  detail_dose VARCHAR(100) NOT NULL COMMENT 'Dosis por toma ej: 5mg',
  detail_frequency VARCHAR(100) NOT NULL COMMENT 'Frecuencia ej: Cada 8 horas',
  detail_duration VARCHAR(100) NOT NULL COMMENT 'Duración ej: 7 días',
  detail_instructions TEXT NULL,
  PRIMARY KEY (detail_id),
  UNIQUE INDEX detail_id_UNIQUE (detail_id ASC),
  INDEX fk_detail_prescription_idx (prescription_id ASC),
  INDEX fk_detail_medication_idx (medication_id ASC),
  CONSTRAINT fk_detail_prescription
    FOREIGN KEY (prescription_id) REFERENCES PRESCRIPTIONS (prescription_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_detail_medication
    FOREIGN KEY (medication_id) REFERENCES MEDICATIONS (medication_id)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;
