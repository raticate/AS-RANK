PASSWORD="root"

mysql -u root -p$PASSWORD -Bse "CREATE DATABASE IF NOT EXISTS ASRank;"

mysql -u root -p$PASSWORD -D ASRank -s -e "CREATE TABLE IF NOT EXISTS ASRank.ASRelationships  (
id SERIAL,
IPversion INT NOT NULL,
AS1 INT NOT NULL,
AS2 INT NOT NULL,
startdate INT(20) NULL,
enddate INT(20) NULL,
relation INT NULL,
PRIMARY KEY (IPversion, AS1, AS2, startdate));

CREATE TABLE IF NOT EXISTS ASRank.CustomerCone(
id SERIAL,
IPversion INT NOT NULL,
AS1 INT NOT NULL,
Customer INT NOT NULL,
startdate INT(20) NULL,
enddate INT(20) NULL,
PRIMARY KEY (IPversion, AS1, Customer, startdate));

CREATE TABLE IF NOT EXISTS ASRank.CustomerConeSize(
id SERIAL,
IPversion INT NOT NULL,
AS1 INT NOT NULL,
startdate INT NOT NULL,
Size INT NOT NULL);

CREATE TABLE IF NOT EXISTS ASRank.BGPView(
id SERIAL,
IPversion INT NOT NULL,
startdate INT NOT NULL,
Size INT NOT NULL);

CREATE TABLE IF NOT EXISTS ASRank.CustomerPrefixCone(
id SERIAL,
IPversion INT NOT NULL,
AS1 INT NOT NULL,
Prefix TEXT NOT NULL,
startdate INT NULL,
enddate INT NULL);
"
