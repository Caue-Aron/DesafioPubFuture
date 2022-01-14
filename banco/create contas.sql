create table CONTA(
    ID INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    INSTITUICAO varchar(100),
    TIPO varchar(30),
    SALDO double,
    DATA_CRIACAO date
)