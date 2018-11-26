CREATE DATABASE weight_system;
use weight_system;
CREATE TABLE tara_trucks (
		id INT(11) NOT NULL,
		truck_id VARCHAR(50) NOT NULL,
		truck_weight INT(5000),
		unit VARCHAR(5) NOT NULL,
		PRIMARY KEY (id, truck_id)
);

CREATE TABLE tara_containers (
		id INT(11) NOT NULL,
		container_id VARCHAR(50) NOT NULL,
		container_weight INT(5000),
		unit VARCHAR(5) NOT NULL,
		PRIMARY KEY (id, container_id)
);

CREATE TABLE weighings (
		id INT(11) NOT NULL,
		session_id VARCHAR(500) NOT NULL,
		datetime DATETIME NOT NULL,
		weight INT(5000) NOT NULL,
		unit VARCHAR(5) NOT NULL,
		direction VARCHAR(10) NOT NULL
		truck_id VARCHAR(50) NOT NULL,
		containers_id VARCHAR(500) NOT NULL,
		produce VARCHAR(50) NOT NULL,
		PRIMARY KEY (id)
);

ALTER TABLE weighings ADD CONSTRAINT tara_trucks_weighings_fk
FOREIGN KEY (truck_id)
REFERENCES tara_trucks (truck_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION;

ALTER TABLE weighings ADD CONSTRAINT tara_containers_weighings_fk
FOREIGN KEY (container_id)
REFERENCES tara_containers (container_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION;
