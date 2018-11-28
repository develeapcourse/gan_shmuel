CREATE DATABASE weight_system;
use weight_system;
CREATE TABLE tara_trucks (
        id INT(11) NOT NULL AUTO_INCREMENT,
        truck_id VARCHAR(11) NOT NULL,
        truck_weight INT(5),
        unit VARCHAR(3) NOT NULL,
        PRIMARY KEY (id, truck_id)
);

CREATE TABLE tara_containers (
        id INT(11) NOT NULL AUTO_INCREMENT,
        container_id VARCHAR(50) NOT NULL,
        container_weight INT(5),
        unit VARCHAR(3) NOT NULL,
        PRIMARY KEY (id, container_id)
);

CREATE TABLE weighings (
        id INT(11) NOT NULL AUTO_INCREMENT,
        session_id VARCHAR(50) NOT NULL,
        datetime DATETIME NOT NULL,
        weight INT(5) NOT NULL,
        unit VARCHAR(3) NOT NULL,
        direction VARCHAR(4) NOT NULL,
        truck_id VARCHAR(11) NOT NULL,
        containers_id VARCHAR(50) NOT NULL,
        produce VARCHAR(50) NOT NULL,
        PRIMARY KEY (id)
);

/*ALTER TABLE weighings ADD CONSTRAINT tara_trucks_weighings_fk
FOREIGN KEY (truck_id)
REFERENCES tara_trucks (truck_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION;

ALTER TABLE weighings ADD CONSTRAINT tara_containers_weighings_fk
FOREIGN KEY (container_id)
REFERENCES tara_containers (container_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION;*/
