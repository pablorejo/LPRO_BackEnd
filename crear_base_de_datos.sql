DROP DATABASE IF EXISTS  muundoGando;
CREATE DATABASE IF NOT EXISTS muundoGando DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE muundoGando;

CREATE TABLE IF NOT EXISTS usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    correo varchar(50) NOT NULL UNIQUE,
    usu_password varchar(256) NOT NULL,
    nombre varchar(50) NOT NULL,
    apellidos varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO usuario (id, correo, usu_password,nombre,apellidos)
VALUES 
(1, 'pablopiorejoiglesias@gmail.com', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4','Pablo Pío', 'Rejo Iglesias'),
(2, 'carlos@gmail.com', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4','Carlos Fernando', 'Fernandez Deus');


CREATE TABLE IF NOT EXISTS Vaca (
    Numero_pendiente INT NOT NULL,
    IdUsuario INT NOT NULL,
    Fecha_nacimiento DATE NOT NULL,
    idNumeroPendienteMadre INT DEFAULT NULL,
    idUsuarioMadre INT DEFAULT NULL,
    nota TEXT,
    segundos_pastando INT,
    segundos_descansando INT,
    segundos_caminando INT,
    CHECK (Numero_pendiente >= 1000 AND Numero_pendiente <= 9999),
    FOREIGN KEY (IdUsuario) REFERENCES usuario(id) ON DELETE CASCADE ON UPDATE CASCADE,
    -- Establecemos que si se elimina a la madre se pongan a null los valores de la madre y si se actualiza a la madre se actualize tambien al hijo
    -- CONSTRAINT fk_vaca_madre FOREIGN KEY (idNumeroPendienteMadre, idUsuarioMadre) REFERENCES Vaca(Numero_pendiente, IdUsuario) ON DELETE SET NULL ON UPDATE CASCADE,
    PRIMARY KEY (Numero_pendiente, IdUsuario)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- Creamos triggers para que si metemos un idNumeroPendienteMadre mas pequeño de 1000 lo ponga a null
DELIMITER //
CREATE TRIGGER before_vaca_insert
BEFORE INSERT ON Vaca
FOR EACH ROW
BEGIN
    IF NEW.idNumeroPendienteMadre < 1000 THEN
        SET NEW.idNumeroPendienteMadre = NULL;
    END IF;
END;
//
DELIMITER ;


DELIMITER //
CREATE TRIGGER before_vaca_update
BEFORE UPDATE ON Vaca
FOR EACH ROW
BEGIN
    IF NEW.idNumeroPendienteMadre < 1000 THEN
        SET NEW.idNumeroPendienteMadre = NULL;
    END IF;
END;
//
DELIMITER ;


INSERT INTO Vaca (Numero_pendiente, IdUsuario, Fecha_nacimiento, nota, idNumeroPendienteMadre, idUsuarioMadre)
VALUES 
(1001, 1, '2010-01-01', 'Vaca líder del rebaño. Muestra un temperamento calmado y es muy sociable.',null,null),
(1002, 1, '2010-02-01', 'Preferencia por pastos cercanos al estanque. Salud excelente.',null,null),
(1003, 1, '2010-03-01', 'Historial de mastitis. Requiere chequeos veterinarios frecuentes.',1001,1),
(1004, 1, '2010-04-01', 'Recuperada de lesión en pata trasera izquierda. Movilidad completa restaurada.',1001,1),
(1005, 1, '2010-05-01', 'Buena productora de leche. Genética valiosa para futuras crías.',null,null),
(1006, 1, '2010-06-01', 'Sensible a cambios climáticos. Necesita alojamiento especial durante el invierno.',1003,1),
(1007, 1, '2010-07-01', '',1003,1),
(1008, 1, '2010-08-01', 'Madre ejemplar. Ha tenido varios partos sin complicaciones.',null,null),
(1009, 1, '2010-09-01', 'Requiere dieta especial debido a sensibilidades alimenticias.',1008,1),
(1010, 1, '2010-10-01', 'Excelente temperamento. Fácil de manejar durante el ordeño y los chequeos veterinarios.',1008,1);

CREATE TABLE IF NOT EXISTS Enfermedades (
    id_enfermedad_vaca INT AUTO_INCREMENT PRIMARY KEY,
    Numero_pendiente INT NOT NULL,
    IdUsuario INT NOT NULL,
    Medicamento VARCHAR(255) NOT NULL,
    Enfermedad VARCHAR(255),
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    periocidad_en_dias INT NOT NULL,
    nota TEXT,
    CONSTRAINT fk_vaca_enfermedad FOREIGN KEY (Numero_pendiente, IdUsuario) REFERENCES Vaca(Numero_pendiente, IdUsuario) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO Enfermedades (Numero_pendiente,IdUsuario, Medicamento, Enfermedad,fecha_inicio,fecha_fin,periocidad_en_dias,nota)
VALUES 
(1001, 1, 'Paracetamol', 'Gripe', '2024-03-01', '2024-03-20', 5, 'Inicio leve, se observa mejoría con el tratamiento.'),
(1002, 1, 'Paracetamol', 'Gripe', '2024-03-03', '2024-03-23', 5, 'Mantener en observación por posibles recaídas.'),
(1003, 1, 'Paracetamol', 'Gripe', '2024-02-29', '2024-03-10', 5, 'La vaca muestra buen apetito, signo positivo.');

CREATE TABLE IF NOT EXISTS Partos (
    id_vaca_parto INT AUTO_INCREMENT PRIMARY KEY,
    Numero_pendiente INT NOT NULL,
    IdUsuario INT NOT NULL,
    fecha_parto DATE NOT NULL,
    nota TEXT,
    CONSTRAINT fk_vaca_parto FOREIGN KEY (Numero_pendiente, IdUsuario) REFERENCES Vaca(Numero_pendiente, IdUsuario) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


INSERT INTO Partos (Numero_pendiente, IdUsuario, fecha_parto, nota)
VALUES 
(1001, 1, '2024-03-01', 'Parto sin complicaciones. La madre y el ternero están en buen estado.'),
(1002, 1, '2024-03-02', 'Parto asistido. Se observará la recuperación de la madre durante los próximos días.'),
(1003, 1, '2024-03-03', 'Parto natural. Se recomienda supervisión continua del ternero.'),
(1004, 1, '2024-03-04', 'Parto prematuro. El ternero requiere cuidados intensivos.'),
(1005, 1, '2024-03-05', 'Parto con complicaciones menores. Ambos se recuperan satisfactoriamente.'),
(1003, 1, '2024-03-06', 'Parto gemelar exitoso. Se monitoreará el desarrollo de ambos terneros.'),
(1004, 1, '2024-03-07', 'Parto natural bajo observación. Sin incidencias.'),
(1003, 1, '2024-03-08', ''),
(1002, 1, '2024-03-09', 'Se necesitó intervención veterinaria para completar el parto. Recuperación en curso.'),
(1001, 1, '2024-03-10', 'Parto rápido y sin asistencia. Ternero vigoroso y saludable.');


CREATE TABLE IF NOT EXISTS parcela(
    id_parcela INT AUTO_INCREMENT UNIQUE NOT NULL,
    IdUsuario INT NOT NULL,
    nombre_parcela VARCHAR(255) NOT NULL,
    FOREIGN KEY (IdUsuario) REFERENCES usuario(id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (id_parcela, IdUsuario)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO parcela (IdUsuario,nombre_parcela)
VALUES 
(1, "parcela casa"),
(1, "parcela cuvi"),
(1, "parcela jesus"),
(1, "prueba jesus vigo");

CREATE TABLE IF NOT EXISTS gps (
    id_vaca_gps INT AUTO_INCREMENT PRIMARY KEY,
    Numero_pendiente INT NOT NULL,
    IdUsuario INT NOT NULL,
    latitude DOUBLE NOT NULL,
    longitude DOUBLE NOT NULL,
    id_parcela INT,

    tipo VARCHAR(255),
    velocidad DOUBLE,
    anomalia BOOLEAN,
    fuera_del_recinto BOOLEAN,

    rssi DOUBLE,
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_vaca_gps FOREIGN KEY (Numero_pendiente, IdUsuario) REFERENCES Vaca(Numero_pendiente, IdUsuario) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- CREATE TABLE IF NOT EXISTS gps_analizado (
--     id_vaca_gps INT AUTO_INCREMENT PRIMARY KEY,
--     Numero_pendiente INT NOT NULL,
--     IdUsuario INT NOT NULL,
--     latitude DOUBLE NOT NULL,
--     longitude DOUBLE NOT NULL,
--     id_parcela INT,
--     tipo VARCHAR(255),
--     velocidade DOUBLE,
--     anomalia BOOLEAN,
--     fuera_del_recinto BOOLEAN,
--     velocidad_m_s DOUBLE,
--     distancia_a_otras_vacas DOUBLE,
--     rssi DOUBLE,
--     fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
--     CONSTRAINT fk_vaca_gps FOREIGN KEY (Numero_pendiente, IdUsuario) REFERENCES Vaca(Numero_pendiente, IdUsuario) ON DELETE CASCADE ON UPDATE CASCADE
-- ) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS coordenadas (
    id_esquina INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    id_parcela INT NOT NULL,
    latitude DOUBLE NOT NULL,
    longitude DOUBLE NOT NULL,
    FOREIGN KEY (id_parcela) REFERENCES parcela(id_parcela) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- El uno es casa el 2 es cuvi
INSERT INTO coordenadas ( id_parcela, latitude, longitude) VALUES
(1, 42.22259255448751, -7.7482447028160095),
(1, 42.222553573687755, -7.7482423558831215),
(1, 42.22215234316532, -7.7485715970396996),
(1, 42.221494627468, -7.748884409666061),
(1, 42.22124211645043, -7.74941984564066),
(1, 42.22116738094084, -7.749530151486396),
(1, 42.221308410001186, -7.749596200883389),
(1, 42.22169027936151, -7.74977456778288),
(1, 42.221911504312814, -7.749478183686733),
(1, 42.222280707415514, -7.7498047426342955),
(1, 42.22191771151127, -7.750540003180505),
(1, 42.22198524579101, -7.750600352883338),
(1, 42.222033413578735, -7.750500775873661),
(1, 42.22217245440937, -7.750652991235255),
(1, 42.22223427782323, -7.750729098916055),
(1, 42.222440852003956, -7.750732451677322),
(1, 42.22248926772979, -7.750282175838947),
(1, 42.2226518946397, -7.7499985322356215),
(1, 42.222719179849356, -7.74979367852211),
(1, 42.22287882675738, -7.749067470431329),
(1, 42.22298161631033, -7.748790867626667),
(1, 42.22292103504818, -7.7486688271164885),
(1, 42.22286889539073, -7.7485595270991325),
(1, 42.222786464987315, -7.748439833521842),
(1, 42.22270055848854, -7.748388200998306),
(1, 42.222660088045444, -7.748359031975268),
(1, 42.22266828145012, -7.748302705585957),
(2,42.1708749220415 ,  -8.684778213500977),
(2,42.17088784344455 ,  -8.683796525001526),
(2,42.171329902931646 ,  -8.683318421244621),
(2,42.171783638124204 ,   -8.68295531719923),
(2,42.17215164330223 ,  -8.682750463485718),
(2,42.17232210277389 ,  -8.683327473700047),
(2,42.17273135272034 ,  -8.684871755540371),
(2,42.17178438357912 ,   -8.68525430560112),
(3,43.127987152360035 ,  -8.485743217170238), 
(3,43.12846161228289 ,  -8.483846224844456), 
(3,43.12783372899827 ,  -8.483420088887215), 
(3,43.12739107474986 ,  -8.483696691691875), 
(3,43.127008613026995 ,  -8.485622182488441),
(4,42.222715952147226 ,  -8.73375367373228), 
(4,42.222645439228366 ,  -8.73369500041008), 
(4,42.22269335822756 , -8.733584359288216),
(4,42.22275915368536 , -8.733649402856827);


CREATE TABLE IF NOT EXISTS sector(
    id_sector INT AUTO_INCREMENT NOT NULL,
    id_parcela INT NOT NULL UNIQUE,
    IdUsuario INT NOT NULL,
    CONSTRAINT fk_sector_parcela FOREIGN KEY (id_parcela, IdUsuario) REFERENCES parcela(id_parcela, IdUsuario) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (id_sector, id_parcela)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO sector (IdUsuario,id_parcela)
VALUES 
-- (1,2);
(1,2);

CREATE TABLE IF NOT EXISTS coordenadas_sector (
    id_esquina INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    id_sector INT NOT NULL,
    id_parcela INT NOT NULL,
    latitude DOUBLE NOT NULL,
    longitude DOUBLE NOT NULL,
    FOREIGN KEY (id_sector,id_parcela) REFERENCES sector(id_sector,id_parcela) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO coordenadas_sector (id_sector,id_parcela,latitude,longitude)
VALUES 
(1,2,42.1708749220415 ,  -8.684778213500977),
(1,2,42.17088784344455 ,  -8.683796525001526),
(1,2,42.171329902931646 ,  -8.683318421244621),
(1,2,42.171783638124204 ,   -8.68295531719923),
(1,2,42.17215164330223 ,  -8.682750463485718);

-- (1,2,42.1708749220415 ,  -8.684778213500977),
-- (1,2,42.17088784344455 ,  -8.683796525001526),
-- (1,2,42.171329902931646 ,  -8.683318421244621),
-- (1,2,42.171783638124204 ,   -8.68295531719923);





-------------------------------------------------------------------------
-------------------------------------------------------------------------
-------------------------------------------------------------------------
-------------------------------------------------------------------------
-------------------------------- NO USADO -------------------------------
-------------------------------- NO USADO -------------------------------
-------------------------------- NO USADO -------------------------------
-------------------------------- NO USADO -------------------------------
-------------------------------------------------------------------------
-------------------------------------------------------------------------
-------------------------------------------------------------------------
-------------------------------------------------------------------------
-- NO USADAS POR EL MOMENTO

CREATE TABLE IF NOT EXISTS puerta (
    id_puerta INT AUTO_INCREMENT PRIMARY KEY,
    IdUsuario INT NOT NULL,
    hora_apertura DATE NOT NULL,
    hora_cierre DATE NOT NULL,
    FOREIGN KEY (IdUsuario) REFERENCES usuario(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- Esta tabla de aquí creo que no hace falta y la habría que modificar la de parcelas para que contenga algo como esto, aun por mirar. 
CREATE TABLE IF NOT EXISTS Pasto (
    id_vaca_pasto INT AUTO_INCREMENT PRIMARY KEY,
    Numero_pendiente INT NOT NULL,
    IdUsuario INT NOT NULL,
    dias_de_pasto INT NOT NULL,
    mes_de_pastore DATE NOT NULL,
    CONSTRAINT fk_vaca_pasto FOREIGN KEY (Numero_pendiente, IdUsuario) REFERENCES Vaca(Numero_pendiente, IdUsuario) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO Pasto (Numero_pendiente,IdUsuario, dias_de_pasto,mes_de_pastore)
VALUES 
(1001,1,1,'2013-01-01'),
(1001,1,1,'2014-01-01'),
(1001,1,1,'2010-01-01'),
(1001,1,1,'2015-01-01'),
(1001,1,1,'2016-01-01'),
(1002,1,1,'2017-01-01'),
(1002,1,1,'2018-01-01'),
(1002,1,1,'2019-01-01'),
(1002,1,1,'2020-01-01'),
(1002,1,1,'2021-01-01');


CREATE TABLE IF NOT EXISTS Leite (
    id_vaca_leite INT AUTO_INCREMENT PRIMARY KEY,
    Numero_pendiente INT NOT NULL,
    IdUsuario INT NOT NULL,
    litros DOUBLE NOT NULL,
    fecha_recogida DATE NOT NULL,
    CONSTRAINT fk_vaca_leite FOREIGN KEY (Numero_pendiente, IdUsuario) REFERENCES Vaca(Numero_pendiente, IdUsuario) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO Leite (Numero_pendiente,IdUsuario, litros,fecha_recogida)
VALUES 
(1001,1,1.0,'2010-01-01'),
(1001,1,1.0,'2013-01-01'),
(1001,1,1.0,'2014-01-01'),
(1001,1,1.0,'2015-01-01'),
(1001,1,1.0,'2016-01-01'),
(1002,1,1.0,'2017-01-01'),
(1002,1,1.0,'2018-01-01'),
(1002,1,1.0,'2019-01-01'),
(1002,1,1.0,'2020-01-01'),
(1002,1,1.0,'2021-01-01');