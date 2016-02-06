PASSWORD=""

mysql -u root -p$PASSWORD -Bse "CREATE DATABASE IF NOT EXISTS ASRank;"
  
  
mysql -u root -p$PASSWORD -D  ASRank -s -e "CREATE TABLE IF NOT EXISTS ASRank.ASRelationships  (
IPversion INT NOT NULL,
AS1 INT NOT NULL,
AS2 INT NOT NULL,
startdate INT(20) NULL,
enddate INT(20) NULL,
relation INT NULL,
PRIMARY KEY (IPversion, AS1, AS2, startdate, enddate));


CREATE TABLE IF NOT EXISTS ASRank.CustomerCone(
IPversion INT NOT NULL,
AS1 INT NOT NULL,
Customer INT NOT NULL,
startdate INT(20) NULL,
enddate INT(20) NULL,
PRIMARY KEY (IPversion, AS1, Customer, startdate, enddate));

"


