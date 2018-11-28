CREATE DATABASE weight_system;
use weight_system;

CREATE TABLE tara_trucks (
        truck_id VARCHAR(11) NOT NULL,
        truck_weight INT(5),
        unit VARCHAR(3) NOT NULL,
        PRIMARY KEY (truck_id)
);

INSERT into tara_trucks VALUES ("1",200,"kl");


CREATE TABLE tara_containers (
        container_id VARCHAR(50) NOT NULL,
        container_weight INT(5),
        unit VARCHAR(3) NOT NULL,
        PRIMARY KEY (container_id)
);

INSERT into tara_containers VALUES ("1",50,"kl");

CREATE TABLE weighings (
        id INT(11) NOT NULL AUTO_INCREMENT,
        session_id VARCHAR(50) NOT NULL,
        datetime BIGINT NOT NULL,
        weight INT(5) NOT NULL,
        unit VARCHAR(3) NOT NULL,
        direction VARCHAR(4) NOT NULL,
        truck_id VARCHAR(11) NOT NULL,
        containers_id VARCHAR(50) NOT NULL,
        produce VARCHAR(50) NOT NULL,
        PRIMARY KEY (id)
);

INSERT into weighings VALUES (1,12,20181102090000,400,1,"in","1","1","orange");
INSERT into weighings VALUES (2,12,20181102010000,100,1,"out","1","1","na");

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
