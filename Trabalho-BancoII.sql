-- Criação do banco de dados
CREATE DATABASE IF NOT EXISTS projeto_final;
USE projeto_final;

-- ========================
-- TABELAS
-- ========================

-- Tabela de Pacientes
CREATE TABLE paciente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    data_nascimento DATE,
    telefone VARCHAR(25),
    email VARCHAR(100)
);

-- Criação da tabela Especialidade (deve ser criada antes de médico)
CREATE TABLE especialidade (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

-- Tabela Médico com chave estrangeira para especialidade
CREATE TABLE medico (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    crm VARCHAR(20) UNIQUE NOT NULL,
    especialidade_id INT,
    CONSTRAINT fk_medico_especialidade FOREIGN KEY (especialidade_id) REFERENCES especialidade(id)
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- Tabela Clínicas
CREATE TABLE clinica (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    endereco VARCHAR(200)
);

CREATE TABLE log_delecao_paciente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255),
    cpf VARCHAR(20),
    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Tabela Consultas com chaves estrangeiras para paciente, médico e clínica
CREATE TABLE consulta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT,
    medico_id INT,
    clinica_id INT,
    data_consulta DATETIME NOT NULL,
    status VARCHAR(20) DEFAULT 'Agendada',
    observacoes TEXT,
    CONSTRAINT fk_consulta_paciente FOREIGN KEY (paciente_id) REFERENCES paciente(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_consulta_medico FOREIGN KEY (medico_id) REFERENCES medico(id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_consulta_clinica FOREIGN KEY (clinica_id) REFERENCES clinica(id)
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- Tabela Receita Médica com chave estrangeira para consulta
CREATE TABLE receita_medica (
    id INT AUTO_INCREMENT PRIMARY KEY,
    consulta_id INT,
    medicamento TEXT,
    posologia TEXT,
    CONSTRAINT fk_receita_consulta FOREIGN KEY (consulta_id) REFERENCES consulta(id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- ========================
-- VIEW – Consultas futuras com detalhes
-- ========================
CREATE OR REPLACE VIEW vw_consultas_futuras AS
SELECT 
    c.id AS consulta_id,
    p.nome AS paciente,
    m.nome AS medico,
    e.nome AS especialidade,
    cl.nome AS clinica,
    c.data_consulta,
    c.status
FROM consulta c
JOIN paciente p ON c.paciente_id = p.id
JOIN medico m ON c.medico_id = m.id
JOIN especialidade e ON m.especialidade_id = e.id
JOIN clinica cl ON c.clinica_id = cl.id
WHERE c.data_consulta >= NOW();

-- ========================
-- FUNÇÃO – Contar consultas de um paciente
-- ========================
DELIMITER $$

CREATE FUNCTION total_consultas_paciente(pacienteID INT) RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE total INT;
    SELECT COUNT(*) INTO total FROM consulta WHERE paciente_id = pacienteID;
    RETURN total;
END $$

DELIMITER ;

-- ========================
-- PROCEDURE – Agendar nova consulta
-- ========================
DELIMITER $$

CREATE PROCEDURE agendar_consulta(
    IN p_paciente_id INT,
    IN p_medico_id INT,
    IN p_clinica_id INT,
    IN p_data DATETIME,
    IN p_obs TEXT
)
BEGIN
    INSERT INTO consulta (paciente_id, medico_id, clinica_id, data_consulta, observacoes)
    VALUES (p_paciente_id, p_medico_id, p_clinica_id, p_data, p_obs);
END $$

DELIMITER ;

-- ========================
-- TRIGGER – Impede agendamento de consulta no passado
-- ========================
DELIMITER $$

CREATE TRIGGER before_insert_consulta
BEFORE INSERT ON consulta
FOR EACH ROW
BEGIN
    IF NEW.data_consulta < NOW() THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Não é possível agendar uma consulta no passado.';
    END IF;
END $$

DELIMITER ;

DELIMITER //

CREATE TRIGGER after_delete_paciente
AFTER DELETE ON pacientes
FOR EACH ROW
BEGIN
    INSERT INTO log_delecao_paciente (nome, cpf)
    VALUES (OLD.nome, OLD.cpf);
END //

DELIMITER ;

-- ========================
-- TRANSAÇÃO – Exemplo (usar no código cliente)
-- ========================
-- START TRANSACTION;
-- INSERT INTO paciente (...) VALUES (...);
-- SET @id_paciente = LAST_INSERT_ID();
-- CALL agendar_consulta(@id_paciente, ..., ..., ..., ...);
-- COMMIT;

-- ========================
-- DADOS DE EXEMPLO
-- ========================

INSERT INTO especialidade (nome) VALUES 
('Clínico Geral'), 
('Cardiologia'), 
('Pediatria');

INSERT INTO medico (nome, crm, especialidade_id) VALUES
('Dra. Ana Silva', 'CRM12345', 1),
('Dr. João Cardoso', 'CRM67890', 2),
('Dr. Carlos Eduardo', 'CRM11223', 3),
('Dra. Mariana Oliveira', 'CRM44556', 4);


INSERT INTO clinica (nome, endereco) VALUES
('Clínica Vida', 'Rua das Flores, 123'),
('Saúde Total', 'Av. Brasil, 456');

INSERT INTO paciente (nome, cpf, data_nascimento, telefone, email) VALUES
('Ana Sophia Araújo', '438.150.926-98', '1938-11-09', '+55 (041) 1338 9083', 'ana-liviafreitas@gmail.com'),
('Samuel Pereira', '542.170.863-26', '1983-05-22', '(084) 9407 8161', 'isabelly31@gmail.com'),
('Daniela Gonçalves', '139.826.507-12', '1982-11-19', '+55 (084) 4192-8327', 'luiza83@ig.com.br'),
('Sr. Enzo Azevedo', '564.017.289-49', '1988-05-17', '(051) 2423-8849', 'omoreira@hotmail.com'),
('Luna Carvalho', '012.583.967-77', '1998-03-26', '51 4801 8451', 'dda-cruz@gmail.com'),
('Dra. Emanuella Santos', '281.659.703-21', '1956-07-08', '71 8095-7015', 'carlos-eduardoduarte@bol.com.br'),
('Bruno Rodrigues', '182.953.647-82', '1963-05-11', '71 3465-7871', 'cauemendes@vieira.net'),
('Breno Caldeira', '310.627.895-12', '1963-09-09', '71 2997-3763', 'pintothales@oliveira.br'),
('Srta. Nicole Castro', '065.891.473-10', '1953-08-11', '(011) 2473-1781', 'carvalhoraquel@da.br'),
('João Caldeira', '260.398.514-06', '1955-08-07', '+55 (071) 4309-8050', 'hsantos@caldeira.com'),
('Noah Campos', '361.478.029-50', '1991-08-03', '0800 985 4353', 'qcostela@ig.com.br'),
('Lorenzo Lopes', '107.468.523-71', '2003-05-20', '+55 71 2513-5427', 'vieiranoah@ig.com.br'),
('Daniel Ferreira', '192.764.853-09', '1962-03-29', '+55 71 8740-1640', 'sophia24@pires.br'),
('Alana Correia', '120.684.937-13', '1940-03-23', '(041) 5053 3158', 'lucasda-cruz@hotmail.com'),
('Alice da Luz', '563.210.749-34', '1964-10-21', '+55 (081) 7543-3036', 'daniel45@ig.com.br'),
('Juliana Teixeira', '501.274.683-07', '1993-09-04', '(084) 5698 1693', 'pintoalexandre@bol.com.br'),
('Nina da Paz', '561.924.830-51', '1975-05-29', '21 4656-4823', 'nda-luz@bol.com.br'),
('João Vieira', '048.137.265-26', '1994-09-16', '+55 11 8721-4895', 'maria-eduardalima@da.com'),
('Lucas Cardoso', '763.589.410-20', '1954-08-13', '+55 (011) 1632 8708', 'ramosgabriel@souza.br'),
('Mariana Santos', '687.153.490-39', '1972-04-10', '41 7347-1434', 'evelyn12@hotmail.com'),
('João Pedro da Costa', '316.924.780-87', '1962-09-06', '84 6909 6705', 'ipeixoto@ig.com.br'),
('Dra. Yasmin das Neves', '734.860.512-53', '1956-12-29', '(061) 2980-6990', 'dcunha@barros.br'),
('Lorenzo Martins', '564.832.019-15', '1941-08-15', '(084) 3100 3309', 'fernandoribeiro@da.org'),
('Sr. Otávio Correia', '241.809.375-14', '1944-11-15', '0900 314 9190', 'emoura@bol.com.br'),
('Heloísa Alves', '671.329.840-04', '2005-07-17', '+55 81 9877-6945', 'freitasana-sophia@rezende.com'),
('Giovanna da Mata', '735.629.481-82', '1935-11-30', '41 3136-7837', 'faragao@yahoo.com.br'),
('João Farias', '457.962.381-91', '1982-05-31', '(051) 4443-1351', 'leandrorocha@souza.org'),
('Diogo Gonçalves', '352.704.198-23', '1941-12-14', '81 4271-0947', 'lmendes@gmail.com'),
('Lucca Correia', '167.048.953-10', '1946-02-15', '+55 51 1869 9938', 'tpires@bol.com.br'),
('Gabriela Caldeira', '913.582.074-88', '1958-03-10', '81 1206-7974', 'murilogomes@cardoso.net'),
('Yuri da Paz', '613.582.904-15', '1957-02-11', '(041) 9947 1746', 'fpires@bol.com.br'),
('Leandro Martins', '940.718.625-30', '1940-01-03', '+55 (051) 7874-2967', 'amonteiro@martins.com'),
('Isaac Oliveira', '746.980.351-39', '1968-11-18', '(061) 1680 8760', 'lais77@da.com'),
('Leonardo Rodrigues', '103.592.846-98', '1947-03-21', '+55 21 1712-7484', 'pribeiro@uol.com.br'),
('Bianca Nogueira', '382.607.914-04', '1934-11-18', '(011) 4997 2787', 'gabrielly86@uol.com.br'),
('Sr. Samuel Duarte', '963.870.251-68', '1986-06-02', '51 2702 8951', 'souzaana-vitoria@gmail.com'),
('Srta. Júlia da Costa', '174.283.096-03', '1977-08-18', '(084) 8091-3431', 'castroana-luiza@hotmail.com'),
('Sra. Alice Barbosa', '504.263.187-90', '1959-01-14', '+55 (041) 2196-9379', 'beatrizfernandes@fernandes.com'),
('Esther Viana', '217.946.358-82', '1996-09-15', '(031) 3671 3695', 'augusto64@gmail.com'),
('Nina Barros', '974.618.203-03', '1968-08-22', '+55 84 1047 0952', 'pietro62@costela.org'),
('Fernando Rocha', '451.307.926-61', '1984-04-24', '+55 31 6048 1754', 'enrico37@gmail.com'),
('Maria Eduarda Martins', '931.582.604-33', '1940-09-14', '+55 (051) 4711 3826', 'maria-clara86@bol.com.br'),
('Dra. Brenda Peixoto', '176.208.934-31', '1966-09-01', '21 1585 0643', 'qcarvalho@aragao.net'),
('Yuri da Rocha', '183.495.207-79', '1972-04-08', '+55 (011) 2842-1020', 'joanamartins@gmail.com'),
('Francisco Barros', '261.503.478-26', '1996-01-19', '21 3908-4700', 'rpereira@gmail.com'),
('Raquel Pires', '195.480.732-50', '1986-05-16', '0300-847-8961', 'ana-juliaporto@oliveira.br'),
('Sabrina Castro', '569.728.143-91', '1943-09-02', '+55 31 1161 5280', 'oliveirathales@ig.com.br'),
('Rebeca Barros', '495.087.163-39', '1965-01-19', '+55 51 5851 4936', 'benicio24@mendes.br'),
('Diego da Conceição', '961.750.423-52', '1985-09-24', '84 7525 4599', 'da-costaian@cardoso.br'),
('Lara Rodrigues', '976.214.058-30', '1949-08-16', '(011) 9784 0369', 'da-rochaotavio@cunha.br'),
('Alexandre Sales', '628.341.705-17', '1940-04-15', '(021) 0715-9696', 'enzo60@yahoo.com.br'),
('Pedro Henrique Ramos', '516.708.324-90', '2005-11-04', '+55 21 6453 5218', 'sophiemonteiro@da.net'),
('Danilo Fernandes', '328.650.179-40', '1997-09-04', '0300 979 9552', 'ribeiroana-luiza@ig.com.br'),
('Guilherme Caldeira', '581.239.047-97', '1973-08-08', '+55 11 1998 6798', 'uda-mota@santos.com'),
('Levi Cavalcanti', '512.083.476-08', '1984-01-22', '31 4665 9051', 'nogueiramiguel@yahoo.com.br'),
('Dra. Maria da Costa', '512.763.890-86', '1976-08-31', '84 6528-1685', 'pedro-henrique23@rodrigues.net'),
('Daniel da Costa', '149.865.027-94', '1952-05-14', '0300-622-2927', 'rmoreira@pires.br'),
('Luiz Otávio Duarte', '473.259.816-19', '1986-07-03', '21 8623-9240', 'gabrielly18@gmail.com'),
('Bruno da Cruz', '472.630.158-62', '1938-02-28', '84 0685 3615', 'lopeseduardo@da.com'),
('Gustavo Henrique Ribeiro', '278.405.613-90', '1954-11-18', '81 9861-4341', 'ana-beatrizramos@correia.com'),
('Maitê Duarte', '246.089.153-98', '1960-01-10', '+55 21 8518 8888', 'cribeiro@moura.org'),
('Srta. Isabella Campos', '531.642.708-44', '1980-08-10', '+55 (051) 7722-1704', 'da-pazbruno@lima.br'),
('Lorena Fernandes', '034.296.751-70', '1993-12-31', '71 7652 7758', 'pereiradavi-lucca@uol.com.br'),
('Carolina Viana', '451.028.973-14', '1957-03-18', '(031) 5705-9640', 'gmoreira@araujo.br'),
('Cauê Campos', '358.940.126-51', '1985-01-07', '31 7192 8565', 'enzoaraujo@ig.com.br'),
('Luiz Felipe Silveira', '681.293.754-19', '2001-05-20', '+55 (081) 1217-2715', 'vieiraevelyn@yahoo.com.br'),
('Davi Lucca da Luz', '583.019.476-75', '1983-08-26', '81 9578-2911', 'hrocha@uol.com.br'),
('Maria Julia Cardoso', '251.364.908-70', '1952-02-04', '(021) 8018-2422', 'ryansilveira@yahoo.com.br'),
('Fernando da Paz', '842.579.063-83', '1955-07-09', '+55 (041) 9959-0010', 'sofiapeixoto@bol.com.br'),
('Alice Sales', '849.316.250-70', '1942-09-08', '+55 (031) 7677-3592', 'nicole56@hotmail.com'),
('Sr. Ian Duarte', '714.385.069-10', '1986-10-25', '0800-632-5953', 'dsilva@lima.br'),
('Bryan Novaes', '873.142.096-69', '2001-11-20', '0300-748-0162', 'sarah65@gmail.com'),
('Ana Beatriz da Mota', '584.037.921-23', '1950-09-14', '+55 81 1655 8523', 'barbosabreno@hotmail.com'),
('Sra. Yasmin Ribeiro', '872.461.935-37', '1956-08-25', '61 9495 8887', 'xaragao@yahoo.com.br'),
('Ana Sophia Peixoto', '940.832.167-78', '1999-12-03', '+55 (041) 8962-3091', 'pirespedro-lucas@da.br'),
('Srta. Júlia Santos', '970.514.623-34', '1999-08-21', '51 6527 8585', 'pda-mota@yahoo.com.br'),
('Fernanda das Neves', '493.567.218-82', '1971-10-01', '(011) 1986 6524', 'maysa15@fernandes.br'),
('Eduardo Teixeira', '489.107.652-67', '2006-10-22', '+55 21 3016-5712', 'aliceribeiro@da.org'),
('Dr. Pedro Caldeira', '130.986.742-96', '1959-11-21', '(021) 0049 9154', 'gcunha@uol.com.br'),
('Diogo Correia', '527.981.064-94', '1974-09-07', '0300 329 6685', 'lcastro@rocha.com'),
('João Pedro Duarte', '745.289.016-76', '1966-09-10', '+55 (081) 1742 6841', 'laura33@hotmail.com'),
('Brenda Ramos', '956.843.102-06', '2006-01-20', '(041) 8519-1088', 'isaacmartins@correia.net'),
('Dra. Luiza Carvalho', '870.314.659-66', '1997-06-17', '(041) 0640 3910', 'mariana18@gmail.com'),
('Lucas Azevedo', '462.813.759-55', '1985-11-28', '41 1825 1286', 'alexandrearagao@rezende.br'),
('Isis Dias', '375.126.094-34', '1936-08-29', '+55 41 3119-0790', 'nunesana-laura@viana.com'),
('Evelyn Dias', '958.126.437-09', '1971-12-24', '+55 (081) 8926 8705', 'maria66@hotmail.com'),
('João Miguel da Mata', '873.612.590-30', '1990-09-12', '84 8826 3435', 'fmoura@barros.com'),
('Diogo da Rosa', '735.201.469-16', '1999-09-18', '+55 51 9363 8546', 'paulo45@bol.com.br'),
('Letícia Castro', '753.269.084-92', '1954-05-23', '+55 (031) 4899 6423', 'vitor-hugofarias@uol.com.br'),
('Milena Mendes', '478.312.506-62', '1959-08-01', '71 0801-0062', 'da-costaanthony@santos.com'),
('Maysa Rocha', '708.463.951-93', '2007-06-12', '(011) 0862 1182', 'laviniasouza@moraes.org'),
('Ana Júlia Moura', '673.512.048-53', '1947-04-04', '71 6687 0021', 'kmelo@gmail.com'),
('Amanda Dias', '374.062.591-07', '1936-08-30', '+55 (084) 9261-4293', 'vitor21@bol.com.br'),
('Sra. Ana Beatriz Castro', '631.245.870-90', '1971-09-25', '(041) 7358-6629', 'goncalvesluiz-felipe@ig.com.br'),
('Bruno Fogaça', '269.537.408-92', '1935-03-29', '(041) 7541 2126', 'bcavalcanti@gmail.com'),
('Sr. Noah Martins', '604.398.127-04', '1986-05-08', '+55 (041) 2444-7212', 'ana-beatriz47@gmail.com'),
('Dr. Felipe Sales', '937.012.654-61', '1986-03-27', '(071) 7569 2459', 'llopes@lopes.org'),
('Dra. Maysa Rodrigues', '935.826.704-65', '1959-01-08', '81 0737-4167', 'lucca42@nascimento.com'),
('Maria Vitória Rocha', '968.402.537-83', '1982-11-06', '+55 (041) 9096-5610', 'leonardo88@porto.br'),
('Maria Sophia Santos', '250.379.684-29', '1953-10-24', '(084) 4573 8757', 'uporto@jesus.com');

CALL agendar_consulta(1, 1, 1, '2025-09-13 08:42:42', 'Rem exercitationem debitis rem.');
CALL agendar_consulta(2, 2, 1, '2025-10-08 00:45:59', 'Animi corporis provident consequuntur beatae.');
CALL agendar_consulta(3, 1, 1, '2025-07-17 22:18:04', 'Officia perspiciatis cum voluptates doloribus.');
CALL agendar_consulta(4, 2, 1, '2025-08-01 16:10:46', 'Cum nam vero doloremque illo delectus.');
CALL agendar_consulta(5, 1, 1, '2025-09-15 22:05:53', 'Hic qui sunt ipsum inventore.');
CALL agendar_consulta(6, 1, 1, '2025-07-16 04:02:36', 'Dignissimos quibusdam repellat aperiam.');
CALL agendar_consulta(7, 2, 1, '2025-07-25 14:46:25', 'Deleniti eveniet itaque ea similique minus.');
CALL agendar_consulta(8, 1, 1, '2025-09-15 18:54:18', 'Nisi nostrum nesciunt expedita sapiente.');
CALL agendar_consulta(9, 1, 1, '2025-09-13 16:14:00', 'Repellendus provident error nostrum.');
CALL agendar_consulta(10, 1, 1, '2025-07-23 23:09:38', 'Est dolores blanditiis.');
CALL agendar_consulta(11, 2, 1, '2025-08-20 23:32:25', 'Magni in consequuntur.');
CALL agendar_consulta(12, 2, 2, '2025-08-21 23:46:59', 'Delectus odio possimus officia voluptatum.');
CALL agendar_consulta(13, 1, 1, '2025-09-07 14:42:51', 'Laudantium consequuntur et iste.');
CALL agendar_consulta(14, 2, 2, '2025-07-20 22:35:50', 'Veritatis laborum deserunt fugit natus.');
CALL agendar_consulta(15, 2, 1, '2025-09-17 03:26:13', 'Illum laudantium quae ipsam cumque natus.');
CALL agendar_consulta(16, 1, 2, '2025-10-01 00:12:39', 'Eos eius modi cumque.');
CALL agendar_consulta(17, 1, 1, '2025-08-29 03:18:36', 'Quia quisquam mollitia beatae beatae quod.');
CALL agendar_consulta(18, 2, 1, '2025-10-03 16:03:43', 'Molestiae quidem quis ipsam dolor.');
CALL agendar_consulta(19, 2, 2, '2025-08-26 00:21:23', 'Quasi officiis dolorum.');
CALL agendar_consulta(20, 2, 1, '2025-10-08 16:07:43', 'Ipsum expedita repellendus.');
CALL agendar_consulta(21, 2, 1, '2025-08-27 08:46:52', 'Quod dolores repellat.');
CALL agendar_consulta(22, 2, 1, '2025-09-10 19:38:10', 'Similique nostrum incidunt nulla quos.');
CALL agendar_consulta(23, 2, 2, '2025-10-02 17:20:10', 'Rem necessitatibus minus nisi.');
CALL agendar_consulta(24, 1, 1, '2025-08-01 02:01:18', 'Voluptatem eos nemo veritatis maiores.');
CALL agendar_consulta(25, 1, 1, '2025-10-11 03:11:16', 'Consequatur quibusdam illum.');
CALL agendar_consulta(26, 2, 1, '2025-07-21 11:49:13', 'Sint consectetur sint dolorum.');
CALL agendar_consulta(27, 1, 1, '2025-09-22 19:20:39', 'Repudiandae quis perspiciatis laudantium neque.');
CALL agendar_consulta(28, 2, 2, '2025-08-10 19:49:49', 'Impedit iste odio sunt at maiores eius.');
CALL agendar_consulta(29, 2, 2, '2025-10-08 21:58:18', 'Iste laborum neque sit sed.');
CALL agendar_consulta(30, 1, 2, '2025-07-24 18:42:35', 'Odio possimus sed recusandae id.');
CALL agendar_consulta(31, 2, 1, '2025-08-26 10:48:54', 'Libero eum eligendi molestias.');
CALL agendar_consulta(32, 2, 1, '2025-07-28 09:58:50', 'Sequi ratione tempora quis aliquid numquam.');
CALL agendar_consulta(33, 1, 1, '2025-10-04 23:19:53', 'Accusamus ut culpa itaque voluptatibus.');
CALL agendar_consulta(34, 1, 2, '2025-08-26 06:31:07', 'Voluptatum tenetur sunt error.');
CALL agendar_consulta(35, 2, 2, '2025-10-08 15:13:41', 'At facere assumenda optio.');
CALL agendar_consulta(36, 1, 2, '2025-09-16 17:44:48', 'Amet numquam quas quidem.');
CALL agendar_consulta(37, 1, 1, '2025-08-26 09:51:17', 'Provident a labore.');
CALL agendar_consulta(38, 1, 2, '2025-07-28 14:53:13', 'Dolorem perspiciatis ab possimus repellendus voluptates.');
CALL agendar_consulta(39, 2, 2, '2025-08-25 17:44:13', 'Labore dolorem at.');
CALL agendar_consulta(40, 1, 1, '2025-10-01 23:41:22', 'Aut facilis error.');
CALL agendar_consulta(41, 2, 1, '2025-08-21 21:28:43', 'Odit perspiciatis architecto.');
CALL agendar_consulta(42, 2, 2, '2025-09-08 10:14:16', 'Nostrum cum expedita.');
CALL agendar_consulta(43, 2, 1, '2025-08-05 10:07:45', 'Quibusdam ullam nulla ipsam dolor tempore consequuntur.');
CALL agendar_consulta(44, 2, 1, '2025-07-27 16:39:04', 'Quas expedita inventore ratione dolorum officia.');
CALL agendar_consulta(45, 1, 2, '2025-08-08 19:56:42', 'Nobis quam eligendi velit ad sed.');
CALL agendar_consulta(46, 2, 2, '2025-10-08 18:29:57', 'Dignissimos non deleniti hic.');
CALL agendar_consulta(47, 2, 1, '2025-09-16 11:21:31', 'Quos recusandae dolores.');
CALL agendar_consulta(48, 1, 2, '2025-08-22 04:51:09', 'Dolores odit architecto.');
CALL agendar_consulta(49, 1, 1, '2025-10-10 00:33:08', 'Voluptates ut consequatur.');
CALL agendar_consulta(50, 1, 1, '2025-10-07 07:30:58', 'In molestias cupiditate iusto voluptates asperiores.');
CALL agendar_consulta(51, 1, 2, '2025-09-10 18:19:49', 'Accusamus dolor ullam.');
CALL agendar_consulta(52, 1, 2, '2025-09-30 08:51:11', 'Magni occaecati magnam impedit praesentium.');
CALL agendar_consulta(53, 2, 2, '2025-07-23 17:44:41', 'Modi corrupti assumenda aspernatur ullam voluptate.');
CALL agendar_consulta(54, 2, 1, '2025-07-30 19:43:44', 'Eveniet nesciunt quis officiis officia est.');
CALL agendar_consulta(55, 1, 2, '2025-08-27 05:05:25', 'Animi assumenda ipsa iste.');
CALL agendar_consulta(56, 2, 1, '2025-09-12 20:21:23', 'Est qui qui.');
CALL agendar_consulta(57, 2, 2, '2025-07-27 07:59:47', 'Provident praesentium cum.');
CALL agendar_consulta(58, 1, 2, '2025-08-18 09:33:20', 'Maxime reprehenderit ea fuga quibusdam sit.');
CALL agendar_consulta(59, 1, 2, '2025-09-24 21:32:18', 'Quo adipisci rem.');
CALL agendar_consulta(60, 1, 1, '2025-08-11 03:26:05', 'Aperiam quae nemo aspernatur iste facere.');
CALL agendar_consulta(61, 2, 1, '2025-09-02 05:50:59', 'Cumque culpa quo tempora perferendis beatae.');
CALL agendar_consulta(62, 1, 2, '2025-09-25 15:48:59', 'A similique accusamus aliquid facilis ullam.');
CALL agendar_consulta(63, 1, 1, '2025-08-02 02:41:00', 'Mollitia totam qui.');
CALL agendar_consulta(64, 2, 2, '2025-08-25 10:52:31', 'Eum impedit quam earum.');
CALL agendar_consulta(65, 1, 1, '2025-07-23 07:09:51', 'Fuga magnam temporibus debitis rem voluptatem.');
CALL agendar_consulta(66, 2, 2, '2025-08-23 15:53:48', 'Soluta sint quo.');
CALL agendar_consulta(67, 1, 1, '2025-08-14 21:39:08', 'Assumenda itaque fuga eos quos.');
CALL agendar_consulta(68, 1, 1, '2025-09-25 13:00:40', 'Doloribus fuga voluptas voluptatum quod quasi.');
CALL agendar_consulta(69, 1, 2, '2025-09-06 19:14:58', 'Corrupti ut ad molestiae.');
CALL agendar_consulta(70, 1, 1, '2025-09-15 11:31:33', 'Veritatis a omnis.');
CALL agendar_consulta(71, 1, 2, '2025-10-06 04:00:05', 'Aut minus dolores laudantium.');
CALL agendar_consulta(72, 1, 2, '2025-07-21 13:14:23', 'Quae at ullam.');
CALL agendar_consulta(73, 2, 1, '2025-10-10 20:30:19', 'Impedit tempora itaque quibusdam neque magnam.');
CALL agendar_consulta(74, 1, 2, '2025-09-15 14:29:39', 'Asperiores necessitatibus ipsa vitae dolores.');
CALL agendar_consulta(75, 2, 2, '2025-08-10 01:49:37', 'Unde hic rerum eveniet iste.');
CALL agendar_consulta(76, 2, 2, '2025-08-07 10:01:40', 'Velit consequatur quo.');
CALL agendar_consulta(77, 1, 1, '2025-07-26 07:35:57', 'Autem ipsum et.');
CALL agendar_consulta(78, 1, 1, '2025-07-27 11:00:40', 'Facere quo iste iure sequi at.');
CALL agendar_consulta(79, 2, 1, '2025-10-02 03:30:40', 'Repudiandae possimus aliquam saepe.');
CALL agendar_consulta(80, 1, 1, '2025-08-16 13:29:19', 'At dolorum explicabo.');
CALL agendar_consulta(81, 1, 1, '2025-09-03 14:07:18', 'Perspiciatis ea voluptatibus.');
CALL agendar_consulta(82, 1, 1, '2025-07-18 18:06:02', 'Sequi nam mollitia atque aut.');
CALL agendar_consulta(83, 1, 1, '2025-09-30 19:23:05', 'Commodi aperiam quos.');
CALL agendar_consulta(84, 2, 1, '2025-08-06 07:38:35', 'Dicta id placeat.');
CALL agendar_consulta(85, 1, 2, '2025-09-16 07:53:56', 'Neque ea repellat.');
CALL agendar_consulta(86, 2, 1, '2025-07-17 20:28:20', 'Deserunt officia repellat.');
CALL agendar_consulta(87, 1, 2, '2025-07-24 15:59:59', 'Commodi velit amet unde inventore.');
CALL agendar_consulta(88, 1, 2, '2025-09-24 01:43:13', 'Libero fugit incidunt explicabo tenetur.');
CALL agendar_consulta(89, 2, 1, '2025-08-11 10:25:41', 'Ipsum corrupti nostrum nulla.');
CALL agendar_consulta(90, 1, 1, '2025-09-16 13:56:31', 'Libero sunt laboriosam assumenda.');
CALL agendar_consulta(91, 2, 2, '2025-08-21 22:09:52', 'In odit reiciendis.');
CALL agendar_consulta(92, 2, 2, '2025-08-08 22:13:49', 'Voluptatibus molestiae accusantium fugit quae laboriosam quos.');
CALL agendar_consulta(93, 2, 1, '2025-08-18 03:19:54', 'Magnam harum debitis eum dolor tempore.');
CALL agendar_consulta(94, 1, 1, '2025-09-29 07:47:59', 'Animi voluptatibus minus quisquam.');
CALL agendar_consulta(95, 2, 2, '2025-08-07 08:02:57', 'Aut omnis eaque repellendus.');
CALL agendar_consulta(96, 1, 1, '2025-09-25 07:08:55', 'Quisquam veniam nemo.');
CALL agendar_consulta(97, 1, 1, '2025-10-01 03:43:44', 'Explicabo saepe sapiente debitis nihil.');
CALL agendar_consulta(98, 2, 1, '2025-10-02 00:16:48', 'Totam adipisci praesentium veniam natus.');
CALL agendar_consulta(99, 2, 1, '2025-09-08 09:48:46', 'Saepe repellat voluptas molestiae.');
CALL agendar_consulta(100, 2, 2, '2025-08-01 18:45:03', 'Alias animi nobis accusantium labore ex.');




