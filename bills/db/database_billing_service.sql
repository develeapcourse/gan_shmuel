CREATE DATABASE flaskApp;
use flaskApp;
CREATE TABLE rates (
                productName VARCHAR(400) NOT NULL,
                scope VARCHAR(100) NOT NULL,
                rates FLOAT NOT NULL,
                PRIMARY KEY (productName, scope)
);


CREATE TABLE provider (
                providerId INT NOT NULL AUTO_INCREMENT,
                providerName VARCHAR(400) NOT NULL,
                PRIMARY KEY (providerId)
);
INSERT into provider VALUES (1,"Provider 1");

CREATE TABLE truck (
                truckId INT NOT NULL AUTO_INCREMENT,
                providerId INT NOT NULL,
                PRIMARY KEY (truckId)
);

INSERT into truck VALUES (1,1);

ALTER TABLE truck ADD CONSTRAINT provider_truck_fk
FOREIGN KEY (providerId)
REFERENCES provider (providerId)
ON DELETE NO ACTION
ON UPDATE NO ACTION;
