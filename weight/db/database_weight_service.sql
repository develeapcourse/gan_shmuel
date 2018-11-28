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
        container_weight VARCHAR(5),
        unit VARCHAR(3) NOT NULL,
        PRIMARY KEY (id, container_id)
);

CREATE TABLE weighings (
        id INT(11) NOT NULL AUTO_INCREMENT,
        session_id VARCHAR(50) NOT NULL,
        datetime VARCHAR(14) NOT NULL,
        weight VARCHAR(5) NOT NULL,
        unit VARCHAR(3) NOT NULL,
        direction VARCHAR(4) NOT NULL,
        truck_id VARCHAR(11) NOT NULL,
        containers_id VARCHAR(50) NOT NULL,
        produce VARCHAR(50) NOT NULL,
        PRIMARY KEY (id)
);


